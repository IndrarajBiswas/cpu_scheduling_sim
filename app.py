"""Flask application that visualises classic CPU scheduling algorithms.

The app exposes a small dashboard that generates pseudo-random workloads and
compares how different scheduling strategies behave under normal conditions and
after introducing a transient event.  The heavy lifting happens in plain Python
functions so that the implementation is easy to read and reason about when
teaching or self-studying operating system concepts.
"""

from __future__ import annotations

import copy
import math
import random
from typing import Dict, List, Sequence, Tuple

from flask import Flask, render_template, request

app = Flask(__name__)

# ----------------------------
# Process definition
# ----------------------------
class Process:
    """Representation of a process participating in the simulation."""

    def __init__(self, pid: int | str, arrival: int, burst: int, priority: int) -> None:
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority

        # Mutable attributes populated during simulations.
        self.remaining = burst  # For Round Robin calculations
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0
        self.start_time: int | None = None
        self.response_ratio: float = 0.0  # Used by HRRN scheduling

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"P{self.pid}(AT={self.arrival}, BT={self.burst}, Pri={self.priority})"

# ----------------------------
# Process Generation
# ----------------------------
def generate_processes(
    n: int = 97,
    arrival_range: Tuple[int, int] = (0, 20),
    burst_range: Tuple[int, int] = (1, 20),
    priority_range: Tuple[int, int] = (1, 10),
) -> List[Process]:
    """Return a list of randomly generated :class:`Process` objects."""

    processes: List[Process] = []
    for i in range(1, n + 1):
        arrival = random.randint(*arrival_range)
        burst = random.randint(*burst_range)
        priority = random.randint(*priority_range)
        processes.append(Process(i, arrival, burst, priority))
    return processes

# ----------------------------
# Scheduling Algorithms
# ----------------------------
def simulate_fcfs(processes: List[Process]) -> Tuple[List[Tuple[int | str, int, int]], List[Process]]:
    """Simulate First-Come, First-Served scheduling."""

    processes.sort(key=lambda p: p.arrival)
    current_time = 0
    gantt_chart: List[Tuple[int | str, int, int]] = []
    for p in processes:
        if current_time < p.arrival:
            current_time = p.arrival
        p.start_time = current_time
        p.waiting = current_time - p.arrival
        current_time += p.burst
        p.completion = current_time
        p.turnaround = p.completion - p.arrival
        gantt_chart.append((p.pid, p.start_time, p.completion))
    return gantt_chart, processes

def simulate_sjf(processes: List[Process]) -> Tuple[List[Tuple[int | str, int, int]], List[Process]]:
    """Simulate the non-preemptive Shortest Job First algorithm."""

    processes = sorted(processes, key=lambda p: p.arrival)
    completed: List[Process] = []
    gantt_chart: List[Tuple[int | str, int, int]] = []
    current_time = 0
    ready_queue: List[Process] = []
    while processes or ready_queue:
        while processes and processes[0].arrival <= current_time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda p: p.burst)
            p = ready_queue.pop(0)
            if current_time < p.arrival:
                current_time = p.arrival
            p.start_time = current_time
            p.waiting = current_time - p.arrival
            current_time += p.burst
            p.completion = current_time
            p.turnaround = p.completion - p.arrival
            gantt_chart.append((p.pid, p.start_time, p.completion))
            completed.append(p)
        else:
            current_time = processes[0].arrival
    return gantt_chart, completed

def simulate_round_robin(
    processes: List[Process], quantum: int = 4
) -> Tuple[List[Tuple[int | str, int, int]], List[Process]]:
    """Simulate the Round Robin algorithm with a fixed time quantum."""

    processes = sorted(processes, key=lambda p: p.arrival)
    queue: List[Process] = []
    current_time = 0
    gantt_chart: List[Tuple[int | str, int, int]] = []
    completed: List[Process] = []
    while processes or queue:
        if not queue and processes and processes[0].arrival > current_time:
            current_time = processes[0].arrival
        while processes and processes[0].arrival <= current_time:
            queue.append(processes.pop(0))
        if queue:
            p = queue.pop(0)
            if p.start_time is None:
                p.start_time = current_time
            exec_time = min(quantum, p.remaining)
            start_exec = current_time
            current_time += exec_time
            p.remaining -= exec_time
            gantt_chart.append((p.pid, start_exec, current_time))
            while processes and processes[0].arrival <= current_time:
                queue.append(processes.pop(0))
            if p.remaining > 0:
                queue.append(p)
            else:
                p.completion = current_time
                p.turnaround = p.completion - p.arrival
                p.waiting = p.turnaround - p.burst
                completed.append(p)
    return gantt_chart, completed

