import csv
import datetime

from mpi4py import MPI
from tqdm import tqdm

from fsm_gen.generator import FSMGenerator
from walks.hsi import HSI
from walks.random_walk import RandomWalk


def save_to_csv_row(writer, key, result):
    state_size, input_size, _, coverage, walk_type = key.split("_")

    writer.writerow([state_size, input_size, coverage, walk_type, result["hsi_len"], result["walk_len"], result["time_taken"]])


def run_walk(state_size, input_size, index, percent, walk_type):
    fsm = FSMGenerator(state_size, input_size)
    key = f"{len(fsm.states)}_{input_size}_{index}"
    hsi_suite = HSI(fsm).generate_HSI_suite()
    walk = RandomWalk(fsm, percent, hsi_suite)

    start_time = datetime.datetime.now()
    walk_len = walk.walk(walk_type)
    end_time = datetime.datetime.now()

    return f"{key}_{percent}_{walk_type}", {
        "hsi_len": len(hsi_suite),
        "walk_len": walk_len,
        "time_taken": end_time - start_time
    }


def distribute_tasks(state_sizes, input_sizes, percent_cov, input_size_multipliers):
    tasks = []
    for state_size in state_sizes:
        for input_size_key in input_sizes:
            if state_size >= 20:
                if input_size_key == "2":
                    continue
                
            if input_size_key == "2":
                input_size = 2
            else:
                input_size = int(state_size * input_size_multipliers[input_size_key])

            for i in range(20):  # Generate 20 random automata for each configuration
                for percent in percent_cov:
                    for walk_type in RandomWalk.WalkType:
                        tasks.append((state_size, input_size, i, percent, walk_type))

    return tasks


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
        chunks = [tasks[i::size] for i in range(size)]
        print(f"Running {total_tasks} tasks with {size} ranks")
    else:
        chunks = None
        total_tasks = None

    total_tasks = comm.bcast(total_tasks, root=0)
    task_chunk = comm.scatter(chunks, root=0)

    # Run assigned tasks with progress bar
    results = []
    for task in tqdm(task_chunk, desc=f"Rank {rank}", leave=True, position=rank, dynamic_ncols=True):
        state_size, input_size, index, percent, walk_type = task
        result_key, result = run_walk(state_size, input_size, index, percent, walk_type)
        results.append((result_key, result))

    all_results = comm.gather(results, root=0)

    if rank == 0:
        filename = f"result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["State Size", "Input Size", "Target Coverage", "Walk Type", "HSI Suite Length", "Walk Length", "Time Taken"])

            for result_set in all_results:
                for result_key, result in result_set:
                    save_to_csv_row(writer, result_key, result)
