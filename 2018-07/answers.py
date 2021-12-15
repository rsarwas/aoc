# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# each line describes an edge in a directed graph. 
# Nodes is a set of single letters; they appear to be in the set {A..Z}
# Edges is a set of (char, char) tuples where each char is in Nodes
#  the first char is the starting node, and the other is the end node
# predecessors is a dictionary with nodes as keys and a list of nodes
# that must be done before this node can execute (the list is only
# the nodes connected to the key node.)
# 

def part1(lines):
    nodes, edges = parse(lines)
    # print(nodes, edges)
    predecessors = make_predecessors(nodes, edges)
    # print(predecessors)
    task_order = order_tasks(predecessors, nodes)
    return "".join(task_order)

def part2(lines):
    nodes, edges = parse(lines)
    # print(nodes, edges)
    predecessors = make_predecessors(nodes, edges)
    # print(predecessors)
    task_time = time_tasks(predecessors, nodes)
    return task_time

def parse(lines):
    nodes = set()
    edges = set()
    for line in lines:
        n1, n2 = line[5], line[36]
        nodes.add(n1)
        nodes.add(n2)
        edges.add((n1,n2))
    return nodes, edges

def make_predecessors(nodes, edges):
    predecessors = {}
    for node in nodes:
        if node not in predecessors:
            predecessors[node] = []
        for edge in edges:
            start,end = edge
            if end == node:
                predecessors[node].append(start)
    return predecessors

def order_tasks(predecessors, nodes):
    # returns a list of nodes in a valid order of execution
    # A task can only be added to the list when it has no predesessors
    # If multiple tasks can be done at the same time, the go alphabetically
    # IMPORTANT: the predecessor list should be updated, and new list of
    # candidates selected after each task is added to the task list.
    # i.e. if A and F are ready, then A is added to tasks.  If A frees up
    # task D, that will be done before task F.
    tasks = []
    undone = set(nodes)
    while undone:
        ready = find_ready(predecessors, undone)
        # print("tasks", tasks)
        # print("undone", undone)
        # print("predecessors", predecessors)
        # print("ready", ready, "\n")
        if not ready:
            print("PANIC - there is no ready node")
            break
        ready.sort()
        node = ready[0]
        tasks.append(node)
        undone.remove(node)
        remove(node, predecessors)
    return tasks

def time_tasks(predecessors, nodes):
    # execute the tasks with a number of workers. task A takes 1 + base
    # seconds to complete. B takes 2 + base, while Z take 26+base.
    # At time zero, give each worker a ready task. (not all workers may
    # get a task, and some tasks may not get started).  When a task is
    # completed, get a new list of ready tasks, and start as many as possible.
    # the key in assignments is a (worker_id, task) tuple, and the value is the
    # time remaining until complete. worker_ids are the numbers 0..NUM_WORKERS-1
    # completed_tasks = [] # no need to keep track of the order of the completed tasks
    # completed_tasks is nodes - undone if needed.
    assignments = {}
    undone = set(nodes)
    available_workers = list(range(0,NUM_WORKERS))
    seconds = 0
    while undone:
        # print("undone", undone)
        # print("predecessors", predecessors)
        ready_tasks = find_ready(predecessors, undone)
        ready_tasks = remove_assigned(ready_tasks, assignments)
        ready_tasks.sort()
        assignments |= assign_tasks(available_workers, ready_tasks) # |= merge dict in Python 3.9
        # print("assignments", assignments)
        # print("available_workers", available_workers)
        # print("seconds", seconds)
        # print("ready", ready, "\n")
        wait = time_until_next_task_is_complete(assignments)
        finished = update(assignments, wait)
        #print("wait", wait)
        #print("finished", finished)
        seconds += wait
        for (worker_id,task) in finished:
            available_workers.append(worker_id)
            undone.remove(task)
            remove(task, predecessors)
    return seconds

def remove_assigned(ready_tasks, assignments):
    assigned = [t for (_,t) in assignments.keys()]
    for a in assigned:
        if a in ready_tasks:
            ready_tasks.remove(a)
    return ready_tasks

def assign_tasks(available_workers, ready_tasks):
    # assigns ready tasks to available workers
    # and creates a list of assignments (dictionary (worker_id: task))
    # if ready list is short, not all workers may get a task
    # if ready list is long, not all tasks will get assigned to a worker
    new_assignments = {}
    # print("   available_workers", available_workers)
    # print("   ready_tasks", ready_tasks)
    in_labor = []  # do not delete from available_workers until the zip is done
    for item in zip(available_workers, ready_tasks):
        worker, task = item
        # print("   assign", worker, "to", task)
        in_labor.append(worker)
        new_assignments[item] = time_to_complete(task)
    for worker in in_labor:
        available_workers.remove(worker)
    return new_assignments

def time_to_complete(task):
    # 'A' = 1, 'B' = 2, ... 'Z' = 26
    return ord(task) - ord("A") + 1 + BASE_TASK_TIME

def update(assignments, wait):
    ready = []
    for item in assignments.keys():
        assignments[item] -= wait
        if assignments[item] == 0:
            ready.append(item)
    for item in ready:
        del assignments[item]
    return ready
    
def time_until_next_task_is_complete(assignments):
    # return the length of the shortest task underway
    return min(assignments.values())

def find_ready(predecessors, undone):
    # return keys (nodes) from predecessors that have no predecessors
    # i.e. and empty list in values, and are still in the set
    # of undone tasks (nodes)
    ready = []
    for node in undone:
        p_list = predecessors[node]
        if not p_list:
            ready.append(node)
    return ready

def remove(node, predecessors):
    # mutates predecessors by removing node from any predecessor lists
    # as an item in predecessors has an empty list it is ready to execute
    for _, p_list in predecessors.items():
        if node in p_list:
            p_list.remove(node)

NUM_WORKERS = 5 # use 2 for test/sample case; 5 for puzzle
BASE_TASK_TIME = 60 # use 0 for test/sample case; 60 for puzzle

if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
