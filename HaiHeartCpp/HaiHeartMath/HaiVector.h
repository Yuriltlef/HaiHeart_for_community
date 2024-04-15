#pragma once
#include <iostream>
#define VECTOR_TYPES template<typename ANY, typename LIST_WITH_LEN>
#define ANY_LIST template<typename LIST>

VECTOR_TYPES
class HaiVector;

ANY_LIST
int lenof(const LIST& a);

ANY_LIST
int lenof(const LIST& a) {
	return sizeof(a) / sizeof(a[0]);
}


VECTOR_TYPES
class HaiVector
{
private:
	int len;
	ANY* point_list;

public:
	void print_list();
	HaiVector(LIST_WITH_LEN& p_list) noexcept{
		len = lenof(p_list);
		point_list = new ANY[len];
		for (int i = 0; i < len; i++) {
			point_list[i] = p_list[i];
		}
	};
	~HaiVector() {
		delete[] point_list;
	};
};

VECTOR_TYPES
void HaiVector<ANY, LIST_WITH_LEN>::print_list()
{
	for (int i = 0; i < len; i++) {
		std::cout << point_list[i] << "\n";
	}
}
