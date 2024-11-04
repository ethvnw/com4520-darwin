# com4520-darwin

## Setup

1. Clone the repository
2. Change directory to the repository
3. Install Graphviz:
    ```
    sudo apt-get install python3-dev graphviz libgraphviz-dev pkg-config
    ```
4. Create a virtual environment and setup dependencies:

    ```
    python3 -m venv ~/.venv/darwin
    ```

    ```
    source ~/.venv/darwin/bin/activate
    ```

    ```
    pip install -r requirements.txt
    ```

5. Run the application:

    ```
    python test.py
    ```
