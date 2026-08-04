import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QGroupBox, QListWidget, QTableWidget, QPushButton, QFormLayout, QComboBox,
    QLabel, QLineEdit, QSplitter, QStatusBar, QAbstractItemView, QHeaderView,
    QTextEdit, QDoubleSpinBox, QSlider, QAction, QTableWidgetItem
)
from PyQt5.QtCore import Qt

# For plotting, we'll use Matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatplotlibCanvas(FigureCanvas):
    """A simple canvas for embedding Matplotlib plots in PyQt5."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(fig)
        self.setParent(parent)
        # Placeholder plot
        self.axes.set_title("Membership Functions")
        self.axes.set_xlabel("Universe of Discourse")
        self.axes.set_ylabel("Membership Grade")
        self.axes.grid(True)
        self.figure.tight_layout()

class MainWindow(QMainWindow):
    """Main application window for the PyIT2FLS UI."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyIT2FLS Designer (PyQt5)")
        self.setGeometry(100, 100, 1200, 800)

        self._create_actions()
        self._create_menu_bar()
        self._create_status_bar()

        # Main layout
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create tabs
        self.variables_tab = QWidget()
        self.rules_tab = QWidget()
        self.simulation_tab = QWidget()

        self.tabs.addTab(self.variables_tab, "1. Variables & Sets")
        self.tabs.addTab(self.rules_tab, "2. Fuzzy Rules")
        self.tabs.addTab(self.simulation_tab, "3. Simulation & Visualization")

        # Populate tabs with content
        self._create_variables_tab()
        self._create_rules_tab()
        self._create_simulation_tab()

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
        self.open_action = QAction("&Open System...", self)
        self.save_action = QAction("&Save System...", self)
        self.exit_action = QAction("E&xit", self)
        self.exit_action.triggered.connect(self.close)
        self.about_action = QAction("&About", self)

    def _create_status_bar(self):
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

    def _create_variables_tab(self):
        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        # --- Input Variables Panel ---
        input_group = QGroupBox("Input Variables")
        input_layout = QVBoxLayout()
        
        self.input_var_list = QListWidget()
        self.input_var_list.addItems(["service", "food"]) # Example
        
        input_buttons_layout = QHBoxLayout()
        add_input_btn = QPushButton("Add")
        remove_input_btn = QPushButton("Remove")
        input_buttons_layout.addWidget(add_input_btn)
        input_buttons_layout.addWidget(remove_input_btn)
        
        mf_group = QGroupBox("Membership Functions (MFs)")
        mf_layout = QVBoxLayout()
        self.input_mf_table = QTableWidget(3, 4) # Example size
        self.input_mf_table.setHorizontalHeaderLabels(["Name", "Type", "UMF Params", "LMF Params"])
        self.input_mf_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Example data
        self.input_mf_table.setItem(0, 0, QTableWidgetItem("poor"))
        self.input_mf_table.setItem(0, 1, QTableWidgetItem("Triangular"))
        self.input_mf_table.setItem(0, 2, QTableWidgetItem("[0, 1, 2]"))
        self.input_mf_table.setItem(0, 3, QTableWidgetItem("[0.5, 1, 1.5]"))

        mf_buttons_layout = QHBoxLayout()
        add_mf_btn = QPushButton("Add MF")
        remove_mf_btn = QPushButton("Remove MF")
        mf_buttons_layout.addWidget(add_mf_btn)
        mf_buttons_layout.addWidget(remove_mf_btn)

        mf_layout.addWidget(self.input_mf_table)
        mf_layout.addLayout(mf_buttons_layout)
        mf_group.setLayout(mf_layout)

        # Plot for inputs
        self.input_plot_canvas = MatplotlibCanvas(self)

        input_layout.addWidget(QLabel("Variables:"))
        input_layout.addWidget(self.input_var_list)
        input_layout.addLayout(input_buttons_layout)
        input_layout.addWidget(mf_group)
        input_layout.addWidget(self.input_plot_canvas)
        input_group.setLayout(input_layout)

        # --- Output Variables Panel ---
        output_group = QGroupBox("Output Variables")
        output_layout = QVBoxLayout()
        self.output_var_list = QListWidget()
        self.output_var_list.addItems(["tip"]) # Example
        
        output_buttons_layout = QHBoxLayout()
        add_output_btn = QPushButton("Add")
        remove_output_btn = QPushButton("Remove")
        output_buttons_layout.addWidget(add_output_btn)
        output_buttons_layout.addWidget(remove_output_btn)

        output_mf_group = QGroupBox("Membership Functions (MFs)")
        output_mf_layout = QVBoxLayout()
        self.output_mf_table = QTableWidget(3, 4)
        self.output_mf_table.setHorizontalHeaderLabels(["Name", "Type", "UMF Params", "LMF Params"])
        self.output_mf_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        output_mf_buttons = QHBoxLayout()
        output_mf_buttons.addWidget(QPushButton("Add MF"))
        output_mf_buttons.addWidget(QPushButton("Remove MF"))
        output_mf_layout.addWidget(self.output_mf_table)
        output_mf_layout.addLayout(output_mf_buttons)
        output_mf_group.setLayout(output_mf_layout)

        self.output_plot_canvas = MatplotlibCanvas(self)

        output_layout.addWidget(QLabel("Variables:"))
        output_layout.addWidget(self.output_var_list)
        output_layout.addLayout(output_buttons_layout)
        output_layout.addWidget(output_mf_group)
        output_layout.addWidget(self.output_plot_canvas)
        output_group.setLayout(output_layout)

        splitter.addWidget(input_group)
        splitter.addWidget(output_group)
        splitter.setSizes([600, 600])
        layout.addWidget(splitter)
        self.variables_tab.setLayout(layout)

    def _create_rules_tab(self):
        layout = QVBoxLayout()
        
        # Rule creator
        rule_builder_group = QGroupBox("Rule Builder")
        rule_builder_layout = QHBoxLayout()
        rule_builder_layout.setAlignment(Qt.AlignLeft)

        rule_builder_layout.addWidget(QLabel("IF"))
        var1_combo = QComboBox()
        var1_combo.addItems(["service", "food"])
        rule_builder_layout.addWidget(var1_combo)
        
        rule_builder_layout.addWidget(QLabel("is"))
        mf1_combo = QComboBox()
        mf1_combo.addItems(["poor", "good", "excellent"])
        rule_builder_layout.addWidget(mf1_combo)

        op_combo = QComboBox()
        op_combo.addItems(["AND", "OR"])
        rule_builder_layout.addWidget(op_combo)

        var2_combo = QComboBox()
        var2_combo.addItems(["service", "food"])
        var2_combo.setCurrentIndex(1)
        rule_builder_layout.addWidget(var2_combo)
        
        rule_builder_layout.addWidget(QLabel("is"))
        mf2_combo = QComboBox()
        mf2_combo.addItems(["rancid", "delicious"])
        rule_builder_layout.addWidget(mf2_combo)

        rule_builder_layout.addWidget(QLabel("THEN"))
        out_var_combo = QComboBox()
        out_var_combo.addItems(["tip"])
        rule_builder_layout.addWidget(out_var_combo)
        
        rule_builder_layout.addWidget(QLabel("is"))
        out_mf_combo = QComboBox()
        out_mf_combo.addItems(["small", "average", "generous"])
        rule_builder_layout.addWidget(out_mf_combo)
        
        rule_builder_layout.addStretch()
        rule_builder_group.setLayout(rule_builder_layout)

        add_rule_button = QPushButton("Add Rule to List")
        
        # Rule list
        rule_list_group = QGroupBox("Rule Base")
        rule_list_layout = QVBoxLayout()
        self.rule_list_widget = QTextEdit()
        self.rule_list_widget.setReadOnly(True)
        self.rule_list_widget.setPlainText("IF service is poor AND food is rancid THEN tip is small") # Example
        remove_rule_button = QPushButton("Remove Selected Rule")
        remove_rule_button.setEnabled(False) # Placeholder
        rule_list_layout.addWidget(self.rule_list_widget)
        rule_list_layout.addWidget(remove_rule_button)
        rule_list_group.setLayout(rule_list_layout)

        layout.addWidget(rule_builder_group)
        layout.addWidget(add_rule_button)
        layout.addWidget(rule_list_group)
        self.rules_tab.setLayout(layout)

    def _create_simulation_tab(self):
        layout = QHBoxLayout()
        
        # --- Input Controls ---
        controls_group = QGroupBox("Live Inputs & Output")
        controls_layout = QVBoxLayout()

        input_values_layout = QFormLayout()
        self.input_sliders = {}
        for var_name in ["service", "food"]: # Example inputs
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100) # Example range
            label = QLabel("5.0") # Example value
            
            # Connect slider to label update
            slider.valueChanged.connect(lambda val, lbl=label: lbl.setText(f"{val/10.0:.1f}"))
            
            slider_layout = QHBoxLayout()
            slider_layout.addWidget(slider)
            slider_layout.addWidget(label)
            
            input_values_layout.addRow(f"{var_name.capitalize()}:", slider_layout)

        evaluate_button = QPushButton("Evaluate System")
        
        output_layout = QFormLayout()
        self.crisp_output_label = QLabel("N/A")
        font = self.crisp_output_label.font()
        font.setPointSize(16)
        font.setBold(True)
        self.crisp_output_label.setFont(font)
        output_layout.addRow("Crisp Output (tip):", self.crisp_output_label)

        controls_layout.addLayout(input_values_layout)
        controls_layout.addWidget(evaluate_button)
        controls_layout.addSpacing(30)
        controls_layout.addLayout(output_layout)
        controls_layout.addStretch()
        controls_group.setLayout(controls_layout)
        controls_group.setFixedWidth(350)

        # --- Visualization Plot ---
        plot_group = QGroupBox("Control Surface")
        plot_layout = QVBoxLayout()
        self.surface_plot_canvas = MatplotlibCanvas(self)
        
        # Update placeholder for 3D plot
        self.surface_plot_canvas.axes.remove()
        self.surface_plot_canvas.axes = self.surface_plot_canvas.figure.add_subplot(111, projection='3d')
        self.surface_plot_canvas.axes.set_title("System Control Surface")
        self.surface_plot_canvas.axes.set_xlabel("Service")
        self.surface_plot_canvas.axes.set_ylabel("Food")
        self.surface_plot_canvas.axes.set_zlabel("Tip")

        plot_layout.addWidget(self.surface_plot_canvas)
        plot_group.setLayout(plot_layout)

        layout.addWidget(controls_group)
        layout.addWidget(plot_group)
        self.simulation_tab.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) # Note the exec_() here for PyQt5
