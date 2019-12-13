using System;
using System.Collections.Generic;
using System.Linq;

namespace Aoc
{
    internal class Moon
    {
        private int vx,vy,vz;

        internal Moon(int x, int y, int z)
        {
            X = x;
            Y = y;
            Z = z;
            vx = 0;
            vy = 0;
            vz = 0;
        }

        public void ApplyGravity(Moon other)
        {
            vx += (X < other.X) ? 1 : (X > other.X) ? -1 : 0;
            vy += (Y < other.Y) ? 1 : (Y > other.Y) ? -1 : 0;
            vz += (Z < other.Z) ? 1 : (Z > other.Z) ? -1 : 0;
        }

        public void UpdateLocation()
        {
            X += vx;
            Y += vy;
            Z += vz;
        }
        public int X { get; private set; }
        public int Y { get; private set; }
        public int Z { get; private set; }
        public int TotalEnergy => PotentialEnergy * KineticEnergy;

        private int PotentialEnergy => Math.Abs(X) + Math.Abs(Y) + Math.Abs(Z);

        private int KineticEnergy => Math.Abs(vx) + Math.Abs(vy) + Math.Abs(vz);
    }

    class Program
    {

        static private int total_energy(List<Moon> moons, int steps)
        {
            var n = moons.Count;
            for (int t = 0; t < steps; t++)  {
                for (int i = 0; i < n; i++)
                {
                    for (int j = 0; j < n; j++)
                    {
                        if (i == j) continue;
                        moons[i].ApplyGravity(moons[j]);
                    }
                }
                foreach (Moon moon in moons)
                {
                    moon.UpdateLocation();
                }
            }
            var total = 0;
            foreach (Moon moon in moons)
            {
                total += moon.TotalEnergy;
            }
            return total;
        }

        static private void test1()
        {
            List<Moon> moons = new List<Moon>
            {
                new Moon(-1,  0, 2),
                new Moon( 2,-10,-7),
                new Moon( 4, -8, 8),
                new Moon( 3,  5,-1)
            };
            var answer = total_energy(moons, 10);
            Console.WriteLine("Test 1: {0}", answer);
        }
        static private void test2()
        {
            List<Moon> moons = new List<Moon>
            {
                new Moon(-8,-10, 0),
                new Moon( 5,  5,10),
                new Moon( 2, -7, 3),
                new Moon( 9, -8,-3)
            };
            var answer = total_energy(moons, 100);
            Console.WriteLine("Test 2: {0}", answer);
        }
        static private void part1()
        {
            List<Moon> moons = new List<Moon>
            {
                new Moon( 6,-2, -7),
                new Moon(-6, -7,-4),
                new Moon(-9, 11, 0),
                new Moon(-3, -4, 6)
            };
            var answer = total_energy(moons, 1000);
            Console.WriteLine("Part1: {0}", answer);
        }
        static void Main(String[] args)
        {
            test1();
            test2();
            part1();
        }
    }
}