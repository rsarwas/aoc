using System;
using System.Collections.Generic;
using System.Linq;

namespace dotnetAOC
{
    struct Solution202001 : Solution
    {
        public Solution202001(IEnumerable<String> data)
        {
            Data = data;
        }
        private IEnumerable<String> Data { get; set; }

        public String Part1
        {
            get
            {
                return $"{Answer1}";
            }
        }

        public String Part2
        {
            get
            {
                return $"{Answer2}";
            }
        }

        int Answer1
        {
            get
            {
                var diffs = new HashSet<int>();
                var nums = Data.Select(x => int.Parse(x));
                foreach (var num in nums)
                {
                    var diff = 2020 - num;
                    if (diffs.Contains(diff))
                    {
                        return diff * num;
                    }
                    else
                    {
                        diffs.Add(num);
                    }
                }
                return -1;
            }
        }

        int Answer2
        {
            get
            {
                var nums = Data.Select(x => int.Parse(x)).ToArray();
                for (int i = 0; i < nums.Length - 2; i++)
                {
                    for (int j = i + 1; j < nums.Length - 1; j++)
                    {
                        for (int k = j + 1; k < nums.Length; k++)
                        {
                            if (nums[i] + nums[j] + nums[k] == 2020)
                            {
                                return nums[i] * nums[j] * nums[k];
                            }
                        }
                    }
                }
                return -1;
            }
        }
    }
}
