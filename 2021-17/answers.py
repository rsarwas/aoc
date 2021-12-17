# Data Model:
# ===========
# data is text in the form: target area: x=20..30, y=-10..-5
# the numbers may differ: coordinates are x increase to right,
# y increase up, decrease down. launcher is at 0,0 

def part1(data):
    launcher = (0,0)
    target = parse(data)
    # the X velocity should be enough to be zero by the target
    # the x velocity goes to zero by one each step
    # with vxi = 5, x_max = 5 + 4 + 3 + 2 + 1 + 0 + 0 = tri(5)
    # find the x1 <= tri(x) <= x2; if vxi <= x then it will never get to the target
    # if x is greater, it may or may not hit the target, depending on the y component
    # if x is 0 at the target x distance, then shooting up it will have a -vyi and y = 0
    # vy = 4,3,2,1,0,-1,-2,-3,-4, and y = 0,4,7,9,10,10,9,7,4,0,-5,-6,...
    # ignore the part above the horizon for now. we want a maximum -vy after y = 0, that will
    # still hit target.  That will be the lower limit of the target.  vyi = -(y1+1).  The 1 is
    # because the first vy component below the horizon is one more than the the initial
    # velocity. i.e. if vyi = 10, then vy -10 before y=0 and vy=-11 below the horizon.
    # if ymin = -10, we want a vyi = 9
    vxi = initial_vx(target)
    vyi = initial_vy(target)
    vel = (vxi, vyi)
    # print(target)
    # print(vel)
    hit, ys = shoot((launcher, vel), target)
    max_y = max(ys)
    if not hit:
        print("Aak, we missed the target")
    return max_y

def part2(data):
    launcher = (0,0)
    target = parse(data)
    min_vx = initial_vx(target) # any velocity less than this will never get to the target
    max_vx = target[1] # x2 any velocity greater than this will miss the target on the first step
    min_vy = target[2] # y2 any velocity greater than this will miss the target on the first step
    max_vy = initial_vy(target)
    n = (max_vx - min_vx) * (max_vy - min_vy)
    # print("Trying x", min_vx, max_vx, "y", min_vy, max_vy, "n", n)
    hits = 0
    for vx in range(min_vx,max_vx+1):
        for vy in range(min_vy,max_vy+1):
               hit, _ = shoot((launcher, (vx,vy)), target)
               if hit: hits += 1
    return hits

def parse(data):
    data = data.strip().replace("target area: x=", "").replace(" y=", "")
    x,y = data.split(",")
    x1,x2 = x.split("..")
    y1,y2 = y.split("..")
    return (int(x1), int(x2), int(y1), int(y2))

def shoot(probe, target):
    loc, vel = probe
    ys = [loc[0]]
    while before(loc,target):
        loc, vel = update_probe(loc, vel)
        ys.append(loc[1])
        # print(loc)
        if within(loc, target):
            return True, ys
    return False, ys

def before(loc,target):
    x,y = loc
    _,x2,y1,_ = target
    return x < x2 and y > y1

def within(loc, target):
    x,y = loc
    x1,x2,y1,y2 = target
    if x1 <= x and x <= x2 and y1 <= y and y <= y2:
        return True
    return False

def update_probe(loc,vel):
    x, y = loc
    vx, vy = vel
    new_loc = (x + vx, y + vy) 
    if vx < 0:
        vx += 1
    elif vx > 0:
        vx -= 1
    vy -= 1
    return (new_loc, (vx,vy))

def initial_vx(target):
    x = 1
    vx = 1
    x1,x2,_,_ = target
    while x < x1:
        vx += 1
        x += vx
    return vx

def initial_vy(target):
    _,_,y1,_ = target
    return -(y1+1)

def test_part1():
    launcher = 0,0
    target = parse("target area: x=20..30, y=-10..-5")
    velocity = (7,2)
    hit = shoot((launcher,velocity), target)
    print(hit)
    velocity = (6,3)
    hit = shoot((launcher,velocity), target)
    print(hit)
    velocity = (9,0)
    hit = shoot((launcher,velocity), target)
    print(hit)
    velocity = (17,-4)
    hit = shoot((launcher,velocity), target)
    print(hit)

if __name__ == '__main__':
    # test_part1()
    # data = open("test.txt").read() # as one big string
    data = open("input.txt").read() # as one big string
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
