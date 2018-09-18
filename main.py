import random as rn
import string
from enum import Enum
import sys
import os
from PIL import Image, ImageDraw


class OutOfRange(Exception):
    pass


class Utils:
    def exit(self):
        return sys.exit()

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")


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

    def data(self):
        p = Picker()
        # password = ""
        data = []
        password = []
        for i in range(self.length):
            # password += p.pick_random()
            password.append(p.pick_random())
        data.append(password)
        return data


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
        data = []
        p = Picker()
        counter = 0
        self.list_of_ascii_uppercase.insert(0, "/")
        data.append(self.list_of_ascii_uppercase)
        for i in range(len(self.list_of_digits)):
            row = []
            for j in range(len(self.list_of_ascii_uppercase)-1):
                random_choice = p.pick_random()
                row.append(random_choice)
            row.insert(0, self.list_of_digits[counter])
            counter += 1
            data.append(row)
        counter = 0
        return data


class ImageMaker: # ImageMaker
    def __init__(self, data=[]):
        self.data = data
        self.image = self.make_image()
        self.remove_old_image()

    def get_size(self):
        row_length = len(self.data[0])
        column_length = len(self.data)

        row_size = 20 + (row_length*10)
        column_size = 20 + (column_length*10)
        return (row_size, column_size)

    def make_image(self):
        size = self.get_size()
        return Image.new("RGB", size, color="white") # (290, 130)

    def draw_text(self):
        d = ImageDraw.Draw(self.image)

        counter_column = 10
        for i in self.data:
            counter_row = 10
            for j in i:
                d.text((counter_row, counter_column), j, (73, 109, 137))
                counter_row += 10
            counter_row = 10
            counter_column += 10

    def remove_old_image(self):
        image_path = "./test.png"
        if os.path.isfile(image_path):
            os.remove(image_path)

    def save_image(self):
        self.image.save("test.png")


class MenuItem(Enum):
    SINGLE_CONSOLE = 1
    CARD_CONSOLE = 2
    SINGLE_IMAGE = 3
    CARD_IMAGE = 4


class Validate:
    def validate_choice(self, menu_choice):
        if menu_choice == MenuItem.SINGLE_CONSOLE.value:
            self.create_single_console()
        elif menu_choice == MenuItem.CARD_CONSOLE.value:
            self.create_card_console()
        elif menu_choice == MenuItem.SINGLE_IMAGE.value:
            self.create_single_image()
        elif menu_choice == MenuItem.CARD_IMAGE.value:
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
                self.exit()
            except ValueError:
                print("Please enter a number.")
            except OutOfRange:
                print("Please enter a value from "+ str(min_range_number) +"-"+ str(max_range_number) +".")

        return response


class CommandLine(Utils, Validate):
    def __init__(self):
        pass

    def menu(self):
        generate_type_choice = self.generate_type_choice()
        self.validate_choice(generate_type_choice)

    def generate_type_choice(self):
        self.clear()
        print("Bitte wähle einen Menüpunkt aus indem du die vorranstehende Zahl angibst.")
        print("(1). Generate Single Line Password.")
        print("(2). Generate Password Card.")
        print("(3). Generate Single Line Password Image.")
        print("(4). Generate Password Card Image.")

        return self.validate_input(MenuItem.SINGLE_CONSOLE.value, MenuItem.CARD_IMAGE.value)

    def card_line_choice(self):
        self.clear()
        print("Wie viele Reihen soll deine Passwort Karte haben? MAX: 26")
        number_of_rows = self.validate_input(range=False)
        print("Wie viele Spalten soll deine Passwort Karte haben? MAX: 10")
        number_of_columns = self.validate_input(range=False)

        return (number_of_rows, number_of_columns)

    def single_length_choice(self):
        self.clear()
        print("Wie lang soll dein Passwort sein?")
        length = self.validate_input(range=False)

        return length

    def create_single_data(self):
        length = self.single_length_choice()
        s = Single(length)
        data = s.data()
        return data

    def create_single_console(self):
        data = self.create_single_data()
        password = "".join(data[0])
        self.clear()
        print("Your generated password is:" + "\n" + str(password))

    def create_single_image(self):
        data = self.create_single_data()
        i = ImageMaker(data=data)
        i.draw_text()
        i.save_image()

    def create_card_data(self):
        number_of_lines = self.card_line_choice()
        c = Card(number_of_lines[0],number_of_lines[1])
        data = c.data()
        return data

    def create_card_console(self):
        data = self.create_card_data()
        number_of_lines_horizontal = len(data[0])

        self.clear()
        self.draw_line_comsole(number_of_lines_horizontal)
        for i in data:
            row_string = " ".join(i)
            print(row_string)
        self.draw_line_comsole(number_of_lines_horizontal)

    def create_card_image(self):
        data = self.create_card_data()
        i = ImageMaker(data=data)
        i.draw_text()
        i.save_image()

    def draw_line_comsole(self, number_of_lines_horizontal):
        print("--"*int(number_of_lines_horizontal))


def main():
    c = CommandLine()
    c.menu()

if __name__ == '__main__':
    main()
