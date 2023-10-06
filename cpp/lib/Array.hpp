// Implementation of a dynamic array
template <class T>
class Array {
private:
public:
	int n; T *a;

	Array() {
		n = 0;
	}

	Array(int entries) : n(entries) {
		a = new T[n]();
	}

	~Array() {
		delete[] a;
	}

	Array(const Array<T> &A) : n(A.n) {
		a = new T[n];
		memcpy(a, A.a, sizeof(T) * n);
	}

	Array<T>& operator = (const Array<T> &A) {
		if (n != 0) {
			delete[] a;
		}
		n = A.n;
		a = new T[n];
		memcpy(a, A.a, sizeof(T) * n);
		return *this;
	}

	void init(int entries) {
		if (n != 0) {
			delete[] a;
		}
		n = entries;
		a = new T[n]();
	}

	T& operator [] (int i) {
        return a[i];
    }
};