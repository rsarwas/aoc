#include <stdio.h>

int main() {
    int nums[1000];
    int length = 0;
    int *p = nums;

    while (EOF != scanf("%d", p)) {
        p++;
        length++;
    }

    // printf("length: %d\n", length);
    // for (int i = 0; i < length; i++) {
    //     printf("%d\n", nums[i]);
    // }

    for (int i = 0; i < length-1; i++) {
        for (int j = i + 1; j < length; j++) {
            if (nums[i] + nums[j] == 2020) {
                printf("part 1: %d\n", nums[i]*nums[j]);
                i = length;  // break out of all loops
                break;
            }
        }
    }

    for (int i = 0; i < length-2; i++) {
        for (int j = i + 1; j < length-1; j++) {
            for (int k = j + 1; k < length; k++) {
                if (nums[i] + nums[j] + nums[k] == 2020) {
                    printf("part 2: %d\n", nums[i]*nums[j]*nums[k]);
                    i = length; // break out of all loops
                    j = length;
                    break;
                }
            }
        }
    }
}