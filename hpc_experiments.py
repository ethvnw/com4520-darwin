import csv
import datetime
import gc
import os

from mpi4py import MPI
from tqdm import tqdm

from fsm_gen.generator import FSMGenerator
from fsm_gen.mutator import Mutator
from walks.hsi import generate_HSI_suite
from walks.random_walk import RandomWalk

TIME = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def setup_csvs(num_workers: int) -> None:
    """
    Create CSV files for each worker to store results.
    Args:
        num_workers (int): The number of worker processes.
    """
    if not os.path.exists("results"):
        os.mkdir("results")

    for i in range(1, num_workers + 1):
        filename = f"results/{i}_{TIME}.csv"
        with open(filename, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "State Size",
                    "Input Size",
                    "Output Size",
                    "Percent Coverage",
                    "HSI Suite Length",
                    "Walk Type",
                    "Walk Length",
                    "Detected Fault Index",
                    "Time Taken",
                ]
            )


def write_to_csv(
    state_size: int,
    input_size: int,
    output_size: int,
    percent: int,
    walk_type: RandomWalk.WalkType,
    result: dict,
    rank: int,
) -> None:
    """
    Write the results of the walk to a CSV file.
    Args:
        state_size (int): The number of states in the FSM.
        input_size (int): The number of inputs in the FSM.
        output_size (int): The number of outputs in the FSM.
        percent (int): The percentage of the FSM to cover.
        walk_type (RandomWalk.WalkType): The type of walk performed.
        result (dict): The results of the walk.
        rank (int): The rank of the MPI process.
    """
    filename = f"results/{rank}_{TIME}.csv"

    with open(filename, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                state_size,
                input_size,
                output_size,
                percent,
                result["hsi_len"],
                walk_type,
                result["walk_len"],
                result["detected_fault_index"],
                result["time_taken"],
            ]
        )


def run_walk(
    state_size: int,
    input_size: int,
    output_size: int,
    _,
    percent: int,
    walk_type: RandomWalk.WalkType,
    rank: int,
) -> None:
    """
    Run a walk on the FSM and record the results.
    Args:
        state_size (int): The number of states in the FSM.
        input_size (int): The number of inputs in the FSM.
        output_size (int): The number of outputs in the FSM.
        percent (int): The percentage of the FSM to cover.
        walk_type (RandomWalk.WalkType): The type of walk to perform.
        rank (int): The rank of the MPI process.
    """
    fsm = FSMGenerator(state_size, input_size, output_size)
    while len(fsm.states) == 1:
        fsm = FSMGenerator(state_size, input_size, output_size)

    hsi_suite = generate_HSI_suite(fsm)
    mutator = Mutator(fsm)
    mutated_fsm = mutator.create_mutated_fsm()

    walker = RandomWalk(fsm, mutated_fsm, percent, hsi_suite)

    start_time = datetime.datetime.now()
    walk = walker.walk(walk_type)
    end_time = datetime.datetime.now()
    detected_fault = walker.detected_fault(walk)

    results = {
        "hsi_len": len(hsi_suite),
        "walk_len": len(walk) if type(walk) == list else walk,
        "detected_fault_index": detected_fault,
        "time_taken": end_time - start_time,
    }

    write_to_csv(state_size, input_size, output_size, percent, walk_type, results, rank)


def main():
    """
    Parallel processing version of experiments.py.
    Run in terminal:
    mpiexec -n 4 python3 hpc_experiments.py"""
    state_sizes = [5, 10, 20, 40]
    size_multipliers = {"2": 2, "n/2": 0.5, "n": 1, "2n": 2}
    percent_coverage = [80, 90, 95, 100]

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # Process ID
    size = comm.Get_size()  # Total number of processes

    if rank == 0:  # Master process distributes work
        tasks = []

        for state_size in state_sizes:
            for input_size_multiplier in size_multipliers:
                if state_size >= 20 and input_size_multiplier == "2":
                    continue

                input_size = (
                    2
                    if input_size_multiplier == "2"
                    else int(state_size * size_multipliers[input_size_multiplier])
                )

                for output_size_multiplier in size_multipliers:
                    if input_size == 2 and output_size_multiplier == "n/2":
                        continue

                    output_size = (
                        2
                        if output_size_multiplier == "2"
                        else int(state_size * size_multipliers[output_size_multiplier])
                    )

                    for i in range(10):
                        for walk_type in RandomWalk.WalkType:
                            for percent in percent_coverage:
                                tasks.append(
                                    (
                                        state_size,
                                        input_size,
                                        output_size,
                                        i,
                                        percent,
                                        walk_type,
                                    )
                                )

        # Distribute tasks to worker processes
        num_workers = size - 1
        chunk_size = len(tasks) // num_workers
        task_chunks = [
            tasks[i * chunk_size : (i + 1) * chunk_size] for i in range(num_workers)
        ]
        setup_csvs(num_workers)

        for i in range(num_workers):
            comm.send(task_chunks[i], dest=i + 1, tag=11)

    else:  # Worker processes
        tasks = comm.recv(source=0, tag=11)

        # Progress bar for each worker
        for task in tqdm(tasks, desc=f"Worker {rank}", position=rank, leave=True):
            run_walk(*task, rank)
            gc.collect()


if __name__ == "__main__":
    main()
