#include "HaiVector.h"
#include <iostream>

int main() {
	int d[10] = { 1,2,3,3,6,4 };
	HaiVector<int, int [10]> v1(d);
	v1.print_list();
	return 0;
}