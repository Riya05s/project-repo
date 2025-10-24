# algorithms/srtf.py
class SRTF:
    def __init__(self):
        self.sim = None

    def schedule(self):
        best_process = self.sim.current_process_on_cpu

        for proc in self.sim.ready_queue:
            if best_process is None or proc.remaining_time < best_process.remaining_time:
                best_process = proc
        
        if best_process is not self.sim.current_process_on_cpu:
            if self.sim.current_process_on_cpu is not None:
                self.sim.ready_queue.append(self.sim.current_process_on_cpu)
            
            self.sim.current_process_on_cpu = best_process
            if best_process in self.sim.ready_queue:
                self.sim.ready_queue.remove(best_process)



            