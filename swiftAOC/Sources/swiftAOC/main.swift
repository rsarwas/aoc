import AocLib

let problem = getProblemFromCmdLine()
let input = getLinesFromStdin()
let solution = problem.solveWith(data: input)
print("Advent of Code")
print("Problem: \(problem.name)")
print("Answer Part 1: \(solution.part1)")
print("Answer Part 2: \(solution.part2)")
