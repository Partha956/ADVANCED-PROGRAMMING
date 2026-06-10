#include <stdio.h>
#include <time.h>

int main() {
    int inputs[4] = {1000, 5000, 10000, 20000};
    int i, j, k;
    int n;
    long counter;
    clock_t start, end;
    
    printf("N\tConstant\tLinear\t\tQuadratic\n");

    for (i = 0; i < 4; i++) {
        n = inputs[i];

        start = clock();
        int result = n * n;
        end = clock();
        double time_constant = ((double)(end - start)) / CLOCKS_PER_SEC;

        start = clock();
        counter = 0;
        for (j = 0; j < n; j++) {
            counter++;
        }
        end = clock();
        double time_linear = ((double)(end - start)) / CLOCKS_PER_SEC;

        start = clock();
        counter = 0;
        for (j = 0; j < n; j++) {
            for (k = 0; k < n; k++) {
                counter++;
            }
        }
        end = clock();
        double time_quadratic = ((double)(end - start)) / CLOCKS_PER_SEC;

        printf("%d\t%f\t%f\t%f\n", n, time_constant, time_linear, time_quadratic);
    }

    return 0;
}