import csv
import datetime
import concurrent.futures
import os
from tqdm import tqdm
from random_gen import FSMGenerator
from random_walk import RandomWalk


def save_to_csv_row(writer, key, result):
    state_size, input_size, machine_index, coverage = key.split("_")
    state_size = state_size[1:]  # Remove the 'S' prefix
    input_size = input_size[1:]  # Remove the 'I' prefix
    coverage = coverage[1:]  # Remove the 'C' prefix

    writer.writerow([state_size, input_size, coverage, result["walk_len"], result["time_taken"]])


def run_walk(state_size, input_size, index, percent):
    fsm = FSMGenerator(state_size, input_size).machine
    key = f"S{state_size}_I{input_size}_M{index}"
    start_time = datetime.datetime.now()
    walk = RandomWalk(fsm, RandomWalk.WalkType.RANDOM, percent)
    walk_len = walk.walk()
    end_time = datetime.datetime.now()

    return f"{key}_C{percent}", {
        "walk_len": walk_len,
        "time_taken": end_time - start_time
    }


if __name__ == '__main__':
    state_sizes = [5, 10, 20, 40]
    input_sizes = ["2", "n/2", "n", "2n"]
    percent_cov = [80, 90, 95, 99.5]

    input_size_multipliers = {
        "2": 2,
        "n/2": 0.5,
        "n": 1,
        "2n": 2
    }

    print("State sizes:", state_sizes)
    print("Input sizes:", input_sizes)
    print("Percent coverages:", percent_cov)

    if not os.path.exists("experiments"):
        os.makedirs("experiments")

    filename = f"experiments/experiment_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["State Size", "Input Size", "Target Coverage", "Walk Length", "Time Taken"])
        
        total_tasks = len(state_sizes) * len(input_sizes) * 20 * len(percent_cov)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            with tqdm(total=total_tasks, desc="Running random walks") as pbar:
                for state_size in state_sizes:
                    for input_size_key in input_sizes:
                        if input_size_key == "2":
                            input_size = 2
                        else:
                            input_size = int(state_size * input_size_multipliers[input_size_key])

                        for i in range(20):  # Generate 20 random automata for each configuration
                            for percent in percent_cov:
                                futures.append(executor.submit(run_walk, state_size, input_size, i, percent))

                for future in concurrent.futures.as_completed(futures):
                    result_key, result = future.result()
                    save_to_csv_row(writer, result_key, result)
                    pbar.update(1)
                    del result
