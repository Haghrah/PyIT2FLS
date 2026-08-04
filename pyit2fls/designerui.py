"""
PyIT2FLS Designer: a PyQt5 GUI for interactively building, simulating, and
saving/loading Type 1 Mamdani fuzzy logic systems.

This module is only imported by :mod:`pyit2fls` when PyQt5 is installed
(``pip install pyit2fls[gui]``); the rest of the toolkit does not depend on
it. Launch it with the ``pyit2fls-designer`` console script, or with
``python3 -m pyit2fls.designerui``.

The designer keeps its system as the same ``variables``/``rules``
intermediate representation used by :mod:`pyit2fls.FML` and
:mod:`pyit2fls.FCL` (see :func:`pyit2fls.FML.generate_system`), so a system
built in the GUI can be saved as either an FML or FCL file, and either file
format can be opened for further editing. See ``markdown docs/DesignerGUI.md``
for a tutorial.

.. rubric:: Notes

The designer targets Type 1 Mamdani systems only, matching the scope of
:mod:`pyit2fls.FCL` (IEC 61131-7 does not define Takagi-Sugeno rule blocks).
"""
import sys

from numpy import linspace, zeros, meshgrid

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QGroupBox, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QPushButton, QFormLayout, QComboBox, QLabel, QLineEdit, QSplitter,
    QStatusBar, QHeaderView, QSlider, QAction, QDialog, QDialogButtonBox,
    QCheckBox, QFileDialog, QMessageBox, QInputDialog,
)
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

try:
    # Registers the "3d" projection with Matplotlib; every 3D plot elsewhere
    # in this project (e.g. examples/ex_8.py, ex_13.py) imports this
    # explicitly rather than relying on Figure.add_subplot(projection="3d")
    # to auto-import it, since that lazy import is not reliable across
    # Matplotlib versions/installations.
    from mpl_toolkits.mplot3d import Axes3D
    HAS_3D = True
except ImportError:
    HAS_3D = False

from pyit2fls.FML import FML, generate_system, MF_MAP, _default_height, ensure_negated_term
from pyit2fls.FCL import FCL


#: Membership function shapes offered by the "Add MF" dialog, mapped to the
#: shape keys understood by :data:`pyit2fls.FML.MF_MAP`.
MF_SHAPES = {
    "Triangular": "triangularShape",
    "Trapezoidal": "trapezoidalShape",
    "Gaussian": "gaussianShape",
    "Singleton": "singletonShape",
}


def blank_model():
    """
    Returns a fresh, empty ``(variables, rules)`` pair, in the shared shape
    documented in :func:`pyit2fls.FML.generate_system`.
    """
    variables = {"input": {}, "output": {}}
    rules = {"name": "System", "type": "mamdani", "andMethod": "prod",
              "orMethod": "max", "activationMethod": "min", "rules": {}}
    return variables, rules


