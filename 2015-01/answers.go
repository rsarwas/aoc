package main

import (
	"bufio"
	"fmt"
	"os"
)

func what_floor(text string) int {
	floor := 0
	for i := 0; i < len(text); i++ {
		if text[i] == '(' {
			floor++
		}
		if text[i] == ')' {
			floor--
		}
	}
	return floor
}

func when_basement(text string) int {
	floor := 0
	for i := 0; i < len(text); i++ {
		if text[i] == '(' {
			floor++
		}
		if text[i] == ')' {
			floor--
		}
		if floor == -1 {
			return i + 1
		}
	}
	return -1
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		input := scanner.Text()
		fmt.Println("Part 1:", what_floor(input))
		fmt.Println("Part 2:", when_basement(input))
	}
}
