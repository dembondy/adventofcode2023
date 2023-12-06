from dask.distributed import Client, progress
import dask


def parse_file(name: str) -> tuple[list, dict]:
    mappings_dict = dict()
    conversion_flag = str()
    with open(name) as raw_file:
        buffer = list()
        for line in raw_file:
            if "seeds" in line:
                seeds_list = [
                    int(number) for number in line.rstrip().split(":")[1].split(" ")[1:]
                ]
            elif line == "\n":
                if conversion_flag:
                    mappings_dict[conversion_flag] = buffer
                    buffer = list()
            elif "map" in line:
                conversion_flag = line.split(" ")[0]
            else:
                buffer.append([int(number) for number in line.rstrip().split(" ")])
    return seeds_list, mappings_dict


def convert_with_mappings(sources: list[int], mappings: list[list[int]]) -> list[int]:
    destinations = list()
    for source in sources:
        for mapping in mappings:
            if mapping[1] <= source <= (mapping[1] + mapping[2]):
                gap = source - mapping[1]
                destination = mapping[0] + gap
                destinations.append(destination)
                break
        else:
            destinations.append(source)
    return destinations


def reverse_convert_with_mappings(
    destinations: list[int], mappings: list[list[int]]
) -> list[int]:
    sources = list()
    for destination in destinations:
        for mapping in reversed(mappings):
            if mapping[0] <= destination <= (mapping[0] + mapping[2]):
                gap = destination - mapping[0]
                source = mapping[1] + gap
                sources.append(source)
                break
        else:
            sources.append(destination)
    return sources


def expand_seeds(input_seeds: list[int]) -> list[range]:
    seed_starts = input_seeds[::2]
    seed_ranges = input_seeds[1::2]
    seeds_expanded = list()
    for seed_start, seed_range in zip(seed_starts, seed_ranges):
        seeds_expanded.append(range(seed_start, seed_start + seed_range + 1))
    return seeds_expanded


# @dask.delayed
def apply_sequence(
    sequence_seeds: list, sequence_mappings: dict, reverse: bool = False
) -> list:
    tmp_result = sequence_seeds
    if reverse is False:
        for key, value in sequence_mappings.items():
            tmp_result = convert_with_mappings(
                tmp_result, value
            )  # how can this be done with a reduce function?
    else:
        for key, value in reversed(sequence_mappings.items()):
            tmp_result = reverse_convert_with_mappings(tmp_result, value)
    return tmp_result


if __name__ == "__main__":
    seeds, mappings = parse_file("input5_puzzle1")
    # seeds, mappings = parse_file("test_file")
    results_part_1 = apply_sequence(seeds, mappings)

    print("Results of puzzle 1:", min(results_part_1))

    # Let's try reverse search instead
    seed_ranges = expand_seeds(seeds)
    valid_minimum_value = 0
    breakout_flag = False
    while True:
        candidate_seed = apply_sequence([valid_minimum_value], mappings, reverse=True)
        for seed_range in seed_ranges:
            if candidate_seed[0] in seed_range:
                print(
                    f"Found {candidate_seed[0]} in {seed_range}, with {valid_minimum_value}"
                )
                breakout_flag = True
                break
        if breakout_flag:
            break
        valid_minimum_value += 1

    print("Results part 2:", valid_minimum_value)
    # This was painful.
