# CPU Scheduling Simulator

This project demonstrates various **CPU Scheduling** algorithms (FCFS, SJF, Round Robin, Priority, and HRRN) through an **interactive web interface**. It shows how each algorithm schedules a set of processes and reacts to transient events, with visual Gantt charts and key metrics like waiting and turnaround times.

---

## Basic Premise
- **CPU Scheduling** determines how processes are selected for execution.
- Each algorithm has different strategies for prioritizing processes.
- This simulator:
  1. Generates a set of processes (with randomized arrival/burst times).
  2. Allows you to choose one or more scheduling algorithms.
  3. Demonstrates how these algorithms handle a transient event (e.g., new processes arriving mid-simulation).

---

## How to Install & Run

### Option 1: Run with Docker
1. **Install Docker** (if you don’t already have it).
2. **Build the Image** (or pull it from Docker Hub if available):
   ```bash
   docker build -t cpu_scheduling_sim .
   ```
3. **Run the Container**:
   ```bash
   docker run -p 5000:5000 cpu_scheduling_sim
   ```
4. **Open the Web UI**:  
   In your browser, go to [http://localhost:5000](http://localhost:5000) to explore the simulator.

### Option 2: Run Locally (Without Docker)
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/IndrarajBiswas/cpu_scheduling_sim.git
   cd cpu_scheduling_sim
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the App**:
   ```bash
   python app.py
   ```
4. **Open the Web UI**:  
   In your browser, go to [http://localhost:5000](http://localhost:5000).

---

**Enjoy exploring CPU Scheduling algorithms!** If you have any questions or suggestions, feel free to open an issue or submit a pull request.

