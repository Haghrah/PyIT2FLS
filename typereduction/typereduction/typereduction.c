#include <stdlib.h>
#include <math.h>

#define epsilon 0.0000001

struct INTERVAL{
	double a;
	double b;
	double c;
	double d;
};

typedef struct INTERVAL Interval;

int compare_a (const void * in1, const void * in2)
{
	if(((Interval*)in1)->a < ((Interval*)in2)->a) return -1;
	else return 1;
}

int compare_b (const void * in1, const void * in2)
{
	if(((Interval*)in1)->b < ((Interval*)in2)->b) return -1;
	else return 1;
}

int sign(double x) { 
	if (x < 0) {
		return -1;
	}else if (x > 0) {
		return +1;
	}else{
		return  0;
	}
}

int min(int x1, int x2) {
	if (x1 < x2) {
		return x1;
	}else{
		return x2;
	}
}

int max(int x1, int x2) {
	if (x1 > x2) {
		return x1;
	}else{
		return x2;
	}
}

double minf(double x1, double x2) {
	if (x1 < x2) {
		return x1;
	}else{
		return x2;
	}
}

double maxf(double x1, double x2) {
	if (x1 > x2) {
		return x1;
	}else{
		return x2;
	}
}


void WM_algorithm(double *data, double *params, int size, double *result)
{
	double *rawData = data;
	Interval *intervalArray = (Interval *)(data);
	
	char allZero = 1;
	
	double sumF0 = 0., sumF1 = 0., sumF0Y0 = 0., sumF1Y0 = 0., sumF0Y1 = 0., sumF1Y1 = 0.;
	double c = 0., y_l_sup = 0., y_l_inf = 0., y_r_sup = 0., y_r_inf = 0.;
	double s1, s2;
	
	for(int i = 0; i < size; i++)
	{
		if (rawData[2] != 0 || rawData[3] != 0) 
		{
			allZero = 0;
		}
		rawData += 4;
	}
	if(allZero)
	{
		result[0] = 0.;
		result[1] = 0.;
		return;
	}else{
		qsort(intervalArray, size, sizeof(Interval), compare_a);
		
		for (int i = 0; i < size; i++)
		{
			sumF0 += intervalArray[i].c;
			sumF1 += intervalArray[i].d;
			sumF0Y0 += intervalArray[i].a * intervalArray[i].c;
			sumF0Y1 += intervalArray[i].b * intervalArray[i].c;
			sumF1Y0 += intervalArray[i].a * intervalArray[i].d;
			sumF1Y1 += intervalArray[i].b * intervalArray[i].d;
		}
		c = (sumF1 - sumF0) / (sumF0 * sumF1);
		y_l_sup = minf(sumF0Y0 / sumF0, sumF1Y0 / sumF1);
		y_r_inf = minf(sumF1Y1 / sumF1, sumF0Y1 / sumF0);
		
		s1 = sumF0Y0 - sumF0 * intervalArray[0].a;
		s2 = sumF1 * intervalArray[size - 1].a - sumF1Y0;
		y_l_inf = y_l_sup - c * (s1 * s2) / (s1 + s2);
		
		s1 = sumF1Y1 - sumF1 * intervalArray[0].b;
		s2 = sumF0 * intervalArray[size - 1].b - sumF0Y1;
		y_r_sup = y_r_inf + c * (s1 * s2) / (s1 + s2);
		
		result[0] = (y_l_sup + y_l_inf) / 2;
		result[1] = (y_r_sup + y_r_inf) / 2;
	}
	return;
}


