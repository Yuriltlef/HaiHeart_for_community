#pragma once
class Widegt {
private:
	int* data;
public:
	Widegt(const int size) { data = new int[size]; }
	~Widegt() { delete[] data; }
};

template<typename ANY>
int A(ANY& a) {

	return sizeof(a) / sizeof(a[0]);
}