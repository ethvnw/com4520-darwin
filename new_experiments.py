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


def distribute_tasks(state_sizes, input_sizes, percent_cov, input_size_multipliers):
    tasks = []
    for state_size in state_sizes:
        for input_size_key in input_sizes:
            if state_size == 20 or state_size == 40:
                if input_size_key == "2":
                    continue
                
            if input_size_key == "2":
                input_size = 2
            else:
                input_size = int(state_size * input_size_multipliers[input_size_key])

            for i in range(20):  # Generate 20 random automata for each configuration
                for percent in percent_cov:
                    tasks.append((state_size, input_size, i, percent))

    return tasks


def run_task(task):
    state_size, input_size, index, percent = task
    return run_walk(state_size, input_size, index, percent)


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()


    state_sizes = [5, 10, 20, 40]
    input_sizes = ["2", "n/2", "n", "2n"]
    percent_cov = [80, 90, 95, 99.5]
    input_size_multipliers = {"2": 2,"n/2": 0.5,"n": 1,"2n": 2}

    # Scatter tasks to ranks
    if rank == 0:
        tasks = distribute_tasks(state_sizes, input_sizes, percent_cov, input_size_multipliers)
        total_tasks = len(tasks)
        # Split tasks into chunks for scattering
        chunks = [tasks[i::size] for i in range(size)]
        print(f"Running {total_tasks} tasks with {size} ranks")
    else:
        chunks = None
        total_tasks = None

    # Broadcast total number of tasks to all ranks
    total_tasks = comm.bcast(total_tasks, root=0)

    # Scatter task chunks to all ranks
    task_chunk = comm.scatter(chunks, root=0)

    # Run assigned tasks with progress bar
    results = []
    for task in tqdm(task_chunk, desc=f"Rank {rank}", leave=True, position=rank, dynamic_ncols=True):
        state_size, input_size, index, percent = task
        result_key, result = run_walk(state_size, input_size, index, percent)
        results.append((result_key, result))

    # Gather results at rank 0
    all_results = comm.gather(results, root=0)

    if rank == 0:
        filename = f"result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["State Size", "Input Size", "Target Coverage", "Walk Length", "Time Taken"])

            for result_set in all_results:
                for result_key, result in result_set:
                    save_to_csv_row(writer, result_key, result)
