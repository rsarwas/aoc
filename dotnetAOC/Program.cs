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
            if (solution == null)
            {
                Console.WriteLine("No recognized problem specified on command line");
            }
            else
            {
                Console.WriteLine($"Problem: {problem.Name}");
                Console.WriteLine($"Answer Part 1: {solution.Part1}");
                Console.WriteLine($"Answer Part 2: {solution.Part2}");
            }
        }

        static IEnumerable<String> GetLinesFromStdin()
        {
            var results = new List<String>();
            String line;
            while ((line = Console.ReadLine()) != null)
            {
                results.Add(line.TrimEnd());
            }
            return results;
        }

        static Problem GetProblem(string[] args)
        {
            if (args.Length != 1)
            {
                return new Problem("");
            }
            else
            {
                return new Problem(args[0]);
            }
        }
    }

    struct Problem
    {
        public Problem(string name)
        {
            Name = name;
        }
        public String Name { get; }
        public Solution SolveWith(IEnumerable<String> data)
        {
            switch (Name)
            {
                case "2020-01": { return new Solution202001(data); }
                case "2020-05": { return new Solution202005(data); }
                default: { return null; }
            }
        }

    }

    interface Solution
    {

        String Part1 { get; }
        String Part2 { get; }
    }

}
