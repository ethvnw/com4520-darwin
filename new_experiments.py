import csv
import datetime
from tqdm import tqdm
from random_gen import FSMGenerator
from random_walk import RandomWalk
from mpi4py import MPI


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


def distibute_tasks(state_sizes, input_sizes, percent_cov, input_size_multipliers):
    tasks = []
    for state_size in state_sizes:
        for input_size_key in input_sizes:
            if input_size_key == "2":
                input_size = 2
            else:
                input_size = int(state_size * input_size_multipliers[input_size_key])

            for i in range(20):  # Generate 20 random automata for each configuration
                for percent in percent_cov:
                    tasks.append((state_size, input_size, i, percent))

    return tasks


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    state_sizes = [5, 10, 20, 40]
    input_sizes = ["2", "n/2", "n", "2n"]
    percent_cov = [80, 90, 95, 99.5]
    input_size_multipliers = {"2": 2,"n/2": 0.5,"n": 1,"2n": 2}

    if rank == 0:
        tasks = distibute_tasks(state_sizes, input_sizes, percent_cov, input_size_multipliers)
        num_tasks = len(tasks)
    else:
        tasks = None
        num_tasks = None

    num_tasks = comm.bcast(num_tasks, root=0)

    task_chunks = comm.scatter([tasks[i::size] for i in range(size)] if rank == 0 else None, root=0)

    results = []
    for task in tasks:
        state_size, input_size, index, percent = task
        result_key, result = run_walk(state_size, input_size, index, percent)
        results.append((result_key, result))

    all_results = comm.gather(results, root=0)

    if rank == 0:
        with open(f"results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["State Size", "Input Size", "Coverage", "Walk Length", "Time Taken"])

            with tqdm(total=num_tasks, desc="Running walks") as pbar:
                for result in all_results:
                    for key, result in result:
                        save_to_csv_row(writer, key, result)
                        pbar.update(1)
