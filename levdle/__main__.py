from array import array


def distance(a, b, mx=-1):
    # from rosseta code
    def result(d):
        return d if mx < 0 else False if d > mx else True

    if a == b:
        return result(0)
    la, lb = len(a), len(b)
    if mx >= 0 and abs(la - lb) > mx:
        return result(mx + 1)
    if la == 0:
        return result(lb)
    if lb == 0:
        return result(la)
    if lb > la:
        a, b, la, lb = b, a, lb, la

    cost = array("i", range(lb + 1))
    for i in range(1, la + 1):
        cost[0] = i
        ls = i - 1
        mn = ls
        for j in range(1, lb + 1):
            ls, act = cost[j], ls + int(a[i - 1] != b[j - 1])
            cost[j] = min(ls + 1, cost[j - 1] + 1, act)
            if ls < mn:
                mn = ls
        if mx >= 0 and mn > mx:
            return result(mx + 1)
    if mx >= 0 and cost[lb] > mx:
        return result(mx + 1)
    return result(cost[lb])


import tty
import termios
import sys
import datetime
from typing import TextIO

WC = 9972



with open("data/words.txt", "r") as f:
    words = [ s.strip()  for s in f.readlines() ]



import random
from hashlib import sha1


class Game:
    def __init__(self, fin: TextIO, fout: TextIO):
        self.fin = fin
        self.fout = fout
        self.buffer = []
        self.tries = 6
        today = datetime.date.today().isoformat().encode("utf-8")
        idx = int(sha1(today).hexdigest(), 16) % WC
        self.word = words[idx]
        self.win = False

    def read(self):
        return self.fin.read(1)

    def show_buffer(self):
        self.fout.write("\033[99D")  # move left
        self.fout.write("\033[K")  # clear line
        self.fout.write(" ".join(self.buffer))
        self.fout.flush()

    def on_enter(self):
        done = False
        word = ''.join(self.buffer)
        if len(self.buffer) != 5 or word not in words:
            self.fout.write("\033[99D")  # move left
            self.fout.write("\033[K")  # clear line
            self.fout.write(" ".join(self.buffer))
            self.fout.write(" 🚨")
            self.fout.flush()
            return

        self.fout.write("\033[99D")  # move left
        self.fout.write("\033[K")  # clear line
        d = distance(word, self.word)
        if d == 0:
            self.fout.write("\033[32m" + " ".join(self.buffer) + "\033[0m")
            done = True
            self.win = True
        else:
            self.fout.write("\033[33m" + " ".join(self.buffer) + "\033[0m")
            self.fout.write(f" [\033[31;1m{d}\033[0m]")
            if self.tries == 1:
                return True
            else: 
                self.tries -= 1

        self.fout.write("\n")
        self.buffer.clear()
        self.fout.flush()
        return done

    def loop(self):
        while 1:
            c = self.read()
            if c == "":
                self.fout.write("\n")
                break
            elif ord(c) == 127:
                self.buffer.pop()
            elif ord(c) == 13:
                done = self.on_enter()
                if done:
                    break
                continue
            elif not c.isprintable():
                pass
                # print(ord(c))
            elif c.isalpha() and len(self.buffer) < 5:
                c = c.upper()
                self.buffer.append(c)
            self.show_buffer()

    def run(self):
        fd = self.fin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        try:
            self.loop()
        finally:
            pass
        self.fin.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if self.win:
            print(f"\033[99D🎉 You win! [{6 - self.tries + 1}/6]")
        else:
            print(f"\n💩 You lost...")


if __name__ == "__main__":
    repl = Game(sys.stdin, sys.stdout)
    repl.run()
