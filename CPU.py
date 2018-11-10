from Memory import Mem
from Config import START_ADDRESS


class CPU:
    def __init__(self, start_address, mem):
        # Operation Code
        self.op_code = 0
        # Stack pointer
        self.sp = 0
        # Program stack
        self.stack = []
        # Program counter and Index register
        self.reg = {
            'I': 0,
            'PC': start_address
        }
        # V register
        self.v_reg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # CPU clock
        self.timer = {
            'delay': 0,
            'sound': 0
        }
        # Initialize memory
        self.mem = mem

    def emulate_cycle(self):
        # Fetch instruction
        self.op_code = self.mem.fetch_opcode(self.reg['PC'])
        # Decode ope_code

        # Execute ope_code

    # Operation Code 8XY0 ~ 8XYE
    def cpu_8xy(self):
        sec_opcode = self.op_code & 0x000F
        x = (self.op_code & 0x0F00) >> 8
        y = (self.op_code & 0x00F0) >> 4
        if sec_opcode == 0:
            self.v_reg[x] = self.v_reg[y]
        elif sec_opcode == 1:
            self.v_reg[x] = self.v_reg[x] | self.v_reg[y]
        elif sec_opcode == 2:
            self.v_reg[x] = self.v_reg[x] & self.v_reg[y]
        elif sec_opcode == 3:
            self.v_reg[x] = self.v_reg[x] ^ self.v_reg[y]
        elif sec_opcode == 4:
            self.v_reg[x] += self.v_reg[y]
            carry = self.v_reg[x] & 0xFF00
            if carry == 0:
                self.v_reg[0xF] = 0
            else:
                self.v_reg[0xF] = 1
                self.v_reg[x] &= 0x00FF
        elif sec_opcode == 5:
            self.v_reg[x] -= self.v_reg[y]
            borrow = self.v_reg[x] & 0xFF00
            if borrow == 0:
                self.v_reg[0xF] = 1
            else:
                self.v_reg[0xF] = 0
                self.v_reg[x] &= 0x00FF
        elif sec_opcode == 6:
            self.v_reg[0xF] = self.v_reg[x] & 0x01
            self.v_reg[x] >>= 1
        elif sec_opcode == 7:
            self.v_reg[x] = self.v_reg[y] - self.v_reg[x]
            borrow = self.v_reg[x] & 0xFF00
            if borrow == 0:
                self.v_reg[0xF] = 1
            else:
                self.v_reg[0xF] = 0
                self.v_reg[x] &= 0x00FF
        elif sec_opcode == 0xE:
            self.v_reg[0xF] = self.v_reg[x] & 0x80
            self.v_reg[x] <<= 1
        else:
            print "Unknown OpCode: " + str(self.op_code)

        self.reg['PC'] += 2

    # def cpu_annn(self):


    # def __str__(self):

