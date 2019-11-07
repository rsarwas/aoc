using System;
using System.Linq;

namespace Aoc
{
    internal struct Present
    {
        private uint h,w,l;

        internal Present(uint height, uint width, uint length)
        {
            h = height;
            w = width;
            l = length;
        }

        static private uint Min3(uint a, uint b, uint c)
        {
            uint d = (a < b) ? a : b;
            return (d < c) ? d : c;
        }

        private uint SmallestSidePerimeter => Min3(2*h+2*w, 2*h+2*l, 2*w+2*l);

        private uint SmallestSideArea => Min3(h*w, h*l, w*l);

        private uint SurfaceArea => 2*h*w + 2*h*l + 2*w*l;

        private uint Volume => h*w*l;

        public uint Ribbon => Volume + SmallestSidePerimeter;

        public uint Paper => SurfaceArea + SmallestSideArea;
    }

    class Program
    {
        static void Main(String[] args)
        {
            String line;
            uint ribbon = 0;
            uint paper = 0;
            while ((line = Console.ReadLine()) != null) {
                var dims = line.Split('x').Select(s => UInt32.Parse(s)).ToArray();
                Present p = new Present(height:dims[0], width:dims[1], length:dims[2]);
                ribbon += p.Ribbon;
                paper += p.Paper;
            }
            Console.WriteLine("Part1: {0}", paper);
            Console.WriteLine("Part2: {0}", ribbon);
        }
    }
}