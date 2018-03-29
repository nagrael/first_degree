#include <iostream>
#include <cmath>
using namespace std;

float dzeta(float s, int n) {
    float tmp=0;
    for (int i = 1; i <= n; ++i) {
        tmp += 1 / pow(static_cast<float>(i), s);
    }
    return tmp;
}

float rev_dzeta(float s, int n) {
    float tmp=0;
    for (int i = n; i>0; --i) {
        tmp += 1 / pow(static_cast<float>(i), s);
    }
    return tmp;
}

double dzeta(double s, int n) {
    double tmp=0;
    for (int i = 1; i <= n; ++i) {
        tmp += 1 / pow(static_cast<double>(i), s);
    }
    return tmp;
}

double rev_dzeta(double s, int n) {
    double tmp=0;
    for (int i = n; i>0; --i) {
        tmp += 1 / pow(static_cast<double>(i), s);
    }
    return tmp;
}


float eta(float s, int n) {
    float tmp=0;
    for (int i = n; i>0; i--) {
        tmp += (i % 2 - 1) / pow(static_cast<float>(i), s);
    }
    return tmp;
}

float rev_eta(float s, int n) {
    float tmp=0;
    for (int i = 1; i <= n; ++i) {
        tmp += (i % 2 - 1) / pow(static_cast<float>(i), s);
    }
    return tmp;
}

double eta(double s, int n) {
    double tmp=0;
    for (int i = 1; i <= n; ++i) {
        tmp += (i % 2 - 1) / pow(static_cast<double>(i), s);
    }
    return tmp;
}

double rev_eta(double s, int n) {
    double tmp=0;
    for (int i = n; i>0; i--) {
        tmp += (i % 2 - 1) / pow(static_cast<double>(i), s);
    }
    return tmp;
}




float f[] = { 2.f,3.6667f,5.f,7.2f,10.f };
double d[] = { 2,3.6667,5,7.2,10 };
int ns[] = { 50,100,200,500,1000 };

int main() {
    cout.precision(25);
    for (int j = 0;j < 5;j++) {
        for (int i = 0; i < 5; ++i) {
            cout << dzeta(f[i], ns[j]) << " " << rev_dzeta(f[i], ns[j]) << " " << eta(f[i], ns[j])
                << " " << rev_eta(f[i], ns[j]) << endl;
        }
        cout << endl;
        for (int i = 0; i < 5; ++i) {
            cout << dzeta(d[i], ns[j]) << " " << rev_dzeta(d[i], ns[j]) << " " << eta(d[i], ns[j])
                << " " << rev_eta(d[i], ns[j]) << endl;
        }
        cout << endl << endl;
    }

    return 0;


}
