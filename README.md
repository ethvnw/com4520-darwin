# Team Lambda (λ): Random Walks as a Test Generation Method
This repository contains the code to run the experiments used in the research paper: "Random Walks as a Test Generation Method". The repository contains:
- A finite state machine (FSM) generator that randomly generates X states, Y inputs and Z outputs
- A mutator that mutates a given FSM
- HSI test suite generation
- Four types of random walk implementation: pure random, random with resets, statistical and limited self-loops
- Experiments for assessing the effectiveness of the walk types 

## Setup

1. Clone the repository
2. Change directory to the repository
3. Install Graphviz:
    ```bash
    sudo apt-get install python3-dev graphviz libgraphviz-dev pkg-config
    ```
4. Create a virtual environment and setup dependencies:
    ```bash
    python3 -m venv ~/.venv/darwin
    ```
    ```bash
    source ~/.venv/darwin/bin/activate
    ```
    ```bash
    pip install -r requirements.txt
    ```

## Experiments
`experiments.py` can be run from terminal with:
```bash
python experiments.py
```
This conducts experiments for:
- 4 coverage targets [80, 90, 95, 100]%
- 4 FSM state sizes [5, 10, 20, 40]
- 4 size multipliers for inputs and outputs [2, n/2, n, 2n], where 'n' is:
    - the number of states for the input muliplier
    - the number of inputs for the output multiplier
- the 4 walk types

10 FSMs are generated for each configuration, resulting in over 7,500 experiments.
