using System;

namespace Aoc
{
    internal struct FloorCounter
    {
        public string Text { get; set; }
        public int FinalFloor
        {
            get
            {
                int floor = 0;
                foreach (char c in Text)
                {
                    if (c == '(') { floor += 1; }
                    if (c == ')') { floor -= 1; }
                }
                return floor;
            }
        }
        public int StepsToBasement
        {
            get
            {
                int floor = 0;
                int steps = 0;
                foreach (char c in Text)
                {
                    steps += 1;
                    if (c == '(') { floor += 1; }
                    if (c == ')') { floor -= 1; }
                    if (floor == -1) { return steps; }
                }
                return -1;
            }
        }
    }

    class Program
    {
        static void Main(String[] args)
        {
            String line = Console.ReadLine();
            var counter = new FloorCounter { Text = line };
            Console.WriteLine("Part1: {0}", counter.FinalFloor);
            Console.WriteLine("Part2: {0}", counter.StepsToBasement);
        }
    }
}