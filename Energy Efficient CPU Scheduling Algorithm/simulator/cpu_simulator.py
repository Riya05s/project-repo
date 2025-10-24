# simulator/cpu_simulator.py
import collections
import copy

class CPUSimulator:
    def __init__(self, processes):
        self.initial_processes = sorted(processes, key=lambda p: p.arrival_time)
        self.ready_queue = collections.deque()
        self.finished_processes = []
        self.current_time = 0
        self.current_process_on_cpu = None
        self.total_energy_consumed = 0
        self.gantt_chart = []
        self.time_quantum_slice = 0 # Specifically for Round Robin

        self.POWER_BUSY = 5
        self.POWER_IDLE = 1

    def run(self, scheduler):
        process_pool = [copy.deepcopy(p) for p in self.initial_processes]
        self.finished_processes, self.gantt_chart = [], []
        self.current_time, self.total_energy_consumed = 0, 0
        self.current_process_on_cpu = None
        self.ready_queue.clear()
        scheduler.sim = self

        while process_pool or self.ready_queue or self.current_process_on_cpu:
            while process_pool and process_pool[0].arrival_time <= self.current_time:
                self.ready_queue.append(process_pool.pop(0))

            scheduler.schedule()

            if self.current_process_on_cpu:
                if self.current_process_on_cpu.start_time == -1:
                    self.current_process_on_cpu.start_time = self.current_time
                self.gantt_chart.append(self.current_process_on_cpu.pid)
                self.current_process_on_cpu.remaining_time -= 1
                self.total_energy_consumed += self.POWER_BUSY
            else:
                self.gantt_chart.append("Idle")
                self.total_energy_consumed += self.POWER_IDLE

            if self.current_process_on_cpu and self.current_process_on_cpu.remaining_time == 0:
                self.current_process_on_cpu.finish_time = self.current_time + 1
                self.finished_processes.append(self.current_process_on_cpu)
                self.current_process_on_cpu = None
            
            for proc in self.ready_queue:
                proc.wait_time += 1
            
            self.current_time += 1

        self._calculate_final_metrics()
        return self.finished_processes, self.gantt_chart, self.total_energy_consumed

    def _calculate_final_metrics(self):
        for proc in self.finished_processes:
            proc.turnaround_time = proc.finish_time - proc.arrival_time