class MatplotlibCanvas(FigureCanvas):
    """A simple canvas for embedding Matplotlib plots in PyQt5."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(fig)
        self.setParent(parent)
        self.axes.set_title("Membership Functions")
        self.axes.set_xlabel("Universe of Discourse")
        self.axes.set_ylabel("Membership Grade")
        self.axes.grid(True)
        self.figure.tight_layout()


class FormDialog(QDialog):
    """
    A small reusable modal dialog with one text field per entry in
    ``fields``, used for every "Add ..." action in the designer.

    .. rubric:: Parameters

    parent : QWidget

        Parent widget.

    title : str

        Dialog window title.

    fields : list of tuple

        Each tuple is ``(key, label, default_text)``. ``key`` is the name
        under which the field's text is returned by :func:`values`.
    """
    def __init__(self, parent, title, fields):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QFormLayout(self)
        self.edits = {}
        for key, label, default in fields:
            edit = QLineEdit(str(default))
            self.edits[key] = edit
            layout.addRow(label, edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def values(self):
        """Returns ``{key: text}`` for every field, as entered by the user."""
        return {key: edit.text() for key, edit in self.edits.items()}


class MainWindow(QMainWindow):
    """
    Main window of the PyIT2FLS designer.

    .. rubric:: Members

    variables : dict

        The system's input/output variables and terms, in the shared shape
        documented in :func:`pyit2fls.FML.generate_system`.

    rules : dict

        The system's rule base, in the same shared shape.

    .. rubric:: Notes

    The window keeps ``variables``/``rules`` as its single source of truth;
    every widget (variable lists, MF tables, rule builder combo boxes,
    simulation sliders) is refreshed from that state rather than edited
    directly, so File > Open and File > New behave consistently with manual
    edits made through the tabs.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyIT2FLS Designer")
        self.setGeometry(100, 100, 1200, 800)

        self.variables, self.rules = blank_model()
        self.system_name = self.rules["name"]
        self.panels = {}
        self.input_sliders = {}
        self.output_labels = {}

        self._create_actions()
        self._create_menu_bar()
        self._create_status_bar()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.variables_tab = QWidget()
        self.rules_tab = QWidget()
        self.simulation_tab = QWidget()

        self.tabs.addTab(self.variables_tab, "1. Variables & Sets")
        self.tabs.addTab(self.rules_tab, "2. Fuzzy Rules")
        self.tabs.addTab(self.simulation_tab, "3. Simulation & Visualization")

        self._create_variables_tab()
        self._create_rules_tab()
        self._create_simulation_tab()

        self._refresh_all()

    # ------------------------------------------------------------------
    # Menu bar
    # ------------------------------------------------------------------
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.about_action)

    def _create_actions(self):
        self.new_action = QAction("&New System", self)
        self.new_action.triggered.connect(self._new_system)
        self.open_action = QAction("&Open System...", self)
        self.open_action.triggered.connect(self._open_system)
        self.save_action = QAction("&Save System...", self)
        self.save_action.triggered.connect(self._save_system)
        self.exit_action = QAction("E&xit", self)
        self.exit_action.triggered.connect(self.close)
        self.about_action = QAction("&About", self)
        self.about_action.triggered.connect(self._show_about)

    def _create_status_bar(self):
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

    def _show_about(self):
        QMessageBox.about(
            self, "About PyIT2FLS Designer",
            "PyIT2FLS Designer\n\n"
            "A GUI for building, simulating, and saving/loading Type 1 "
            "Mamdani fuzzy logic systems, as FML or FCL files.")

    # ------------------------------------------------------------------
    # Tab 1: Variables & Sets
    # ------------------------------------------------------------------
    def _create_variables_tab(self):
        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._build_variable_panel("input"))
        splitter.addWidget(self._build_variable_panel("output"))
        splitter.setSizes([600, 600])
        layout.addWidget(splitter)
        self.variables_tab.setLayout(layout)

    def _build_variable_panel(self, var_type):
        title = "Input Variables" if var_type == "input" else "Output Variables"
        group = QGroupBox(title)
        layout = QVBoxLayout()

        var_list = QListWidget()
        add_var_btn = QPushButton("Add Variable")
        remove_var_btn = QPushButton("Remove Variable")
        var_buttons = QHBoxLayout()
        var_buttons.addWidget(add_var_btn)
        var_buttons.addWidget(remove_var_btn)

        mf_group = QGroupBox("Membership Functions (MFs)")
        mf_layout = QVBoxLayout()
        mf_table = QTableWidget(0, 4)
        mf_table.setHorizontalHeaderLabels(["Name", "Type", "Params", "Complement"])
        mf_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        add_mf_btn = QPushButton("Add MF")
        remove_mf_btn = QPushButton("Remove MF")
        mf_buttons = QHBoxLayout()
        mf_buttons.addWidget(add_mf_btn)
        mf_buttons.addWidget(remove_mf_btn)
        mf_layout.addWidget(mf_table)
        mf_layout.addLayout(mf_buttons)
        mf_group.setLayout(mf_layout)

        canvas = MatplotlibCanvas(self)

        layout.addWidget(QLabel("Variables:"))
        layout.addWidget(var_list)
        layout.addLayout(var_buttons)
        layout.addWidget(mf_group)
        layout.addWidget(canvas)
        group.setLayout(layout)

        self.panels[var_type] = {"list": var_list, "table": mf_table, "canvas": canvas}

        var_list.currentTextChanged.connect(lambda name, vt=var_type: self._refresh_mf_table(vt, name))
        add_var_btn.clicked.connect(lambda _, vt=var_type: self._add_variable(vt))
        remove_var_btn.clicked.connect(lambda _, vt=var_type: self._remove_variable(vt))
        add_mf_btn.clicked.connect(lambda _, vt=var_type: self._add_term(vt))
        remove_mf_btn.clicked.connect(lambda _, vt=var_type: self._remove_term(vt))

        return group

    def _add_variable(self, var_type):
        dlg = FormDialog(self, "Add Variable",
                          [("name", "Name", ""), ("left", "Domain left", "0"), ("right", "Domain right", "1")])
        if dlg.exec_() != QDialog.Accepted:
            return
        values = dlg.values()
        name = values["name"].strip()
        if not name or name in self.variables[var_type]:
            QMessageBox.warning(self, "Invalid name", "Variable name must be non-empty and unique.")
            return
        try:
            left, right = float(values["left"]), float(values["right"])
        except ValueError:
            QMessageBox.warning(self, "Invalid domain", "Domain left/right must be numbers.")
            return
        if right <= left:
            QMessageBox.warning(self, "Invalid domain", "Domain right must be greater than domain left.")
            return

        self.variables[var_type][name] = {"domainleft": left, "domainright": right, "terms": {}}
        if var_type == "output":
            self.variables[var_type][name]["defuzzifier"] = "COG"
        self.statusBar().showMessage(f"Added {var_type} variable '{name}'")
        self._refresh_all(select={var_type: name})

    def _remove_variable(self, var_type):
        item = self.panels[var_type]["list"].currentItem()
        if item is None:
            return
        del self.variables[var_type][item.text()]
        self._refresh_all()

    def _add_term(self, var_type):
        var_item = self.panels[var_type]["list"].currentItem()
        if var_item is None:
            QMessageBox.warning(self, "No variable selected", "Select a variable first.")
            return
        var_name = var_item.text()

        name, ok = QInputDialog.getText(self, "Term name", "Name:")
        if not ok or not name.strip():
            return
        shape_label, ok = QInputDialog.getItem(self, "Shape", "Membership function shape:",
                                                list(MF_SHAPES.keys()), editable=False)
        if not ok:
            return
        params_text, ok = QInputDialog.getText(
            self, "Parameters", "Comma-separated parameters (height optional, default 1):")
        if not ok:
            return
        try:
            params = [float(p.strip()) for p in params_text.split(",") if p.strip() != ""]
        except ValueError:
            QMessageBox.warning(self, "Invalid parameters", "Parameters must be comma-separated numbers.")
            return

        self.variables[var_type][var_name]["terms"][name.strip()] = {
            "set": MF_SHAPES[shape_label], "params": params, "complement": "false",
        }
        self._refresh_all()

    def _remove_term(self, var_type):
        var_item = self.panels[var_type]["list"].currentItem()
        if var_item is None:
            return
        var_name = var_item.text()
        row = self.panels[var_type]["table"].currentRow()
        if row < 0:
            return
        term_name = self.panels[var_type]["table"].item(row, 0).text()
        del self.variables[var_type][var_name]["terms"][term_name]
        self._refresh_all()

    def _refresh_mf_table(self, var_type, var_name):
        table = self.panels[var_type]["table"]
        table.setRowCount(0)
        terms = self.variables[var_type].get(var_name, {}).get("terms", {})
        for term_name, term_info in terms.items():
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(term_name))
            table.setItem(row, 1, QTableWidgetItem(term_info["set"]))
            table.setItem(row, 2, QTableWidgetItem(", ".join(f"{p:g}" for p in term_info["params"])))
            table.setItem(row, 3, QTableWidgetItem(str(term_info.get("complement", "false"))))
        self._plot_variable(var_type, var_name)

    def _plot_variable(self, var_type, var_name):
        canvas = self.panels[var_type]["canvas"]
        canvas.axes.clear()
        var_info = self.variables[var_type].get(var_name)
        if var_info is not None:
            domain = linspace(var_info["domainleft"], var_info["domainright"], 200)
            for term_name, term_info in var_info["terms"].items():
                if term_name.startswith("NOT_"):
                    continue
                mf = MF_MAP[term_info["set"]]
                params = _default_height(term_info["set"], list(term_info["params"]))
                y = mf(domain, params)
                if str(term_info.get("complement", "false")).lower() == "true":
                    y = 1 - y
                canvas.axes.plot(domain, y, label=term_name)
            if var_info["terms"]:
                canvas.axes.legend()
            canvas.axes.set_title(var_name)
        canvas.axes.set_xlabel("Universe of Discourse")
        canvas.axes.set_ylabel("Membership Grade")
        canvas.axes.grid(True)
        canvas.draw()

    # ------------------------------------------------------------------
    # Tab 2: Fuzzy Rules
    # ------------------------------------------------------------------
    def _create_rules_tab(self):
        layout = QVBoxLayout()

        rule_builder_group = QGroupBox("Rule Builder")
        rb_layout = QHBoxLayout()
        rb_layout.setAlignment(Qt.AlignLeft)

        rb_layout.addWidget(QLabel("IF"))
        self.rule_var1 = QComboBox()
        rb_layout.addWidget(self.rule_var1)
        self.rule_not1 = QCheckBox("NOT")
        rb_layout.addWidget(self.rule_not1)
        rb_layout.addWidget(QLabel("is"))
        self.rule_mf1 = QComboBox()
        rb_layout.addWidget(self.rule_mf1)

        self.rule_op = QComboBox()
        self.rule_op.addItems(["(none)", "AND", "OR"])
        rb_layout.addWidget(self.rule_op)

        self.rule_var2 = QComboBox()
        rb_layout.addWidget(self.rule_var2)
        self.rule_not2 = QCheckBox("NOT")
        rb_layout.addWidget(self.rule_not2)
        rb_layout.addWidget(QLabel("is"))
        self.rule_mf2 = QComboBox()
        rb_layout.addWidget(self.rule_mf2)

        rb_layout.addWidget(QLabel("THEN"))
        self.rule_out_var = QComboBox()
        rb_layout.addWidget(self.rule_out_var)
        rb_layout.addWidget(QLabel("is"))
        self.rule_out_mf = QComboBox()
        rb_layout.addWidget(self.rule_out_mf)

        rb_layout.addStretch()
        rule_builder_group.setLayout(rb_layout)

        self.rule_var1.currentTextChanged.connect(lambda n: self._refresh_term_combo(self.rule_mf1, "input", n))
        self.rule_var2.currentTextChanged.connect(lambda n: self._refresh_term_combo(self.rule_mf2, "input", n))
        self.rule_out_var.currentTextChanged.connect(lambda n: self._refresh_term_combo(self.rule_out_mf, "output", n))

        add_rule_button = QPushButton("Add Rule to List")
        add_rule_button.clicked.connect(self._add_rule)

        rule_list_group = QGroupBox("Rule Base")
        rule_list_layout = QVBoxLayout()
        self.rule_list_widget = QListWidget()
        remove_rule_button = QPushButton("Remove Selected Rule")
        remove_rule_button.clicked.connect(self._remove_rule)
        rule_list_layout.addWidget(self.rule_list_widget)
        rule_list_layout.addWidget(remove_rule_button)
        rule_list_group.setLayout(rule_list_layout)

        layout.addWidget(rule_builder_group)
        layout.addWidget(add_rule_button)
        layout.addWidget(rule_list_group)
        self.rules_tab.setLayout(layout)

    def _refresh_term_combo(self, combo, var_type, var_name):
        combo.blockSignals(True)
        combo.clear()
        terms = self.variables[var_type].get(var_name, {}).get("terms", {})
        combo.addItems([t for t in terms if not t.startswith("NOT_")])
        combo.blockSignals(False)

    def _refresh_rule_builder(self):
        for combo, var_type in ((self.rule_var1, "input"), (self.rule_var2, "input"), (self.rule_out_var, "output")):
            current = combo.currentText()
            combo.blockSignals(True)
            combo.clear()
            combo.addItems(list(self.variables[var_type].keys()))
            combo.blockSignals(False)
            index = combo.findText(current)
            combo.setCurrentIndex(index if index >= 0 else 0)
        self._refresh_term_combo(self.rule_mf1, "input", self.rule_var1.currentText())
        self._refresh_term_combo(self.rule_mf2, "input", self.rule_var2.currentText())
        self._refresh_term_combo(self.rule_out_mf, "output", self.rule_out_var.currentText())

    def _add_rule(self):
        var1, mf1 = self.rule_var1.currentText(), self.rule_mf1.currentText()
        out_var, out_mf = self.rule_out_var.currentText(), self.rule_out_mf.currentText()
        if not (var1 and mf1 and out_var and out_mf):
            QMessageBox.warning(self, "Incomplete rule",
                                 "Select at least one antecedent clause and a consequent.")
            return

        term1 = ensure_negated_term(self.variables, var1, mf1) if self.rule_not1.isChecked() else mf1
        antecedent = [(var1, term1)]
        connector = "and"

        op = self.rule_op.currentText()
        var2, mf2 = self.rule_var2.currentText(), self.rule_mf2.currentText()
        if op != "(none)" and var2 and mf2:
            connector = "and" if op == "AND" else "or"
            term2 = ensure_negated_term(self.variables, var2, mf2) if self.rule_not2.isChecked() else mf2
            antecedent.append((var2, term2))

        rule_name = f"R{len(self.rules['rules']) + 1}"
        self.rules["rules"][rule_name] = {
            "connector": connector, "weight": 1.0,
            "antecedent": antecedent, "consequent": [(out_var, out_mf)],
        }
        self.statusBar().showMessage(f"Added rule {rule_name}")
        self._refresh_all()

    def _remove_rule(self):
        item = self.rule_list_widget.currentItem()
        if item is None:
            return
        del self.rules["rules"][item.data(Qt.UserRole)]
        self._refresh_all()

    def _refresh_rule_list(self):
        self.rule_list_widget.clear()
        for rule_name, rule in self.rules["rules"].items():
            connector = " AND " if rule.get("connector", "and") == "and" else " OR "
            antecedent = connector.join(f"{v} IS {t}" for v, t in rule["antecedent"])
            consequent = " AND ".join(f"{v} IS {t}" for v, t in rule["consequent"])
            item = QListWidgetItem(f"{rule_name}: IF {antecedent} THEN {consequent}")
            item.setData(Qt.UserRole, rule_name)
            self.rule_list_widget.addItem(item)

    # ------------------------------------------------------------------
    # Tab 3: Simulation & Visualization
    # ------------------------------------------------------------------
    def _create_simulation_tab(self):
        layout = QHBoxLayout()

        controls_group = QGroupBox("Live Inputs & Output")
        controls_layout = QVBoxLayout()

        self.sim_input_form = QFormLayout()
        evaluate_button = QPushButton("Evaluate System")
        evaluate_button.clicked.connect(self._evaluate_system)
        self.sim_output_form = QFormLayout()

        controls_layout.addLayout(self.sim_input_form)
        controls_layout.addWidget(evaluate_button)
        controls_layout.addSpacing(30)
        controls_layout.addLayout(self.sim_output_form)
        controls_layout.addStretch()
        controls_group.setLayout(controls_layout)
        controls_group.setFixedWidth(350)

        plot_group = QGroupBox("Control Surface (systems with exactly 2 inputs)")
        plot_layout = QVBoxLayout()
        self.surface_plot_canvas = MatplotlibCanvas(self)
        plot_layout.addWidget(self.surface_plot_canvas)
        plot_group.setLayout(plot_layout)

        layout.addWidget(controls_group)
        layout.addWidget(plot_group)
        self.simulation_tab.setLayout(layout)

    def _refresh_simulation_tab(self):
        while self.sim_input_form.rowCount():
            self.sim_input_form.removeRow(0)
        self.input_sliders.clear()

        for var_name, var_info in self.variables["input"].items():
            left, right = var_info["domainleft"], var_info["domainright"]
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 1000)
            slider.setValue(500)
            label = QLabel(f"{(left + right) / 2:.3f}")

            def _on_change(value, lbl=label, l=left, r=right):
                lbl.setText(f"{l + (r - l) * value / 1000.0:.3f}")
            slider.valueChanged.connect(_on_change)

            row_layout = QHBoxLayout()
            row_layout.addWidget(slider)
            row_layout.addWidget(label)
            self.sim_input_form.addRow(f"{var_name}:", row_layout)
            self.input_sliders[var_name] = (left, right, label)

        while self.sim_output_form.rowCount():
            self.sim_output_form.removeRow(0)
        self.output_labels.clear()

        for var_name in self.variables["output"]:
            label = QLabel("N/A")
            font = label.font()
            font.setPointSize(14)
            font.setBold(True)
            label.setFont(font)
            self.sim_output_form.addRow(f"{var_name}:", label)
            self.output_labels[var_name] = label

    def _evaluate_system(self):
        if not self.variables["input"] or not self.variables["output"] or not self.rules["rules"]:
            QMessageBox.warning(self, "Nothing to evaluate",
                                 "Define at least one input variable, one output variable, and one rule.")
            return
        try:
            system = generate_system(self.variables, self.rules)
        except Exception as exc:
            QMessageBox.critical(self, "Error building system", str(exc))
            return

        inputs = {name: float(label.text()) for name, (left, right, label) in self.input_sliders.items()}
        try:
            _, crisp = system.evaluate(inputs)
        except Exception as exc:
            QMessageBox.critical(self, "Evaluation error", str(exc))
            return

        for var_name, label in self.output_labels.items():
            label.setText(f"{crisp.get(var_name, float('nan')):.4f}")

        self._plot_control_surface(system)

    def _plot_control_surface(self, system):
        canvas = self.surface_plot_canvas
        canvas.figure.clf()
        input_names = list(self.variables["input"].keys())
        output_names = list(self.variables["output"].keys())

        if len(input_names) != 2 or not output_names:
            canvas.axes = canvas.figure.add_subplot(111)
            canvas.axes.set_title("The control surface plot needs exactly 2 input variables.")
            canvas.draw()
            return

        out_name = output_names[0]
        x_name, y_name = input_names
        x_info, y_info = self.variables["input"][x_name], self.variables["input"][y_name]
        n = 15
        X = linspace(x_info["domainleft"], x_info["domainright"], n)
        Y = linspace(y_info["domainleft"], y_info["domainright"], n)
        Z = zeros((n, n))
        for j, yv in enumerate(Y):
            for i, xv in enumerate(X):
                _, crisp = system.evaluate({x_name: xv, y_name: yv})
                Z[j, i] = crisp[out_name]
        XX, YY = meshgrid(X, Y)

        if HAS_3D:
            canvas.axes = canvas.figure.add_subplot(111, projection="3d")
            canvas.axes.plot_surface(XX, YY, Z, cmap="viridis")
            canvas.axes.set_zlabel(out_name)
        else:
            # mpl_toolkits.mplot3d unavailable (e.g. conflicting Matplotlib
            # installs) -- fall back to a 2D heatmap of the same surface
            # rather than losing the whole evaluation because of a plot.
            canvas.axes = canvas.figure.add_subplot(111)
            mesh = canvas.axes.pcolormesh(XX, YY, Z, cmap="viridis", shading="auto")
            canvas.figure.colorbar(mesh, ax=canvas.axes, label=out_name)
        canvas.axes.set_xlabel(x_name)
        canvas.axes.set_ylabel(y_name)
        canvas.axes.set_title("System Control Surface")
        canvas.draw()

    # ------------------------------------------------------------------
    # File menu
    # ------------------------------------------------------------------
    def _refresh_all(self, select=None):
        """
        Rebuilds every widget from ``self.variables``/``self.rules``.

        ``select`` optionally maps ``"input"``/``"output"`` to a variable
        name that should become the selected list item after the rebuild
        (e.g. a variable just added by the user), overriding the default
        of preserving whatever was already selected.
        """
        select = select or {}
        for var_type in ("input", "output"):
            var_list = self.panels[var_type]["list"]
            current = select.get(var_type)
            if current is None and var_list.currentItem() is not None:
                current = var_list.currentItem().text()
            var_list.blockSignals(True)
            var_list.clear()
            var_list.addItems(list(self.variables[var_type].keys()))
            var_list.blockSignals(False)
            matches = var_list.findItems(current, Qt.MatchExactly) if current else []
            if matches:
                var_list.setCurrentItem(matches[0])
            self._refresh_mf_table(var_type, var_list.currentItem().text() if var_list.currentItem() else None)
        self._refresh_rule_builder()
        self._refresh_rule_list()
        self._refresh_simulation_tab()

    def _new_system(self):
        self.variables, self.rules = blank_model()
        self.system_name = self.rules["name"]
        self._refresh_all()
        self.statusBar().showMessage("New system")

    def _open_system(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open System", "", "FML/FCL Files (*.fml *.xml *.fcl);;All Files (*)")
        if not path:
            return
        try:
            with open(path, "r") as f:
                text = f.read()
            if path.lower().endswith(".fcl"):
                name, variables, rules = FCL().parse_fcl(text)
            else:
                name, variables, rules = FML().parse_fml(text)
        except Exception as exc:
            QMessageBox.critical(self, "Failed to open file", str(exc))
            return

        self.system_name, self.variables, self.rules = name, variables, rules
        self._refresh_all()
        self.statusBar().showMessage(f"Opened {path}")

    def _save_system(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save System", f"{self.system_name}.fcl", "FCL File (*.fcl);;FML File (*.fml)")
        if not path:
            return
        try:
            if path.lower().endswith(".fcl"):
                text = FCL().export_fcl(self.system_name, self.variables, self.rules)
            else:
                text = FML().export_fml(self.system_name, self.variables, self.rules)
            with open(path, "w") as f:
                f.write(text)
        except Exception as exc:
            QMessageBox.critical(self, "Failed to save file", str(exc))
            return
        self.statusBar().showMessage(f"Saved {path}")


def main():
    """Launches the PyIT2FLS designer application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
