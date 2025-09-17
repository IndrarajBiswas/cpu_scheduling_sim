# Scheduling Algorithms

This project implements five classic CPU scheduling strategies. The Python
implementations live in [`app.py`](../app.py) and intentionally favour clarity
over micro-optimisations so that the control flow mirrors textbook descriptions.

## Common Concepts

All algorithms operate on a list of `Process` objects with the following fields:

- `arrival` – time at which the process becomes ready.
- `burst` – execution duration (also known as service time).
- `priority` – lower values indicate a higher priority in the Priority scheduler.
- `remaining` – mutable field used by preemptive algorithms (initially equal to
  `burst`).
- `waiting`, `turnaround`, `completion` – populated after the simulation to
  drive the UI metrics.

Every simulation function returns two pieces of information:

1. A **Gantt chart** list `(pid, start_time, end_time)` that the UI animates.
2. The list of processes with metrics filled in.

The helper `compute_stats` function aggregates average, min/max, standard
deviation, throughput and CPU utilisation across the completed processes.

---

## Algorithm Walkthroughs

### First-Come, First-Served (FCFS)

- **Type:** Non-preemptive.
- **Selection rule:** Execute processes strictly in order of arrival.
- **Implementation highlights:**
  - The input list is sorted by `arrival` once, then processed sequentially.
  - Idle CPU periods are represented by fast-forwarding `current_time` when the
    ready queue is empty.
- **What to look for:** FCFS is easy to reason about but can produce long waits
  for short jobs if a large burst arrives first (the convoy effect).

### Shortest Job First (SJF)

- **Type:** Non-preemptive.
- **Selection rule:** From the ready queue, pick the process with the smallest
  remaining burst.
- **Implementation highlights:**
  - Uses a simple list as the ready queue and resorts it after each arrival.
  - When no process has arrived yet, `current_time` jumps to the next arrival.
- **What to look for:** Lowest average waiting time for static workloads, but
  long bursts that arrive early can be postponed indefinitely.

### Round Robin

- **Type:** Preemptive.
- **Selection rule:** Rotate through the ready queue, giving each process up to
  a fixed quantum of CPU time per turn.
- **Implementation highlights:**
  - Maintains a FIFO queue and tracks `remaining` burst time per process.
  - New arrivals during a quantum are enqueued before the next iteration.
  - The default quantum is `4` time units but can be customised via the UI.
- **What to look for:** Improved fairness for time-sharing workloads at the
  expense of additional context switches.

### Static Priority

- **Type:** Non-preemptive.
- **Selection rule:** Choose the process with the **lowest** priority value
  (highest priority) from the ready queue.
- **Implementation highlights:**
  - When multiple processes share the same priority, arrival order decides.
  - Illustrates how starvation can appear when high-priority work keeps
    arriving.

### Highest Response Ratio Next (HRRN)

- **Type:** Non-preemptive, dynamic priority.
- **Selection rule:** Maximise the *response ratio* `(waiting + burst) / burst`.
- **Implementation highlights:**
  - Response ratios are recomputed every cycle to reflect time spent waiting.
  - Offers a compromise between SJF efficiency and FCFS fairness.
- **What to look for:** Observe how long jobs eventually overtake short ones as
  their ratio increases, reducing starvation.

---

## Extending the Simulator

To add a new algorithm:

1. Implement a `simulate_*` function following the pattern above (returning a
   Gantt chart plus the mutated process list).
2. Register it inside the `available_algs` dictionary in the `simulate` route.
3. Update the checkbox list in `templates/index.html` so that the algorithm can
   be selected.
4. Document the behaviour in this file to keep the knowledge base complete.

If your algorithm requires extra per-process attributes, extend the `Process`
class with the necessary defaults so that all simulations start from the same
baseline state.