def simulate_priority(processes: List[Process]) -> Tuple[List[Tuple[int | str, int, int]], List[Process]]:
    """Simulate non-preemptive scheduling based on static priority values."""

    processes = sorted(processes, key=lambda p: p.arrival)
    ready_queue: List[Process] = []
    gantt_chart: List[Tuple[int | str, int, int]] = []
    current_time = 0
    completed: List[Process] = []
    while processes or ready_queue:
        while processes and processes[0].arrival <= current_time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda p: p.priority)  # lower number = higher priority
            p = ready_queue.pop(0)
            if current_time < p.arrival:
                current_time = p.arrival
            p.start_time = current_time
            p.waiting = current_time - p.arrival
            current_time += p.burst
            p.completion = current_time
            p.turnaround = p.completion - p.arrival
            gantt_chart.append((p.pid, p.start_time, p.completion))
            completed.append(p)
        else:
            current_time = processes[0].arrival
    return gantt_chart, completed

def simulate_hrrn(processes: List[Process]) -> Tuple[List[Tuple[int | str, int, int]], List[Process]]:
    """Simulate Highest Response Ratio Next scheduling."""

    processes = sorted(processes, key=lambda p: p.arrival)
    ready_queue: List[Process] = []
    gantt_chart: List[Tuple[int | str, int, int]] = []
    current_time = 0
    completed: List[Process] = []
    while processes or ready_queue:
        while processes and processes[0].arrival <= current_time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            for p in ready_queue:
                waiting_time = current_time - p.arrival
                p.response_ratio = (waiting_time + p.burst) / p.burst
            ready_queue.sort(key=lambda p: p.response_ratio, reverse=True)
            p = ready_queue.pop(0)
            if current_time < p.arrival:
                current_time = p.arrival
            p.start_time = current_time
            p.waiting = current_time - p.arrival
            current_time += p.burst
            p.completion = current_time
            p.turnaround = p.completion - p.arrival
            gantt_chart.append((p.pid, p.start_time, p.completion))
            completed.append(p)
        else:
            current_time = processes[0].arrival
    return gantt_chart, completed

# ----------------------------
# Transient Event Function (for web)
# ----------------------------
def apply_transient_event_choice(processes: List[Process], choice: str) -> Tuple[List[Process], str]:
    """Return a mutated process list after applying a transient event.

    Parameters
    ----------
    processes:
        The baseline workload prior to introducing an external disturbance.
    choice:
        Identifier of the user-selected scenario coming from the web form.
    """

    event_desc = ""
    extra_processes: List[Process] = []
    if choice == '1':
        event_desc = "High-priority process arrives at time=10."
        extra_processes.append(Process(pid='T1', arrival=10, burst=5, priority=1))
    elif choice == '2':
        event_desc = "A process with a very short burst time arrives at time=10."
        extra_processes.append(Process(pid='T2', arrival=10, burst=1, priority=random.randint(1,10)))
    elif choice == '3':
        event_desc = "Multiple processes arrive simultaneously at time=15."
        extra_processes.append(Process(pid='T3', arrival=15, burst=4, priority=3))
        extra_processes.append(Process(pid='T4', arrival=15, burst=6, priority=2))
    else:
        event_desc = "No transient event added."
    processes.extend(extra_processes)
    return processes, event_desc

# ----------------------------
# Detailed Statistical Analysis
# ----------------------------
def compute_stats(processes: Sequence[Process]) -> Dict[str, float]:
    """Compute aggregate metrics for a completed set of processes."""

    n = len(processes)
    if n == 0:
        return {}
    wait_times = [p.waiting for p in processes]
    turn_times = [p.turnaround for p in processes]
    min_wait = min(wait_times)
    max_wait = max(wait_times)
    avg_wait = sum(wait_times) / n
    std_wait = math.sqrt(sum((w - avg_wait) ** 2 for w in wait_times) / n)
    min_turn = min(turn_times)
    max_turn = max(turn_times)
    avg_turn = sum(turn_times) / n
    std_turn = math.sqrt(sum((t - avg_turn) ** 2 for t in turn_times) / n)
    first_arrival = min(p.arrival for p in processes)
    last_completion = max(p.completion for p in processes)
    busy_time = sum(p.burst for p in processes)
    total_time = last_completion - first_arrival if (last_completion - first_arrival) > 0 else 1
    throughput = n / total_time
    cpu_utilization = (busy_time / total_time) * 100
    return {
        "min_wait": min_wait,
        "max_wait": max_wait,
        "avg_wait": avg_wait,
        "std_wait": std_wait,
        "min_turn": min_turn,
        "max_turn": max_turn,
        "avg_turn": avg_turn,
        "std_turn": std_turn,
        "throughput": throughput,
        "cpu_utilization": cpu_utilization,
    }

