def parse_file(name: str) -> dict:
    lines = {}
    with open(name) as raw_file:
        for line in raw_file:
            lines[line.split(":")[0]] = [
                int(entry)
                for entry in line.rstrip().split(":")[1].split(" ")
                if entry.isnumeric()
            ]
    return lines


# let's write a test for the function below
def calculate_distance(time_pressed: int, race_duration: int) -> int:
    time_available = race_duration - time_pressed
    distance = time_pressed * time_available
    return distance


def calculate_winning_presstimes(race_duration: int, current_record: int) -> list:
    possible_presstimes = []
    for presstime in range(race_duration):
        possible_presstimes.append(calculate_distance(presstime, race_duration))
    return [time for time in possible_presstimes if time > current_record]


def calculate_margin_error(file: dict) -> int:
    winning_presstimes = list()
    for available_time, current_record_distance in zip(file["Time"], file["Distance"]):
        winning_presstimes.append(
            len(calculate_winning_presstimes(available_time, current_record_distance))
        )
    margin_error = 1
    for winning_presstime in winning_presstimes:
        margin_error *= winning_presstime
    return margin_error


def fix_file_kerning(file: dict) -> dict:
    fixed_file = dict()
    time_strings = [str(time) for time in file["Time"]]
    time = str()
    for time_string in time_strings:
        time += time_string
    fixed_file["Time"] = [int(time)]
    distance_strings = [str(distance) for distance in file["Distance"]]
    distance = str()
    for distance_string in distance_strings:
        distance += distance_string
    fixed_file["Distance"] = [int(distance)]
    return fixed_file


if __name__ == "__main__":
    # raw_file = parse_file("test_file6")
    raw_file = parse_file("input6_puzzle1")
    result_part_1 = calculate_margin_error(raw_file)
    print(result_part_1)
    fixed_file = fix_file_kerning(raw_file)
    result_part_2 = len(
        calculate_winning_presstimes(fixed_file["Time"][0], fixed_file["Distance"][0])
    )
    print(result_part_2)
