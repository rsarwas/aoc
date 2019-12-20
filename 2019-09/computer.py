class Computer:

    done = 0
    paused = 1

    def __init__(self, intcode):
        self.__code = list(intcode) # make a private copy
        self.__input = []
        self.__output = []
        self.__saved_ip = None
    
    def push_input(self, i):
        # i must be an int
        self.__input.append(i)

    def pop_output(self):
        if len(self.__output) > 0:
            return self.__output.pop()
        return None

    def start(self):
        self.__saved_ip = 0
        self.resume()

    def resume(self):
        self.__saved_ip = self.execute(self.__code, self.__saved_ip)
        return Computer.done if self.__saved_ip is None else Computer.paused
    
    """
        Opcode 1 add parameter 1 and parameter 2 and store the result in parameter 3
        Opcode 2 multiply parameter 1 and parameter 2 and store the result in parameter 3
        Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the instruction 3,50 would take an input value and store it at address 50.
        Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.
        Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    """
    def execute(self, intcode=[99], ip=0):
        #the ip is provide if this program is being "resumed" after a pause; otherwise it is a restart
        instruction,pm1,pm2 = parse(intcode[ip])
        while instruction != 99:
            if instruction == 1:
                ip = op3(ip,intcode,add, pm1, pm2)
            elif instruction == 2:
                ip = op3(ip,intcode,mul, pm1, pm2)
            elif instruction == 3:
                ok, ip = self.io('r', ip, intcode)
                if not ok:
                    return ip # May be zero, if this is the first instruction and it fails
            elif instruction == 4:
                ok, ip = self.io('w', ip, intcode, pm1)
            elif instruction == 5:
                ip = jump(ip,intcode,True, pm1, pm2)
            elif instruction == 6:
                ip = jump(ip,intcode,False, pm1, pm2)
            elif instruction == 7:
                ip = op3(ip,intcode,lt, pm1, pm2)
            elif instruction == 8:
                ip = op3(ip,intcode,eq, pm1, pm2)
            else:
                print(ip, instruction, pm1, pm2)
                raise NotImplementedError
            instruction,pm1,pm2 = parse(intcode[ip])
        return None

    # may return not OK (False) if there is nothing to read in the input queue
    # this is a signal to suspend this program.  The "OS" (calling code) can resume
    # it when there is input in the queue
    # only update the ip if the IO operation succeeded,
    # if it failed, we will use the old ip to retry the command
    def io(self, dir, ip, intcode, pm1=0):
        a1 = intcode[ip+1] if pm1 == 0 else ip+1
        if dir == 'r':
            if len(self.__input) == 0:
                return False, ip
            intcode[a1] = self.__input.pop()
        else:
            self.__output.append(intcode[a1])
        ip += 2
        return True, ip


def add(a,b):
    return a+b
    
def mul(a,b):
    return a*b

def lt(a,b):
    return 1 if a < b else 0

def eq(a,b):
    return 1 if a == b else 0

def op3(ip, intcode, fn, pm1=0, pm2=0):
    a1 = intcode[ip+1] if pm1 == 0 else ip+1
    a2 = intcode[ip+2] if pm2 == 0 else ip+2
    a3 = intcode[ip+3]
    ip += 4
    v1 = intcode[a1]
    v2 = intcode[a2]
    intcode[a3] = fn(v1, v2)
    return ip

def jump(ip, intcode, if_true, pm1=0, pm2=0):
    a1 = intcode[ip+1] if pm1 == 0 else ip+1
    a2 = intcode[ip+2] if pm2 == 0 else ip+2
    v1 = intcode[a1]
    v2 = intcode[a2]
    ip += 3
    # if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    # if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    if if_true:
        if v1 != 0:
            ip = v2
    else:
        if v1 == 0:
            ip = v2
    return ip

def parse(code):
    parameters = code // 100
    instruction = code % 100
    pm1 = parameters % 10
    parameters //= 10
    pm2 = parameters % 10
    # pm3 = parameters // 10
    return instruction, pm1, pm2
