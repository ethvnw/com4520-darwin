from fsm_gen.generator import FSMGenerator
import collections


def is_connected(fsm):
    def dfs(start_state):
        visited = set()
        stack = [start_state]
        while stack:
            state = stack.pop()
            if state not in visited:
                visited.add(state)
                for transition in fsm.transitions:
                    if transition['source'] == state:
                        stack.append(transition['dest'])
        return visited

    all_states = set(fsm.states)
    for state in fsm.states:
        if dfs(state) != all_states:
            return False
        
    return True

def is_deterministic(fsm):
    events = collections.Counter(fsm.events)

    for state in fsm.states:
        transitions = [t for t in fsm.transitions if t["source"] == state]
        triggers = [t["trigger"].split(' / ')[0] for t in transitions]

        if collections.Counter(triggers) != events:
            return False
        
    return True


# run test on 500 random FSMs
tests_failed = []
for i in range(1000):
    fsm = FSMGenerator(num_states=10, num_inputs=2)
    try:
        assert is_connected(fsm)
        assert is_deterministic(fsm)
    except AssertionError:
        tests_failed.append(i)
        print(f"{i}: Connected: {is_connected(fsm)}")
        print(f"{i}: Deterministic: {is_deterministic(fsm)}")
        fsm.draw(f"error_{i}.png")

    
