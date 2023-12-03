# This is a sample Python script.
from typing import Optional


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def parse_file(name: str) -> dict:
    lines = {}
    with open(name) as file:
        for line in file:
            game_number = line.split(':')[0]
            draws = line.rstrip().split(':')[1].split(';')
            list_of_draws = []
            for draw in draws:
                draw = draw.split(',')
                list_of_draws.append(
                    {single_draw.split(' ')[2]: int(single_draw.split(' ')[1]) for single_draw in draw})
            lines[game_number] = list_of_draws
    return lines


def get_valid_games(raw_file: dict):
    sack_content = {'red': 12, 'green': 13, 'blue': 14}
    valid_games = []
    for game_number, draws in raw_file.items():
        invalid_game = False
        for draw in draws:
            for color, number in draw.items():
                if number > sack_content[color]:
                    invalid_game = True
        if not invalid_game:
            valid_games.append(game_number)
    list_of_game_numbers = [int(game_number.split(' ')[1]) for game_number in valid_games]
    print('Valid games: ', valid_games)
    print('The sum of valid game numbers is: ' + str(sum(list_of_game_numbers)))


# Press the green button in the gutter to run the script.
def calculate_power(minimum_cubes: dict) -> int:
    power = 1
    for color, number in minimum_cubes.items():
        power = power * number
    return power


def get_powers(input_file: dict):
    list_of_powers = []
    for game_number, draws in input_file.items():
        minimum_cubes = {}
        for draw in draws:
            for color, number in draw.items():
                minimum_cubes[color] = max(minimum_cubes[color], number) if color in minimum_cubes.keys() else number
        list_of_powers.append(calculate_power(minimum_cubes))
    print('The sum of powers is: ' + str(sum(list_of_powers)))


if __name__ == '__main__':
    file_name = 'input2_puzzle1'
    # file_name = 'test_file'
    raw_file = parse_file(file_name)
    get_valid_games(raw_file)
    get_powers(raw_file)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
