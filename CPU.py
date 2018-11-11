from Memory import Mem
from Config import START_ADDRESS
import random


class CPU:
    def __init__(self, start_address, mem):
        # Operation Code
        self.op_code = 0
        # Stack pointer
        self.sp = 0
        # Program stack
        self.stack = [0] * 24
        # Graphics pixel array
        self.gfx = [0] * 2048
        # Key array
        self.key = [0] * 16
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
        # Draw flag
        self.draw_flag = False

    def emulate_cycle(self):
        # Fetch instruction
        self.op_code = self.mem.fetch_opcode(self.reg['PC'])
        # Decode ope_code
        opc = (self.op_code & 0xF000) >> 12
        # Execute ope_code
        if opc == 0:
            self.cpu_0nnn()
        elif opc == 1:
            self.cpu_1nnn()
        elif opc == 2:
            self.cpu_2nnn()
        elif opc == 3:
            self.cpu_3xnn()
        elif opc == 4:
            self.cpu_4xnn()
        elif opc == 5:
            self.cpu_5xy0()
        elif opc == 6:
            self.cpu_6xnn()
        elif opc == 7:
            self.cpu_7xnn()
        elif opc == 8:
            self.cpu_8xy()
        elif opc == 9:
            self.cpu_9xy0()
        elif opc == 0xA:
            self.cpu_annn()
        elif opc == 0xB:
            self.cpu_bnnn()
        elif opc == 0xC:
            self.cpu_cxnn()
        elif opc == 0xD:
            self.cpu_dxyn()
        elif opc == 0xE:
            self.cpu_ex()
        elif opc == 0xF:
            self.cpu_fx()
        else:
            print "Unknown OpCode: " + str(self.op_code)
        # Update timers
        if self.timer['delay'] > 0:
            self.timer['delay'] -= 1
        if self.timer['sound'] > 0:
            self.timer['sound'] -= 1

    # Instruction 0NNN
    def cpu_0nnn(self):
        if self.op_code == 0x00E0:
            self.gfx = [0] * 2048
            self.draw_flag = True
            self.reg['PC'] += 2
        elif self.op_code == 0x00EE:
            self.sp -= 1
            self.reg['PC'] = self.stack[self.sp] + 2
        else:
            self.reg['PC'] = self.op_code & 0x0FFF

    # Instruction 1NNN
    def cpu_1nnn(self):
        self.reg['PC'] = self.op_code & 0x0FFF

    # Instruction 2NNN
    def cpu_2nnn(self):
        self.stack[self.sp] = self.reg['PC']
        self.sp += 1
        self.reg['PC'] = self.op_code & 0x0FFF

    # Instruction 3XNN
    def cpu_3xnn(self):
        x = (self.op_code & 0x0F00) >> 8
        if self.v_reg[x] == (self.op_code & 0x00FF):
            self.reg['PC'] += 4
        else:
            self.reg['PC'] += 2

    # Instruction 4XNN
    def cpu_4xnn(self):
        x = (self.op_code & 0x0F00) >> 8
        if self.v_reg[x] != (self.op_code & 0x00FF):
            self.reg['PC'] += 4
        else:
            self.reg['PC'] += 2

    # Instruction 5XY0
    def cpu_5xy0(self):
        x = (self.op_code & 0x0F00) >> 8
        y = (self.op_code & 0x00F0) >> 4
        if self.v_reg[x] == self.v_reg[y]:
            self.reg['PC'] += 4
        else:
            self.reg['PC'] += 2

    # Instruction 6XNN
    def cpu_6xnn(self):
        x = (self.op_code & 0x0F00) >> 8
        self.v_reg[x] = (self.op_code & 0x00FF)
        self.reg['PC'] += 2

    # Instruction 7XNN
    def cpu_7xnn(self):
        x = (self.op_code & 0x0F00) >> 8
        self.v_reg[x] = ((self.op_code & 0x00FF) + self.v_reg[x]) & 0x00FF
        self.reg['PC'] += 2

    # Instruction 8XY0 ~ 8XYE
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

    # Instruction 9XY0
    def cpu_9xy0(self):
        x = (self.op_code & 0x0F00) >> 8
        y = (self.op_code & 0x00F0) >> 4
        if self.v_reg[x] != self.v_reg[y]:
            self.reg['PC'] += 4
        else:
            self.reg['PC'] += 2

    # Instruction ANNN
    def cpu_annn(self):
        self.reg['I'] = self.op_code & 0x0FFF
        self.reg['PC'] += 2

    # Instruction BNNN
    def cpu_bnnn(self):
        self.reg['PC'] = self.op_code & 0x0FFF + self.v_reg[0x0]

    # Instruction CXNN
    def cpu_cxnn(self):
        x = (self.op_code & 0x0F00) >> 8
        val_nn = self.op_code & 0x00FF
        self.v_reg[x] = random.randint(0, 255) & val_nn
        self.reg['PC'] += 2

    # Instruction DXYN
    def cpu_dxyn(self):
        x = (self.op_code & 0x0F00) >> 8
        y = (self.op_code & 0x00F0) >> 4
        x_val = self.v_reg[x]
        y_val = self.v_reg[y]
        height = self.op_code & 0x000F
        self.v_reg[0xF] = 0
        for yline in range(0, height):
            pixel = self.mem.load_byte(self.reg['I'] + yline)
            for xline in range(0, 8):
                if pixel & (0x80 >> xline) != 0:
                    if self.gfx[x_val + xline + (y_val + yline) * 64] == 1:
                        self.v_reg[0xF] = 1
                    self.gfx[x_val + xline + (y_val + yline) * 64] ^= 1
        self.draw_flag = True
        self.reg['PC'] += 2

    # Instruction EX9E~EXA1
    def cpu_ex(self):
        x = (self.op_code & 0x0F00) >> 8
        sec_opcode = self.op_code & 0x00FF
        if sec_opcode == 0x9E:
            if self.key[self.v_reg[x]] != 0:
                self.reg['PC'] += 2
        elif sec_opcode == 0xA1:
            if self.key[self.v_reg[x]] == 0:
                self.reg['PC'] += 2
        else:
            print "Unknown OpCode: " + str(self.op_code)
        self.reg['PC'] += 2

    # Instruction FX07~FX65
    def cpu_fx(self):
        x = (self.op_code & 0x0F00) >> 8
        sec_opcode = self.op_code & 0x00FF
        if sec_opcode == 0x07:
            self.v_reg[x] = self.timer['delay']
        elif sec_opcode == 0x0A:
            self.v_reg[x] = self.timer['sound']
        elif sec_opcode == 0x15:
            self.timer['delay'] = self.v_reg[x]
        elif sec_opcode == 0x18:
            self.timer['sound'] = self.v_reg[x]
        elif sec_opcode == 0x1E:
            self.reg['I'] += self.v_reg[x]
            if self.reg['I'] > 0xFFF:
                self.v_reg[0xF] = 1
                self.reg['I'] &= 0xFFF
            else:
                self.v_reg[0xF] = 0
        elif sec_opcode == 0x29:
            self.reg['I'] = self.v_reg[x] * 5
        elif sec_opcode == 0x33:
            self.mem.store_byte(self.reg['I'], self.v_reg[x] / 100)
            self.mem.store_byte(self.reg['I'] + 1, self.v_reg[x] / 10 % 10)
            self.mem.store_byte(self.reg['I'] + 2, self.v_reg[x] % 100 % 10)
        elif sec_opcode == 0x55:
            for i in range(x + 1):
                self.mem.store_byte(self.v_reg[i], self.reg['I'] + i)
        elif sec_opcode == 0x65:
            for i in range(x + 1):
                self.v_reg[i] = self.mem.load_byte(self.reg['I'] + i)
        else:
            print "Unknown OpCode: " + str(self.op_code)
        self.reg['PC'] += 2

    def __str__(self):
        ret = 'Current Instruction: ' + str(hex(self.op_code)).upper()\
              + '\nPC: ' + str(hex(self.reg['PC'])).upper() + '\nI Register: '\
              + str(hex(self.reg['I'])).upper() + '\nStack: '\
              + str(hex(self.stack[self.sp])).upper() + '\nV Register: '
        regs = ''
        for i in range(len(self.v_reg)):
            regs += ' V' + str(i) + ': ' + str(hex(self.v_reg[i])).upper()
        ret += regs + '\n'
        return ret
