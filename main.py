import random as rn
import string


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


class Card:
    list_of_ascii_uppercase = list(string.ascii_uppercase)
    list_of_digits = list(string.digits)

    def __init__(self, number_of_lines_horizontal = 0, number_of_lines_vertical = 0):
        self.number_of_lines_horizontal = number_of_lines_horizontal
        self.number_of_lines_vertical = number_of_lines_vertical

        self.rescale_list(len(string.ascii_uppercase), self.number_of_lines_horizontal, self.list_of_ascii_uppercase)
        self.rescale_list(len(string.digits), number_of_lines_vertical, self.list_of_digits)

    def rescale_list(self, ascii_number, number_of_lines, list_of_content):
        number_of_lines = number_of_lines
        print(list_of_content)
        if number_of_lines > ascii_number:
            number_of_lines = ascii_number
        n = ascii_number - number_of_lines
        if n != 0:
            del list_of_content[-n:]
        return list_of_content

    def field(self):
        field = []
        p = Picker()
        counter = 0
        # self.list_of_digits = list(string.digits)
        self.list_of_ascii_uppercase.insert(0, "/")
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

    # TODO: letztes "\n" entfernen damit in der Konsole schöner aussieht
    def print_card(self):
        field = self.field()

        print("--"*20)
        top_row = " ".join(self.list_of_ascii_uppercase)
        print(top_row)
        for i in field:
            row_string = " ".join(i)
            print(row_string)
        print("--"*20)


# class Generator:

# Höher als 25,9 geht nicht -> 9 und Z werden nicht angezeigt
def main():
    c = Card(26,10)
    c.print_card()

if __name__ == '__main__':
    main()