# ----------------------------
# Flask Routes
# ----------------------------
@app.route("/", methods=["GET"])
def index() -> str:
    """Render the landing page with simulation controls."""

    return render_template("index.html")

@app.route("/simulate", methods=["POST"])
def simulate() -> str:
    """Execute the requested simulations and render the comparison view."""

    # Retrieve simulation parameters from form
    num_processes = int(request.form.get("num_processes", 97))
    time_quantum = int(request.form.get("time_quantum", 4))
    arrival_min = int(request.form.get("arrival_min", 0))
    arrival_max = int(request.form.get("arrival_max", 20))
    burst_min = int(request.form.get("burst_min", 1))
    burst_max = int(request.form.get("burst_max", 20))
    transient_event = request.form.get("transient_event", "4")
    selected_algs = request.form.getlist("algorithms")
    if not selected_algs:
        selected_algs = ["fcfs", "sjf", "rr", "priority", "hrrn"]

    base_processes = generate_processes(
        n=num_processes, 
        arrival_range=(arrival_min, arrival_max), 
        burst_range=(burst_min, burst_max),
        priority_range=(1,10)
    )

    available_algs = {
        "fcfs": ("FCFS", simulate_fcfs),
        "sjf": ("SJF", simulate_sjf),
        "rr": ("Round Robin (q=%d)" % time_quantum, lambda procs: simulate_round_robin(procs, quantum=time_quantum)),
        "priority": ("Priority", simulate_priority),
        "hrrn": ("HRRN", simulate_hrrn)
    }

    simulations = []
    for key in selected_algs:
        if key in available_algs:
            simulations.append(available_algs[key])

    baseline_results = {}
    for name, sim_func in simulations:
        procs_copy = copy.deepcopy(base_processes)
        gantt, completed = sim_func(procs_copy)
        avg_wait = sum(p.waiting for p in completed) / len(completed)
        avg_turn = sum(p.turnaround for p in completed) / len(completed)
        stats = compute_stats(completed)
        baseline_results[name] = {
            "gantt": gantt,
            "avg_wait": avg_wait,
            "avg_turn": avg_turn,
            "processes": completed,
            "stats": stats
        }

    transient_processes = copy.deepcopy(base_processes)
    transient_processes, event_description = apply_transient_event_choice(transient_processes, transient_event)
    transient_results = {}
    for name, sim_func in simulations:
        procs_copy = copy.deepcopy(transient_processes)
        gantt, completed = sim_func(procs_copy)
        avg_wait = sum(p.waiting for p in completed) / len(completed)
        avg_turn = sum(p.turnaround for p in completed) / len(completed)
        stats = compute_stats(completed)
        transient_results[name] = {
            "gantt": gantt,
            "avg_wait": avg_wait,
            "avg_turn": avg_turn,
            "processes": completed,
            "stats": stats
        }

    summary = []
    for name in baseline_results.keys():
        summary.append({
            "algorithm": name,
            "baseline_wait": baseline_results[name]["avg_wait"],
            "transient_wait": transient_results[name]["avg_wait"],
            "baseline_turn": baseline_results[name]["avg_turn"],
            "transient_turn": transient_results[name]["avg_turn"],
        })

    # For advanced dashboard: prepare additional chart data for line chart from first algorithm's processes
    first_alg = list(baseline_results.keys())[0]
    proc_data = baseline_results[first_alg]["processes"]
    process_ids = [str(p.pid) for p in proc_data]
    process_waits = [p.waiting for p in proc_data]
    process_turns = [p.turnaround for p in proc_data]

    chart_data = {
        "algorithms": list(baseline_results.keys()),
        "baseline_waits": [baseline_results[name]["avg_wait"] for name in baseline_results],
        "transient_waits": [transient_results[name]["avg_wait"] for name in transient_results],
        "baseline_turns": [baseline_results[name]["avg_turn"] for name in baseline_results],
        "transient_turns": [transient_results[name]["avg_turn"] for name in transient_results],
        "process_ids": process_ids,
        "process_waits": process_waits,
        "process_turns": process_turns
    }

    return render_template("results.html",
                           event_description=event_description,
                           baseline_results=baseline_results,
                           transient_results=transient_results,
                           summary=summary,
                           chart_data=chart_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)