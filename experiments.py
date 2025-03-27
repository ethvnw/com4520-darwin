import csv
import datetime
import os

from fsm_gen.generator import FSMGenerator
from fsm_gen.mutator import Mutator
from walks.hsi import generate_harmonised_state_identifiers, generate_HSI_suite
from walks.random_walk import RandomWalk

FILENAME = f"results/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

def write_to_csv(state_size, input_size, output_size, percent, walk_type, result):
    with open(FILENAME, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([state_size, input_size, output_size, percent, result["hsi_len"], result["sum_hi"], walk_type, result["walk_len"], result["detected_fault_index"], result["time_taken"]])


def run_walk(state_size, input_size, output_size, percent, walk_type):
    fsm = FSMGenerator(state_size, input_size, output_size)
    while len(fsm.states) == 1:
        fsm = FSMGenerator(state_size, input_size, output_size)

    len_state_identifiers = 0
    state_identifiers = generate_harmonised_state_identifiers(fsm)
    for set in state_identifiers.values():
        for seq in set:
            len_state_identifiers += len(seq)

    hsi_suite = generate_HSI_suite(fsm, state_identifiers)

    mutator = Mutator(fsm)
    mutated_fsm = mutator.create_mutated_fsm()
    
    walker = RandomWalk(fsm, mutated_fsm, percent, hsi_suite)

    start_time = datetime.datetime.now()
    walk = walker.walk(walk_type)
    end_time = datetime.datetime.now()
    detected_fault = walker.detected_fault(walk)

    results = {
        "sum_hi": len_state_identifiers,
        "hsi_len": len(hsi_suite),
        "walk_len": len(walk) if type(walk) == list else walk,
        "detected_fault_index": detected_fault,
        "time_taken": end_time - start_time
    }

    write_to_csv(state_size, input_size, output_size, percent, walk_type, results)


def main():
    state_sizes = [5, 10, 20, 40]
    size_multipliers = {"2": 2, "n/2": 0.5, "n": 1, "2n": 2}
    percent_coverage = [80, 90, 95, 100]

    if not os.path.exists("results"):
        os.mkdir("results")

    with open(FILENAME, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["State Size", "Input Size", "Output Size", "Percent Coverage", "HSI Suite Length", "H_i Sum", "Walk Type", "Walk Length", "Detected Fault Index", "Time Taken"])

    for state_size in state_sizes:
        for input_size_multiplier in size_multipliers:
            if state_size >= 20 and input_size_multiplier == "2":
                continue

            input_size = 2 if input_size_multiplier == "2" else int(state_size * size_multipliers[input_size_multiplier])

            for output_size_multiplier in size_multipliers:
                if input_size == 2 and output_size_multiplier == "n/2":
                    continue

                output_size = 2 if output_size_multiplier == "2" else int(state_size * size_multipliers[output_size_multiplier])

                for _ in range(10):
                    for walk_type in RandomWalk.WalkType:
                        for percent in percent_coverage:
                            run_walk(state_size, input_size, output_size, percent, walk_type)

if __name__ == "__main__":
    main()