void EKM_algorithm(double *data, double *params, int size, double *result)
{
	double *rawData = data;
	Interval *intervalArray = (Interval *)(data);
	
	char allZero = 1;
	int k_l = 0, k_r = 0, k_l_prime = 0, k_r_prime = 0;
	int s_l = 0, s_r = 0;
	int imin = 0, imax = 0;
	double a_l = 0., b_l = 0., a_r = 0., b_r = 0.;
	double a_l_prime = 0., b_l_prime = 0.;
	double a_r_prime = 0., b_r_prime = 0.;
	double y_l = 0., y_l_prime = 0., y_r = 0., y_r_prime = 0.;
	
	
	k_l = (int)(size / 2.4);
	k_r = (int)(size / 1.7);
	
	for(int i = 0; i < size; i++)
	{
		if (rawData[2] != 0 || rawData[3] != 0) 
		{
			allZero = 0;
		}
		if (i < k_l)
		{
			a_l += rawData[0] * rawData[3];
			b_l += rawData[3];
		}else{
			a_l += rawData[0] * rawData[2];
			b_l += rawData[2];
		}
		if (i < k_r)
		{
			a_r += rawData[0] * rawData[2];
			b_r += rawData[2];
		}else{
			a_r += rawData[0] * rawData[3];
			b_r += rawData[3];
		}
		rawData += 4;
	}
	
	
	
	if(allZero)
	{
		result[0] = 0.;
		result[1] = 0.;
		return;
	}else{
		y_l_prime = a_l / b_l;
		y_r_prime = a_r / b_r;
		
		qsort(intervalArray, size, sizeof(Interval), compare_a);
		
		while(1) {
			k_l_prime = 0;
			for (int i = 0; i < size - 1; i++) {
				if((intervalArray[i].a <= y_l_prime && intervalArray[i + 1].a >= y_l_prime) || 
				   (fabs(y_l_prime - intervalArray[i].a) <= epsilon) || 
				   (fabs(y_l_prime - intervalArray[i + 1].a) <= epsilon))
				{
					k_l_prime = i;
					break;
				}
			}
			if (k_l_prime == k_l) {
				y_l = y_l_prime;
				break;
			}
			
			s_l = sign(k_l_prime - k_l);
			imin = min(k_l, k_l_prime) + 1;
			imax = max(k_l, k_l_prime);
			
			a_l_prime = 0;
			b_l_prime = 0;
			for (int i = imin; i < imax; i++) {
				a_l_prime += intervalArray[i].a * (intervalArray[i].d - intervalArray[i].c);
				b_l_prime += intervalArray[i].d - intervalArray[i].c;
			}
			a_l_prime = s_l * a_l_prime + a_l;
			b_l_prime = s_l * b_l_prime + b_l;
			
			k_l = k_l_prime;
			y_l_prime = a_l_prime / b_l_prime;
			a_l = a_l_prime;
			b_l = b_l_prime;
		}
		
		while(1) {
			k_r_prime = 0;
			for (int i = 0; i < size - 1; i++) {
				if((intervalArray[i].a <= y_r_prime && intervalArray[i + 1].a >= y_r_prime) || 
				   (fabs(y_r_prime - intervalArray[i].a) <= epsilon) || 
				   (fabs(y_r_prime - intervalArray[i + 1].a) <= epsilon))
				{
					k_r_prime = i;
					break;
				}
			}
			if (k_r_prime == k_r) {
				y_r = y_r_prime;
				break;
			}
			
			s_r = sign(k_r_prime - k_r);
			imin = min(k_r, k_r_prime) + 1;
			imax = max(k_r, k_r_prime);
			
			a_r_prime = 0;
			b_r_prime = 0;
			for (int i = imin; i < imax; i++) {
				a_r_prime += intervalArray[i].a * (intervalArray[i].d - intervalArray[i].c);
				b_r_prime += intervalArray[i].d - intervalArray[i].c;
			}
			a_r_prime = - s_r * a_r_prime + a_r;
			b_r_prime = - s_r * b_r_prime + b_r;
			
			k_r = k_r_prime;
			y_r_prime = a_r_prime / b_r_prime;
			a_r = a_r_prime;
			b_r = b_r_prime;
		}
		
		result[0] = y_l;
		result[1] = y_r;
	}
	
	return;
}

