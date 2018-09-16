import random as rn
import string

class Picker:
    lsit_of_ASCII = list(string.printable)

    def __init__(self):
        # Last ASCII signs are not really usefull
        del self.lsit_of_ASCII[-6:]

    def pick_random(self):
        random_choice = rn.choice(self.lsit_of_ASCII)
        self.lsit_of_ASCII.remove(random_choice)
        return random_choice


def main():
    p = Picker()
    print(p.pick_random())
    print(p.pick_random())

if __name__ == '__main__':
    main()
