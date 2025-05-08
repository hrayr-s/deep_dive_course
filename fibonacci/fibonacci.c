#include <math.h>
#include <stdio.h>


unsigned long long int de_formula(unsigned long long int n) {
    if (n == 0) {
        return 0;
    }

    if (n == 1) {
        return 1;
    }

    if (n <= 4) {
        return de_formula(n-1) + de_formula(n-2);
    }

    if (n % 2 == 1) {
        return pow(de_formula(n / 2), 2) + pow(de_formula(n / 2 + 1), 2);
    } else {
        unsigned long long int _n = n / 2;
        return de_formula(_n) * (de_formula(_n - 1) + de_formula(_n + 1));
    }
}

int main() {
    for (int i=2; i <= 10; i++) {
        printf("it is: %llu\n", de_formula(i));
    }
    return 0;
}