void KM_algorithm(double *data, double *params, int size, double *result)
{
	double *rawData = data;
	Interval *intervalArray = (Interval *)(data);
	
	char allZero = 1;
	int k_l = 0, k_r = 0;
	double w = 0;
	double y_l_prime = 0., y_r_prime = 0.;
	double y_l_num = 0., y_l_den = 0.;
	double y_r_num = 0., y_r_den = 0.;
	double y_prime_num = 0., y_prime_den = 0.;
	double y_l = 0, y_r = 0;
	
	for(int i = 0; i < size; i++)
	{
		if (rawData[2] != 0 || rawData[3] != 0) 
		{
			allZero = 0;
		}
		w = (rawData[2] + rawData[3]) / 2;
		y_prime_num += rawData[0] * w;
		y_prime_den += w;
		rawData += 4;
	}
	
	if(allZero)
	{
		result[0] = 0.;
		result[1] = 0.;
		return;
	}else{
	
		y_l_prime = y_prime_num / y_prime_den;
		y_r_prime = y_prime_num / y_prime_den;
		
		qsort(intervalArray, size, sizeof(Interval), compare_a);
		
		while(1) {
			k_l = 0;
			for(int i = 0; i < size - 1; i++)
			{
				if((intervalArray[i].a <= y_l_prime && intervalArray[i + 1].a >= y_l_prime) || 
				   (fabs(y_l_prime - intervalArray[i].a) <= epsilon) || 
				   (fabs(y_l_prime - intervalArray[i + 1].a) <= epsilon))
				{
					k_l = i;
					break;
				}
			}
			for(int i = 0; i <= k_l; i++)
			{
				y_l_num += intervalArray[i].a * intervalArray[i].d;
				y_l_den += intervalArray[i].d;
			}
			for(int i = k_l + 1; i < size; i++)
			{
				y_l_num += intervalArray[i].a * intervalArray[i].c;
				y_l_den += intervalArray[i].c;
			}
			y_l = y_l_num / y_l_den;
			if(fabs(y_l - y_l_prime) <= epsilon)
			{
				break;
			}else{
				y_l_prime = y_l;
			}
		}
		
		while(1) {
			k_r = 0;
			for(int i = 0; i < size - 1; i++)
			{
				if((intervalArray[i].a <= y_r_prime && intervalArray[i + 1].a >= y_r_prime) || 
				   (fabs(y_r_prime - intervalArray[i].a) <= epsilon) || 
				   (fabs(y_r_prime - intervalArray[i + 1].a) <= epsilon))
				{
					k_r = i;
					break;
				}
			}
			for(int i = 0; i <= k_r; i++)
			{
				y_r_num += intervalArray[i].a * intervalArray[i].c;
				y_r_den += intervalArray[i].c;
			}
			for(int i = k_r + 1; i < size; i++)
			{
				y_r_num += intervalArray[i].a * intervalArray[i].d;
				y_r_den += intervalArray[i].d;
			}
			y_r = y_r_num / y_r_den;
			if(fabs(y_r - y_r_prime) <= epsilon)
			{
				break;
			}else{
				y_r_prime = y_r;
			}
		}
		
		result[0] = y_l;
		result[1] = y_r;
	
	}
	
	return;
	
}

void EIASC_algorithm(double *data, double *params, int size, double *result) 
{
	double *rawData = data;
	Interval *intervalArray = (Interval *)(data);
	
	char allZero = 1;
	int L = 0, R = 0;
	double d = 0;
	double a_l = 0, b_l = 0, a_r = 0, b_r = 0;
	double y_l = 0, y_r = 0;
	
	for(int i = 0; i < size; i++)
	{
		if (rawData[2] != 0 || rawData[3] != 0) 
		{
			allZero = 0;
		}
		b_l += rawData[2];
		b_r += rawData[2];
		a_l += rawData[0] * rawData[2];
		a_r += rawData[1] * rawData[2];
		rawData += 4;
	}

	if(allZero)
	{
		result[0] = 0.;
		result[1] = 0.;
		return;
	}else{
	
		qsort(intervalArray, size, sizeof(Interval), compare_a);
		
		for(L = 0; L < size; L++)
		{
			d = intervalArray[L].d - intervalArray[L].c;
			a_l += intervalArray[L].a * d;
			b_l += d;
			y_l = a_l / b_l;
			if(y_l <= intervalArray[L + 1].a || fabs(y_l - intervalArray[L + 1].a) < epsilon)
			{
				break;
			}
		}
		
		// We know that Interval.a = Interval.b in IT2FSs!
		//qsort(intervalArray, size, sizeof(Interval), compare_b);
		
		for(R = size - 1; R > 0; R--)
		{
			d = intervalArray[R].d - intervalArray[R].c;
			a_r += intervalArray[R].b * d;
			b_r += d;
			y_r = a_r / b_r;
			if(y_r >= intervalArray[R - 1].b || fabs(y_r - intervalArray[R - 1].b) < epsilon)
			{
				break;
			}
		}
		
		result[0] = y_l;
		result[1] = y_r;
	}
	return;
}
















