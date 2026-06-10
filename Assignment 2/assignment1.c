#include <stdio.h>
#include <stdlib.h>

int main() {
    int inputs[5] = {10, 100, 1000, 5000, 10000};
    int i; 
    int j;
    int k;

    for (k = 0; k < 5; k++) {
        int n = inputs[k];
        printf("Checking for input size: %d\n", n);

        int sum = (n * (n + 1)) / 2;
        int space1 = 4; 
        printf("Constant Time Space: %d bytes\n", space1);

        int *arr = (int*)malloc(n * 4); 
        for(i = 0; i < n; i++) {
            arr[i] = i;
        }
        int space2 = n * 4;
        printf("Linear Time Space: %d bytes\n", space2);

        if(n <= 5000) {
            int *matrix = (int*)malloc(n * n * 4);
            for(i = 0; i < n; i++) {
                for(j = 0; j < n; j++) {
                    matrix[i*n + j] = i * j;
                }
            }
            long space3 = (long)n * n * 4;
            printf("Quadratic Time Space: %ld bytes\n", space3);
        } else {
            printf("Quadratic Time Space: Too big to run!\n");
        }

        printf("\n");
    }

    return 0;
}