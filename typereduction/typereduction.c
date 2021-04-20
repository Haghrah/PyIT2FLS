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


void EIASC_algorithm(double *data, double *params, int size, double *result) 
{
	double *rawData = data;
	Interval *intervalArray = (Interval *)(data);
	
	
	int startIndex = -1, endIndex = size;
	int L = 0, R = 0;
	double b = 0, d = 0;
	double a_l = 0, b_l = 0, a_r = 0, b_r = 0;
	double y_l = 0, y_r = 0;
	
	for(int i = 0; i < size; i++)
	{
		if(rawData[2] != 0. && startIndex < 0.) {
			startIndex = i;
		}else if(rawData[2] != 0. && startIndex > -1.) {
			endIndex = i;
		}
		b += rawData[2];
		a_l += rawData[0] * rawData[2];
		a_r += rawData[1] * rawData[3];
		rawData += 4;
	}
	b_l = b;
	b_r = b;
	
	intervalArray = intervalArray + startIndex;
	size = endIndex - startIndex + 1;
	if (size == 0) 
	{
		return;
	}else{
		qsort(intervalArray,size,sizeof(Interval),compare_a);
		
		for(L = 0; L < size; L++)
		{
			d = intervalArray[L].d - intervalArray[L].c;
			a_l += intervalArray[L].a * d;
			b_l += d;
			y_l = a_l / b_l;
			if(abs(y_l - intervalArray[L + 1].a) < epsilon)
			{
				break;
			}
		}
		
		qsort(intervalArray,size,sizeof(Interval),compare_b);
		
		for(R = size - 1; R > 0; R--)
		{
			d = intervalArray[L].d - intervalArray[L].c;
			a_r += intervalArray[L].b * d;
			b_r += d;
			y_r = a_r / b_r;
			if(abs(y_r - intervalArray[R - 1].b) < epsilon)
			{
				break;
			}
		}
		
		result[0] = startIndex;
		result[1] = endIndex;
		result[2] = y_l;
		result[3] = y_r;
	}
	
	
	
	
	
	
	
}
















