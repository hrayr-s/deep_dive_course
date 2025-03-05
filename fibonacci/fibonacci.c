#include <stdio.h>


unsigned long long fib_cache[100] = {0}; // Supports up to fib(99)


/**
 * Traditional Fibonacci calculator
 * @param n-th Fibonacci number
 * @return
 */
int fibonacci(int n)
{
    if (n < 1)
    {
        return 0;
    }

    if (n == 1) { return 1; }
    return fibonacci(n - 1) + fibonacci(n - 2);
}


/**
 * Calculate Fibonacci number using formula and caching
 * @param n-th Fibonacci number
 * @return
 */
unsigned long long int de_formula(unsigned long long int n) {
    if (n == 0) { return 0; }
    if (n == 1) { return 1; }

    if (n <= 99 && fib_cache[n] != 0) return fib_cache[n];

    if (n % 2 == 0) {
        unsigned long long int k = n / 2;

        k = de_formula(k) * (2 * de_formula(k - 1) + de_formula(k));
        if (n <=99 && fib_cache[n] == -1)
        {
            fib_cache[n] = k;
        }
        return k;
    }

    unsigned long long int _n = (n + 1) / 2;
    unsigned long long int a = de_formula(_n);
    unsigned long long int b = de_formula(_n - 1);
    _n = a * a + b * b;
    if (_n <= 99)
    {
        fib_cache[n] = _n;
    }
    return _n;
}


/**
 * Calculates Fibonacci number without using cache and print the call level with nth number.
 * So, this visualizes the approach without caching and can be seen how many numbers(recursions) we skip.
 * @param n-th Fibonacci number
 * @param level recursion level
 * @return
 */
unsigned long long int de_formula_l(unsigned long long int n, int level) {
    if (n == 0) { return 0; }
    if (n == 1) { return 1; }
    for (int i = 0; i < level; i++)
    {
        printf("\t");
    }
    if (n % 2 == 0) {
        unsigned long long int k = n / 2;
        printf("%llu\n", k);
        return de_formula_l(k, level + 1) * (2 * de_formula_l(k - 1, level + 1) + de_formula_l(k, level + 1));
    }
    unsigned long long int _n = (n + 1) / 2;
    printf("%llu\n", _n);
    unsigned long long int a = de_formula_l(_n, level + 1);
    unsigned long long int b = de_formula_l(_n - 1, level + 1);
    return a * a + b * b;
}

int main() {
    printf("Fibonacci 20th is: %llu\n", de_formula(20));
    printf("Fibonacci 40th is: %llu\n", de_formula(40));
    printf("Fibonacci 400th is: %llu\n", de_formula(400));
    printf("Fibonacci 41st is: %llu\n", de_formula_l(41, 0));
    return 0;
}
