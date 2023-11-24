#include <stdio.h>

long min3l(long a, long b, long c) {
    long d = (a < b) ? a : b;
    return (d < c) ? d : c;
}

long surface_area(long h, long w, long l) {
	return 2*h*w + 2*h*l + 2*w*l;
}

long smallest_side_area(long h, long w, long l) {
	return min3l(h*w, h*l, w*l);
}

long smallest_side_perimeter(long h, long w, long l) {
	return min3l(2*h+2*w, 2*h+2*l, 2*w+2*l);
}

long volume(long h, long w, long l) {
    return h*w*l;
}

long ribbon(long h, long w, long l) {
    return volume(h, w, l) + smallest_side_perimeter(h, w, l);
}

long paper(long h, long w, long l) {
	return surface_area(h, w, l) + smallest_side_area(h, w, l);
}

int main() {
    long ribbon_total = 0;
    long paper_total = 0;
    int c;
    long d[3];
    int i = 0;
    d[0] = d[1] = d[2] = 0;
    while((c = getchar()) != EOF) {
        if (c == '\n') {
            if (i==2 & d[i] > 0) {
                paper_total += paper(d[0], d[1], d[2]);
                ribbon_total += ribbon(d[0], d[1], d[2]);
            }
            i = 0;
            d[0] = d[1] = d[2] = 0;
        }
        if (c == 'x') {
            i++;
        }
        if (c >= '0' && c <= '9') {
            d[i] = d[i] * 10 + (c - '0');
        }
    }
    printf("Part 1: %lu\n", paper_total);
    printf("Part 2: %lu\n", ribbon_total);
   return 0;
}
