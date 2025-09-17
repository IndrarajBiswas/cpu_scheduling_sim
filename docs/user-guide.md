# User Guide

This guide walks through the simulator's interface and explains how to interpret
the output. Launch the application (see the main `README.md` for instructions)
and follow along.

## 1. Configuration Form

The landing page (`/`) contains the configuration controls.

### Workload controls

- **Number of Processes** – how many synthetic processes to generate.
- **Arrival Range** – inclusive bounds for randomly sampled arrival times.
- **Burst Range** – inclusive bounds for randomly sampled CPU burst durations.
- **Time Quantum (RR)** – quantum length used only by the Round Robin algorithm.

### Algorithm selection

Tick one or more of the following checkboxes to include them in the results:

- FCFS
- SJF
- Round Robin
- Priority
- HRRN

### Transient event scenarios

Choose one of the radio buttons to introduce a disturbance in the baseline
workload:

1. **High-priority process** at time `10` with burst `5` and priority `1`.
2. **Very short burst** at time `10` (priority randomised).
3. **Simultaneous arrivals** – two extra processes at time `15`.
4. **No event** – the baseline workload is reused.

A preview panel on the right updates live as you change values so you can double
check the configuration before running the simulation.

## 2. Results Dashboard

Submitting the form posts to `/simulate` and displays the dashboard.

### Per-algorithm cards

Each selected algorithm renders as a card containing:

- **Animated Gantt chart** – click “Play Animation” to reveal the execution
  order.
- **Average metrics** – waiting time and turnaround time for the algorithm.
- **Process table** (collapsible) – per-process breakdown of arrival, burst,
  waiting and turnaround times.
- **Detailed statistics** (collapsible) – min/max/standard deviation, throughput
  and CPU utilisation.

### Charts

At the top of the results page you will find two Chart.js visualisations:

- **Metrics bar chart** – compares baseline vs transient average waiting and
  turnaround times for every algorithm.
- **Process line chart** – plots waiting and turnaround times for individual
  processes belonging to the first algorithm in the selection.

### Scenario bookmarking

Use the buttons above the charts to manage saved scenarios:

- **Save This Scenario** – prompts for a name and stores the summary in
  `localStorage`.
- **Show Saved Scenarios** – toggles a table comparing the first algorithm’s
  metrics across saved runs.
- **Clear Saved Scenarios** – wipes saved data from the browser.

## 3. Tips & Troubleshooting

- Round Robin is the only preemptive algorithm implemented; reduce the time
  quantum if the Gantt chart feels too similar to FCFS.
- If the dashboard appears empty, ensure at least one algorithm checkbox was
  selected before running the simulation.
- Transient events may cause process IDs such as `T1`, `T2`, etc., to appear in
  the results tables. These processes are tagged separately so you can see the
  impact of the injected workload.
- The simulator uses random data; re-running with the same configuration will
  generate a different workload unless you modify `generate_processes` to use a
  fixed seed.

