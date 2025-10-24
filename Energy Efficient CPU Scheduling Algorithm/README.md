# Energy-Efficient-Scheduler
> OS Project (Course PBL)

## Team Roles and Responsibilities

### - [Tanmay Chauhan](https://github.com/tanmaychauhan12) (Team Lead & Simulator Architect)
  - Primary Role: Designs and builds the core simulation engine—the "world" where the CPU and processes exist. He is responsible for the main time loop, process state transitions, and the energy consumption model.
- OS Algorithm: Implements the Round Robin (RR) scheduler. This is a foundational, preemptive algorithm that introduces the concept of a time quantum.

### - [Riya](https://github.com/Riya05s) (Performance Algorithm Specialist)
  - Primary Role: Focuses on a classic high-performance scheduling algorithm to serve as a key benchmark. She will also be responsible for implementing the core performance metrics (Turnaround Time, Wait Time).
- OS Algorithm: Implements the Shortest Remaining Time First (SRTF) scheduler. This is a more complex preemptive algorithm that requires constantly checking for shorter jobs.

### - Palak Bisht (Priority & UI Integration Lead)
  - Primary Role: Handles scheduling based on process priority and leads the integration of the backend simulator with the frontend UI.
- OS Algorithm: Implements the Preemptive Priority scheduler. This algorithm introduces the concept of process priority levels and how they trigger context switches.

### - [Muskan Bhatt](https://github.com/muskanbhatt) (Energy-Aware Algorithm & Data Analyst)
  - Primary Role: Develops the project's central innovation—the custom energy-aware scheduler. She is also responsible for creating test workloads and analyzing the final data to prove the project's hypothesis.
- OS Algorithm: Implements the Custom Energy-Aware (CEA) scheduler, using the composite score to balance performance and power.

## Motivation
Modern devices and data centers must balance performance with energy use. Traditional CPU schedulers (RR, SJF, Priority) ignore energy as a primary objective, causing unnecessary power draw and higher costs. This project builds an energy-aware scheduler that prioritizes processes using a composite score (estimated energy-to-finish, user priority, deadline urgency, and aging). It also uses adaptive time quanta, low-power state modeling, and a simple DVFS core model. A
Streamlit GUI will let users run experiments, view Gantt/energy timelines, and compare against standard baselines. The result is a reproducible tool to explore energy–performance tradeoffs

The Vision: An interactive web application where a user can upload a list of computing tasks, run them through four different CPU schedulers (three classic, one custom energy-aware), and instantly see a visual comparison of performance vs. energy consumption.


## Phase 0: Foundation & Setup (Target: Week 1)
Goal: Establish a professional project structure and a collaborative environment.
 1. Project Management (Tanmay):
    - Create a private repository on GitHub named Energy-Efficient-Scheduler.
    - Invite all team members as collaborators.
    - Set up a "Projects" board on GitHub with columns: Backlog, To-Do, In Progress, Done. Populate the To-Do list with the tasks from Phases 0 and 1.
 2. Environment Setup (Everyone):
    - Install Python, Git, and VS Code.
    - Clone the new repository: git clone <repository_url>
    - Create and activate a virtual environment:
       - python -m venv venv
         source venv/bin/activate
    - Create a requirements.txt file with the following, then run pip install -r requirements.txt:
       - streamlit
         pandas
         matplotlib
  3. Project Structure (Tanmay):
     - Create the following directory structure and push it to the repo. This keeps our code organized.
        ###
           /CPU-Scheduler-Showcase
           ├── algorithms/
           │   ├── round_robin.py
           │   ├── srtf.py
           │   ├── priority_preemptive.py
           │   └── advanced_energy_aware.py
           ├── simulator/
           │   ├── process.py
           │   └── cpu_simulator.py
           ├── utils/
           │   └── plotter.py
           ├── workloads/
           │   └── workload1.txt
           ├── app.py
           └── requirements.txt
  4. Core Data Class (Tanmay):
     - Create the file simulator/process.py. This class is the blueprint for every task we will schedule.

  Checkpoint: The core simulator exists. It's a "car" with no driver. Now, let's build the drivers (the algorithms).

## Phase 1: Building the Simulator Engine (Target: Week 2)
Goal: Create a functioning, time-based simulation loop.
Simulator Class (Tanmay):
  - Create simulator/cpu_simulator.py. This class will manage time, process queues, and the CPU state. It's the heart of the project.

Checkpoint: The core simulator exists. It's a "car" with no driver. Now, let's build the drivers (the algorithms).

## Phase 2: Implementing the Scheduling Algorithms (Target: Weeks 3-4)
Goal: Each team member implements their assigned OS scheduler. This is the main backend phase.
  - Standard Interface: All schedulers must be a class with an __init__(self, simulator) method and a schedule(self) method. This makes them plug-and-play.

  1. Round Robin (Tanmay):
     - Create algorithms/round_robin.py.
  2. Shortest Remaining Time First (Riya):
     - Create algorithms/srtf.py. This must be preemptive.
  4. Preemptive Priority (Palak):
     - Create algorithms/priority.py.
  5. Custom Energy-Aware (Muskan):
     - Create algorithms/energy_aware.py.

Checkpoint: All four scheduling algorithms are implemented in their respective files.

## Phase 3: Terminal-Based Integration & Testing (Target: Week 5)
Goal: Prove that all algorithms work correctly before building the UI.

  1. Main Script (Tanmay):
     - Expand main.py to load a workload, create four separate simulator instances (one for each algorithm), run them all, and print the comparative results to the terminal. This verifies the backend logic completely.

  2. Metric Calculations (Riya):
     - Write helper functions that take the finished_processes list and calculate average turnaround time and average wait time. Add these to the main.py printout.

  3. Comprehensive Workloads (Muskan):
     - Create workloads/cpu_heavy.txt (many long jobs) and workloads/mixed.txt (a realistic mix). Test all algorithms with all workloads.

  4. Debugging (Everyone):
     - This is a team effort. Run main.py and fix any bugs. Does SRTF preempt correctly? Does Round Robin cycle through processes? Does the energy count seem reasonable?

Checkpoint: Running python main.py produces a clean, correct, comparative report of all four schedulers for any given workload file.
