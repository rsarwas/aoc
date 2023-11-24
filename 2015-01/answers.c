#include <stdio.h>

int main()
{
    int floor = 0;
    int basement = -1;
    int position = 0;
    int c;
    while ((c = getchar()) != EOF)
    {
        floor += (c == '(') ? 1 : (c == ')') ? -1
                                             : 0;
        position++;
        if (floor == -1 && basement == -1)
            basement = position;
    }
    printf("Part 1: %d\n", floor);
    printf("Part 2: %d\n", basement);
    return 0;
}
