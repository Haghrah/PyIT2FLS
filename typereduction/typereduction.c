#include <math.h>

void EIASC_Algorithm(double *intervals, double *params, int size, double *result){
	double *interval = intervals;
	int startIndex = -1, endIndex = -1;
	double b = 0;
	
	for(int i = 0; i < size; i++)
	{
		if(interval[2] != 0. && startIndex < 0.) {
			startIndex = i;
		}else if(interval[2] == 0. && startIndex > -1.) {
			endIndex = i;
			break;
		}
		b += interval[2];
		interval += 4;
	}
	result[0] = startIndex;
	result[1] = endIndex;
	result[2] = b;
}
















