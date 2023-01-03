# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    # pick the optimum strategy to build robots, collect and spend resourses
    # for each blue print to maximize the geodes cracked in 24 minutes
    # each robot collects one resourse per minute
    # the singular robot factory can create 1 robot per minute if it has the resources
    # return sum of quality levels (blueprint id * geodes cracked in 24 minutes)
    result = 0
    blueprints = parse(lines)
    for blueprint in blueprints:
        geodes = max_geodes_cracked(blueprint, 24)
        result += geodes * blueprint["id"]
    return result


def part2(lines):
    return -1


def parse(lines):
    data = []
    for line in lines:
        line = (
            line.strip()
            .replace("Blueprint ", "")
            .replace(": Each ore robot costs ", ",")
        )
        line = line.replace(" ore. Each clay robot costs ", ",").replace(
            " ore. Each obsidian robot costs ", ","
        )
        line = (
            line.replace(" clay. Each geode robot costs ", ",")
            .replace("ore and ", ",")
            .replace(" obsidian.", "")
        )
        items = line.split(",")
        blueprint = {
            "id": int(items[0]),
            "ore": int(items[1]),
            "clay": int(items[2]),
            "obs": (int(items[3]), int(items[4])),
            "geo": (int(items[5]), int(items[6])),
        }
        print(blueprint)
        data.append(blueprint)
    return data


def max_geodes_cracked(blueprint, time):
    result = 0
    # assume 1 or each robot, how much ore and clay is required
    (ore1, obs) = blueprint["geo"]
    (ore2, clay) = blueprint["obs"]
    ore3 = blueprint["clay"]
    ore4 = blueprint["ore"]
    print("assume one of each robot")
    clay_time = ore3 + 1
    print("time to first clay: ore required", ore3, "+1 build =", clay_time, "minutes")
    obs_time = 1 + max(ore2 + ore3, clay_time + clay)
    print(
        "time to first obs: ore required:",
        ore2 + ore3,
        "clay required:",
        clay,
        "clay time:",
        clay_time + clay,
        "+buid",
        obs_time,
        "minutes",
    )
    geo_time = 1 + max(ore1 + ore2 + ore3, obs_time + obs)
    print(
        "time to first geo: ore required:",
        ore1 + ore2 + ore3,
        "obs required:",
        obs,
        "obs time:",
        obs_time + obs,
        "+buid",
        geo_time,
        "minutes",
    )
    for item in blueprint:
        result += len(item)
    return result


if __name__ == "__main__":
    lines = open("test.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
