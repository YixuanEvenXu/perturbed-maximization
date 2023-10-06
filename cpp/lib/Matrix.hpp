// Implementation of a dynamic matrix
template <class T>
class Matrix {
private:
public:
	int n, m; T **a;
	
	Matrix() {
		n = m = 0;
	}

	Matrix(const Matrix<T> &M) : n(M.n), m(M.m) {
		a = new T*[n];
		for (int i = 0; i < n; i++) {
			a[i] = new T[m];
			memcpy(a[i], M.a[i], sizeof(T) * m);
		}
	}

	Matrix<T>& operator = (const Matrix<T> &M) {
		if (n != 0 && m != 0) {
			for (int i = 0; i < n; i++)
				delete[] a[i];
			delete[] a;
		}
		n = M.n;
		m = M.m;
		a = new T*[n];
		for (int i = 0; i < n; i++) {
			a[i] = new T[m];
			memcpy(a[i], M.a[i], sizeof(T) * m);
		}
		return *this;
	}

	Matrix(int rows, int cols) : n(rows), m(cols) {
		a = new T*[n];
		for (int i = 0; i < n; i++)
			a[i] = new T[m]();
	}

	~Matrix() {
		for (int i = 0; i < n; i++)
			delete[] a[i];
		delete[] a;
	}

	void init(int rows, int cols) {
		if (n != 0 && m != 0) {
			for (int i = 0; i < n; i++)
				delete[] a[i];
			delete[] a;
		}
		n = rows, m = cols;
		a = new T*[n];
		for (int i = 0; i < n; i++)
			a[i] = new T[m]();
	}
	
	T* operator [] (int i) {
        return a[i];
    }
};