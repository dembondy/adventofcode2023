# This is a sample Python script.
from typing import Optional

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

string_numbers = {'one': 1,
                  'two': 2,
                  'three': 3,
                  'four': 4,
                  'five': 5,
                  'six': 6,
                  'seven': 7,
                  'eight': 8,
                  'nine': 9}


def parse_file(name: str) -> list:
    with open(name) as file:
        lines = [line.rstrip() for line in file]
    return lines


def remove_letters_and_convert_to_list(line: str) -> list:
    numbers = []
    for character in line:
        if character.isnumeric():
            numbers.append(int(character))
    return numbers


def parse_letters(line: str) -> str:
    replace_dic = {key: key + str(number) + key for number, key in enumerate(string_numbers.keys(), 1)}
    for key, value in replace_dic.items():
        line = line.replace(key, value)
    return line


def merge_first_and_last_element_of_list(numbers: list) -> int:
    merged_numbers = int(str(numbers[0]) + str(numbers[-1]))
    return merged_numbers


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_name = 'input1_puzzle1'
    # file_name = 'test_file'
    raw_file = parse_file(file_name)
    parsed_letters = [parse_letters(line) for line in raw_file]
    clean_file_part1 = [remove_letters_and_convert_to_list(line) for line in raw_file]
    clean_file_part2 = [remove_letters_and_convert_to_list(line) for line in parsed_letters]
    numbers_file_part1 = [merge_first_and_last_element_of_list(line) for line in clean_file_part1]
    numbers_file_part2 = [merge_first_and_last_element_of_list(line) for line in clean_file_part2]
    total_part1 = sum(numbers_file_part1)
    total_part2 = sum(numbers_file_part2)
    print(f'The total number for part 1 is: {total_part1}')
    print(f'The total number for part 2 is: {total_part2}')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
