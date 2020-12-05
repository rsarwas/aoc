using System;
using System.Collections.Generic;

namespace dotnetAOC
{
    class Program
    {
        static void Main(string[] args)
        {
            var input = GetLinesFromStdin();
            var problem = GetProblem(args);
            var solution = problem.SolveWith(input);
            Console.WriteLine("Advent of Code");
            if (solution == null) {
                Console.WriteLine("No recognized problem specified on command line");
            } else {
                Console.WriteLine($"Problem: {problem.Name}");
                Console.WriteLine($"Answer Part 1: {solution.Part1}");
                Console.WriteLine($"Answer Part 2: {solution.Part2}");
            }
        }

        static IEnumerable<String> GetLinesFromStdin() {
            var results = new List<String>();
            String line;
            while ((line = Console.ReadLine()) != null) {
                results.Add(line.TrimEnd());
            }
            return results;
        }

        static Problem GetProblem(string[] args) {
            if (args.Length < 2) {
                return new Problem("");
            } else {
                return new Problem(args[1]);
            }
        }
    }

    struct Problem {
        public Problem(string name) {
            Name = name;
        }
        public String Name { get; }
        public Solution SolveWith(IEnumerable<String> data) {
            switch (Name)
            {
                case "2020-01": {
                    return new Solution202001(data);
                }
                default: { return null; }
            }
        }

    }

    interface Solution {

        String Part1 { get; }
        String Part2 { get; }
    }

    struct Solution202001: Solution {
        public Solution202001(IEnumerable<String> data) {
            Data = data;
        }
        private IEnumerable<String> Data { get; set; }

        public String Part1 {
            get {
                //return "Not Implemented";
                return $"{Answer1}";
            }
        }

        public String Part2 {
            get {
                return "Not Implemented";
                //return $"{Answer2}";
            }
        }

        int Answer1 {
            get {
                return -1;
            }
        }

        int Answer2 {
            get {
                return -1;
            }
        }
    }
}
