package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func min(a, b int64) int64 {
	if a <= b {
		return a
	}
	return b
}

func surfaceArea(h, w, l int64) int64 {
	return 2*h*w + 2*h*l + 2*w*l
}

func smallestSideArea(h, w, l int64) int64 {
	return min(min(h*w, h*l), w*l)
}

func smallestSidePerimeter(h, w, l int64) int64 {
	return min(min(2*h+2*w, 2*h+2*l), 2*w+2*l)
}

func volume(h, w, l int64) int64 {
	return h * w * l
}

func paper(h, w, l int64) int64 {
	return surfaceArea(h, w, l) + smallestSideArea(h, w, l)
}

func ribbon(h, w, l int64) int64 {
	return volume(h, w, l) + smallestSidePerimeter(h, w, l)
}

func main() {
	var total_paper int64 = 0
	var total_ribbon int64 = 0
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		//fmt.Println(scanner.Text())
		var dims = strings.Split(scanner.Text(), "x")
		h, _ := strconv.ParseInt(dims[0], 10, 0)
		w, _ := strconv.ParseInt(dims[1], 10, 0)
		l, _ := strconv.ParseInt(dims[2], 10, 0)
		total_paper += paper(h, w, l)
		total_ribbon += ribbon(h, w, l)
	}
	fmt.Println("Part 1:", total_paper)
	fmt.Println("Part 2:", total_ribbon)
}
