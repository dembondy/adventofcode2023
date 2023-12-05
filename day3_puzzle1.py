import numpy as np


class Number:
    def __init__(self, number, x, y):
        self.number = number
        self.position = (x, y)
        self.adjacent_numbers = []
        self.is_adjacent_to_symbol = False
        self.accounted_for_in_number_group = False
        self.is_adjacent_to_gear = False

    def __repr__(self):
        if self.is_adjacent_to_symbol:
            return f"{self.number}*"
        return f"{self.number}"

    def check_for_symbol_adjacency(self, matrix):
        x = self.position[0]
        y = self.position[1]
        for coordinate in self.adjacent_coordinates:
            self.check_coordinate(matrix, coordinate)

    @property
    def adjacent_coordinates(self) -> list:
        x = self.position[0]
        y = self.position[1]
        return generate_adjacent_coordinates(x, y)

    def check_coordinate(self, matrix, coordinate):
        try:
            if is_symbol(matrix[coordinate[1], coordinate[0]]):
                self.is_adjacent_to_symbol = True
        except IndexError:
            pass


class NumberGroup:
    def __init__(self, list_of_numbers: list):
        self.numbers = list_of_numbers
        self.accounted_for_in_final_tally = False

    def __repr__(self):
        return f"{self.value}"

    @property
    def is_relevant(self) -> bool:
        for number in self.numbers:
            if number.is_adjacent_to_symbol:
                return True
        return False

    @property
    def value(self) -> int:
        positions = []
        value = ""
        for number in self.numbers:
            positions.append(number.position[0])
        sorted_positions = sorted(positions)
        for position in positions:
            for number in self.numbers:
                if number.position[0] == position:
                    value += str(number.number)
        return int(value)

    @property
    def may_be_gear(self) -> bool:
        for number in self.numbers:
            if number.is_adjacent_to_gear:
                return True
        return False

    def is_number_in_group(self, number: Number) -> bool:
        return number in self.numbers


class Gear:
    def __init__(self, x, y):
        self.position = (x, y)
        self.adjacent_numbers = []

    def __repr__(self):
        return "⚙️"

    @property
    def adjacent_coordinates(self) -> list:
        x = self.position[0]
        y = self.position[1]
        return generate_adjacent_coordinates(x, y)

    def check_for_number_adjacency(self, matrix):
        x = self.position[0]
        y = self.position[1]
        for coordinate in self.adjacent_coordinates:
            self.check_coordinate(matrix, coordinate)

    def add_to_numbers(self, number: Number):
        if number not in self.adjacent_numbers:
            self.adjacent_numbers.append(number)

    def check_coordinate(self, matrix, coordinate):
        try:
            if isinstance(matrix[coordinate[1], coordinate[0]], Number):
                self.add_to_numbers(matrix[coordinate[1], coordinate[0]])
                matrix[coordinate[1], coordinate[0]].is_adjacent_to_gear = True
        except IndexError:
            pass


def generate_adjacent_coordinates(x, y):
    return [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1),
        (x - 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y - 1),
        (x + 1, y + 1),
    ]


def parse_file(name: str) -> list:
    lines = []
    with open(name) as raw_file:
        for line in raw_file:
            lines.append([line.rstrip()])
    return lines


def generate_matrix(list_of_lines: list) -> np.array:
    x = len(list_of_lines[0][0])
    y = len(list_of_lines)
    matrix = np.empty((x, y), dtype=object)  # create empty matrix
    for y, line in enumerate(list_of_lines):
        for x, character in enumerate(line[0]):
            if character.isnumeric():
                input_char = Number(character, x, y)
            elif character == "*":
                input_char = Gear(x, y)
            else:
                input_char = character
            matrix[y, x] = input_char
    return matrix


def generate_adjacency_list(matrix: np.array) -> np.array:
    for row in matrix:
        for number in row:
            if isinstance(number, Number):
                number.check_for_symbol_adjacency(matrix)
    return matrix


def generate_gear_adjacency_list(matrix: np.array) -> np.array:
    for row in matrix:
        for number in row:
            if isinstance(number, Gear):
                number.check_for_number_adjacency(matrix)
    return matrix


def is_symbol(character: str) -> bool:
    if (not isinstance(character, Number)) and character != ".":
        return True


def fill_adjacent_numbers(matrix: np.array) -> np.array:
    for y, row in enumerate(matrix):
        for x, col in enumerate(row):
            if isinstance(col, Number):
                try:
                    if isinstance(matrix[y, x - 1], Number):
                        col.adjacent_numbers.append(matrix[y, x - 1])
                        try:
                            if isinstance(matrix[y, x - 2], Number):
                                col.adjacent_numbers.append(matrix[y, x - 2])
                        except IndexError:
                            pass
                except IndexError:
                    pass
                try:
                    if isinstance(matrix[y, x + 1], Number):
                        col.adjacent_numbers.append(matrix[y, x + 1])
                        try:
                            if isinstance(matrix[y, x + 2], Number):
                                col.adjacent_numbers.append(matrix[y, x + 2])
                        except IndexError:
                            pass
                except IndexError:
                    pass

    return matrix


def get_relevant_numbers(number_groups: list) -> list:
    relevant_numbers = []
    for number_group in number_groups:
        if number_group.is_relevant:
            number_group.accounted_for_in_final_tally = True
            relevant_numbers.append(number_group)
    return relevant_numbers


def get_relevant_gears(matrix: np.array, number_groups: list[NumberGroup]) -> list:
    relevant_gears = []
    for row in matrix:
        for number in row:
            if isinstance(number, Gear):
                if len(number.adjacent_numbers) >= 2:
                    gear_ratios = []
                    for adjacent_number in number.adjacent_numbers:
                        for number_group in number_groups:
                            if number_group.is_number_in_group(adjacent_number):
                                if number_group.may_be_gear:
                                    if number_group not in gear_ratios:
                                        gear_ratios.append(number_group)
                    relevant_gears.append(gear_ratios)
    return relevant_gears


def generate_number_groups(matrix: np.array) -> list:
    number_groups = []
    for row in matrix:
        for number in row:
            if isinstance(number, Number):
                if not number.accounted_for_in_number_group:
                    list_of_numbers = [number] + number.adjacent_numbers
                    number_group = NumberGroup(list_of_numbers)
                    for individual_number in list_of_numbers:
                        individual_number.accounted_for_in_number_group = True
                    number_groups.append(number_group)
    return number_groups


if __name__ == "__main__":
    file = parse_file("input3_puzzle1")
    # file = parse_file("test_file_day3")
    matrix_file = generate_matrix(file)
    adjacency_matrix = generate_adjacency_list(matrix_file)
    adjacency_matrix = generate_gear_adjacency_list(adjacency_matrix)
    matrix = fill_adjacent_numbers(adjacency_matrix)
    number_groups = generate_number_groups(matrix)
    relevant_numbers = get_relevant_numbers(number_groups)
    relevant_numbers_for_gears = get_relevant_gears(matrix, number_groups)
    relevant_numbers_for_gears = [
        gear for gear in relevant_numbers_for_gears if len(gear) == 2
    ]
    result_part_2 = []
    for relevant_number_for_gears in relevant_numbers_for_gears:
        result_part_2.append(
            relevant_number_for_gears[0].value * relevant_number_for_gears[1].value
        )
    print(matrix)
    print(relevant_numbers_for_gears)
    print("result part 1: ", sum([number.value for number in relevant_numbers]))
    print("result part 2: ", sum(result_part_2))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
