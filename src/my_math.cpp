#include <stdlib.h>

int sum(int a, int b)
{
    int* leak = (int*)malloc(sizeof(int));
    return a;
}