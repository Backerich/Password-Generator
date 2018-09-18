import random as rn
import string
from enum import Enum
import sys
import os
from PIL import Image, ImageDraw


class Picker:
    list_of_ASCII = list(string.printable)

    def __init__(self):
        # Last ASCII signs are not really usefull
        del self.list_of_ASCII[-6:]

    def pick_random(self):
        try:
            random_choice = rn.choice(self.list_of_ASCII)
            self.list_of_ASCII.remove(random_choice)
        except IndexError:
            self.list_of_ASCII = list(string.printable)
            del self.list_of_ASCII[-6:]
            random_choice = rn.choice(self.list_of_ASCII)
            self.list_of_ASCII.remove(random_choice)
        return random_choice


class Single:
    def __init__(self, length):
        self.length = length

    def get_single_password(self):
        p = Picker()
        password = ""
        for i in range(self.length):
            # random_ascii = p.pick_random()
            password += p.pick_random()
        return password


class Card:
    def __init__(self, number_of_lines_horizontal = 0, number_of_lines_vertical = 0):
        self.list_of_ascii_uppercase = list(string.ascii_uppercase)
        self.list_of_digits = list(string.digits)
        self.number_of_lines_horizontal = number_of_lines_horizontal
        self.number_of_lines_vertical = number_of_lines_vertical

        self.rescale_list(len(string.ascii_uppercase), self.number_of_lines_horizontal, self.list_of_ascii_uppercase)
        self.rescale_list(len(string.digits), number_of_lines_vertical, self.list_of_digits)

    def rescale_list(self, ascii_number, number_of_lines, list_of_content):
        number_of_lines = number_of_lines
        if number_of_lines > ascii_number:
            number_of_lines = ascii_number
        n = ascii_number - number_of_lines
        if n != 0:
            del list_of_content[-n:]
        return list_of_content

    def data(self):
        field = []
        p = Picker()
        counter = 0
        self.list_of_ascii_uppercase.insert(0, "/")
        field.append(self.list_of_ascii_uppercase)
        for i in range(len(self.list_of_digits)):
            row = []
            for j in range(len(self.list_of_ascii_uppercase)-1):
                random_choice = p.pick_random()
                row.append(random_choice)
            row.insert(0, self.list_of_digits[counter])
            counter += 1
            field.append(row)
        counter = 0
        return field


class ImageCard:
    def __init__(self):
        self.image = self.make_image_card()

    def make_image_card(self):
        return Image.new("RGB", (512, 512), color="white")

    def draw_text(self):
        d = ImageDraw.Draw(self.image)
        array = [["A", "B", "C", "A"], ["A", "B", "C", "B"], ["A", "B", "C", "C"], ["A", "B", "C", "D"]]

        counter_column = 10
        for i in array:
            counter_row = 10
            for j in i:
                d.text((counter_row, counter_column), j, (73, 109, 137))
                counter_row += 10
            counter_row = 10
            counter_column += 10

    def save_image(self):
        self.image.save("test.png")

    def remove_old_image(self):
        image_path = "./test.png"
        if os.path.isfile(image_path):
            os.remove(image_path)


class MenuItem(Enum):
    SINGLE_CONSOLE = 1
    CARD_CONSOLE = 2
    IMAGE = 3


class OutOfRange(Exception):
    pass


class CommandLine:
    # menu_Items = MenuItem()

    def __init__(self):
        pass

    def menu(self):
        generate_type_choice = self.generate_type_choice()
        self.validate_choice(generate_type_choice)

    def generate_type_choice(self):
        clear()
        print("Bitte wähle einen Menüpunkt aus indem du die vorranstehende Zahl angibst.")
        print("(1). Generate Single Line Password.")
        print("(2). Generate Password Card.")
        print("(3). Generate Password Image.")

        return self.validate_input(MenuItem.SINGLE_CONSOLE.value, MenuItem.IMAGE.value)

    def card_line_choice(self):
        clear()
        print("Wie viele Reihen soll deine Passwort Karte haben? MAX: 26")
        number_of_rows = self.validate_input(1, 26)
        print("Wie viele Spalten soll deine Passwort Karte haben? MAX: 10")
        number_of_columns = self.validate_input(1, 10)

        return (number_of_rows, number_of_columns)

    def single_length_choice(self):
        clear()
        print("Wie lang soll dein Passwort sein?")
        length = self.validate_input(range=False)

        return length

    def validate_choice(self, menu_choice):
        if menu_choice == MenuItem.SINGLE_CONSOLE.value:
            self.create_single_console()
        elif menu_choice == MenuItem.CARD_CONSOLE.value:
            self.create_card_console()
        elif menu_choice == MenuItem.IMAGE.value:
            self.create_card_image()
        else:
            print("Command not found")

    # vlt. Validate Klasse
    def validate_input(self, min_range_number=1, max_range_number=1, range=True):
        while True:
            try:
                response = int(input("-> "))
                if range == True and response > max_range_number:
                    raise OutOfRange
                break
            except KeyboardInterrupt:
                exit()
            except ValueError:
                print("Please enter a number.")
            except OutOfRange:
                print("Please enter a value from "+ str(min_range_number) +"-"+ str(max_range_number) +".")

        return response

    def create_single_data(self):
        length = self.single_length_choice()
        s = Single(length)
        password = s.get_single_password()
        return password

    def create_single_console(self):
        password = self.create_single_data()
        clear()
        print("Your generated password is:" + "\n" + str(password))

    def create_card_data(self):
        number_of_lines = self.card_line_choice()
        c = Card(number_of_lines[0],number_of_lines[1])
        data = c.data()
        return data

    def create_card_console(self):
        data = self.create_card_data()
        number_of_lines_horizontal = len(data[0])

        clear()
        self.draw_line_comsole(number_of_lines_horizontal)
        for i in data:
            row_string = " ".join(i)
            print(row_string)
        self.draw_line_comsole(number_of_lines_horizontal)

    def create_card_image(self):
        data = self.create_card_data()
        i = ImageCard()
        i.remove_old_image()
        i.draw_text()
        i.save_image()

    def draw_line_comsole(self, number_of_lines_horizontal):
        print("--"*int(number_of_lines_horizontal+1))


def exit():
    return sys.exit()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    c = CommandLine()
    c.menu()

if __name__ == '__main__':
    main()
