def parse_file(name: str) -> dict:
    lines = {}
    with open(name) as raw_file:
        for line in raw_file:
            line_parts = line.rstrip().split(":")
            winning_numbers = [
                int(number)
                for number in line_parts[1].split("|")[0].split(" ")
                if number.isnumeric()
            ]
            our_numbers = [
                int(number)
                for number in line_parts[1].split("|")[1].split(" ")
                if number.isnumeric()
            ]
            lines[line_parts[0]] = [set(winning_numbers), set(our_numbers)]
    return lines


def find_matches(winning_numbers: set, our_numbers: set) -> list:
    matches = []
    if winning_numbers & our_numbers:
        matches.append((winning_numbers & our_numbers))
    return matches


def calculate_match_points(matches: list) -> int:
    set_matches = matches[0] if len(matches) > 0 else set()
    if len(set_matches) == 0:
        return 0
    else:
        return 2 ** (len(set_matches) - 1)


def generate_card_copies(card_count: list) -> list:
    card_copies = [1] * len(card_count)
    for index, number in enumerate(card_count):
        for count in range(1, number + 1):
            card_copies[index + count] += 1 * card_copies[index]
    return card_copies


if __name__ == "__main__":
    file = parse_file("input4_puzzle1")
    # file = parse_file("test_file")
    matching_numbers = [
        find_matches(winning_numbers, our_numbers)
        for winning_numbers, our_numbers in file.values()
    ]

    match_points = [calculate_match_points(matches) for matches in matching_numbers]
    total_points = sum(match_points)
    print("Results part 1", total_points)

    count_matching_numbers = [
        0 if len(matches) == 0 else len(matches[0]) for matches in matching_numbers
    ]
    card_copies = generate_card_copies(count_matching_numbers)
    total_card_copies = sum(card_copies)
    print("Results part 2", total_card_copies)
