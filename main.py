from collections import deque
import tkinter as tk
from tkinter import ttk

class Process:
    def __init__(self, name, arrival_time, execution_time, level):
        self.name = name
        self.arrival_time = arrival_time
        self.execution_time = execution_time
        self.exec_time = execution_time
        self.level = level
        self.waiting_time = 0

class MultilevelScheduler:
    def __init__(self):
        self.high_queue = deque()
        self.medium_queue = deque()
        self.low_queue = deque()

    def add_process(self, process):
        if process.level == '0':
            self.high_queue.append(process)
        elif process.level == '1':
            self.medium_queue.append(process)
        elif process.level == '2':
            self.low_queue.append(process)

    def run_scheduler(self):
        min_t = min(process.arrival_time for process in self.high_queue)
        time_b = min_t
        time_e = 0
        t_wait = 0
        avg_wait = 0

        process_names = []
        process_times_b = []
        process_times_e = []

        while self.high_queue or self.medium_queue or self.low_queue:
            if self.high_queue:
                h_q = 3
                self.high_queue = deque(sorted(self.high_queue, key=lambda x: x.arrival_time))
                process = self.high_queue.popleft()
                process_names.append(process.name)
                if(process.arrival_time > time_b):
                    time_b = process.arrival_time
                if process.execution_time > 0:
                    if process.execution_time < h_q:
                        h_q = process.execution_time
                    process.execution_time -= h_q
                    time_e = time_b + h_q
                    self.print_status(process, time_b, time_e)
                    process_times_b.append(time_b)
                    process_times_e.append(time_e)
                    time_b += h_q
                    process.waiting_time = time_e - (process.arrival_time + process.exec_time)
                if process.execution_time > 0:
                    self.medium_queue.append(process)


            elif self.medium_queue:
                m_q = 2
                self.medium_queue = deque(sorted(self.medium_queue, key=lambda x: x.execution_time))
                process = self.medium_queue.popleft()
                process_names.append(process.name)
                if(process.arrival_time > time_b):
                    time_b = process.arrival_time
                if process.execution_time > 0:
                    if process.execution_time < m_q:
                        m_q = process.execution_time
                    process.execution_time -= m_q
                    time_e = time_b + m_q
                    self.print_status(process, time_b, time_e)
                    process_times_b.append(time_b)
                    process_times_e.append(time_e)
                    time_b += m_q
                    process.waiting_time = time_e - (process.arrival_time + process.exec_time)
                if process.execution_time > 0:
                    self.low_queue.append(process)


            elif self.low_queue:
                self.low_queue = deque(sorted(self.low_queue, key=lambda x: x.execution_time))
                process = self.low_queue.popleft()
                process_names.append(process.name)
                if(process.arrival_time <= time_b):
                    while process.execution_time > 0:
                        time_e += process.execution_time
                        self.print_status(process, time_b, time_e)
                        process_times_b.append(time_b)
                        process_times_e.append(time_e)
                        time_b += process.execution_time
                        process.waiting_time = time_e - (process.arrival_time + process.exec_time)
                        process.execution_time = 0

            if(process.execution_time == 0):
                print(f"Process {process.name} completed execution")
                print(f"[ Process {process.name} waiting time : {process.waiting_time} ]")
                print("--------------------------------------------------------------")
                t_wait = t_wait + process.waiting_time

        print("--------------------------------------------------------------")
        avg_wait = t_wait/8
        print(f"[ Average waiting time : {round(avg_wait, 2)} ]")


        root = tk.Tk()
        root.title("Multi Level Processing")

        for i, name in enumerate(process_names):
            ttk.Label(root, text=name).grid(row=0, column=i * 2, padx=30, pady=20)
            ttk.Separator(root, orient="vertical").grid(row=0, column=i * 2 + 1, sticky="ns")
            ttk.Label(root, text="").grid(row=0, column=i * 2 + 2)

        for i, t_b in enumerate(process_times_b):
            ttk.Label(root, text=t_b, foreground="green").grid(row=1, column=i * 2, padx=3, pady=2)

        for i, t_e in enumerate(process_times_e):
            ttk.Label(root, text=t_e, foreground="red").grid(row=1, column=i * 2 + 1, padx=3, pady=2)

        root.mainloop()



    @staticmethod
    def print_status(process, time_b, time_e):
        print(f"Process {process.name} entered the kernel at time {time_b}")
        print(f"Process {process.name} left the kernel at time {time_e}")
        print("--------------------------------------------------------------")



if __name__ == '__main__':

    scheduler = MultilevelScheduler()

    # Add processes to the scheduler
    scheduler.add_process(Process('P0', 0, 5, '2')),
    scheduler.add_process(Process('P1', 0, 3, '1')),
    scheduler.add_process(Process('P2', 0, 1, '0')),
    scheduler.add_process(Process('P3', 10, 6, '1')),
    scheduler.add_process(Process('P4', 12, 8, '2')),
    scheduler.add_process(Process('P5', 14, 5, '0')),
    scheduler.add_process(Process('P6', 15, 2, '0')),
    scheduler.add_process(Process('P7', 17, 1, '1')),
    scheduler.add_process(Process('P8', 20, 7, '2'))



    # n = 8
    #
    # a = []
    # for i in range(n):
    #     value = int(input("Enter the arrival time for p" + str(i) + " : "))
    #     a.append(value)
    #
    # e = []
    # for i in range(n):
    #     value = int(input("Enter the execution time for p" + str(i) + " : "))
    #     e.append(value)
    #
    #
    # scheduler.add_process(Process("p0", a[0], e[0], '2'))
    # scheduler.add_process(Process("p1", a[1], e[1], '1'))
    # scheduler.add_process(Process("p2", a[2], e[2], '0'))
    # scheduler.add_process(Process("p3", a[3], e[3], '1'))
    # scheduler.add_process(Process("p4", a[4], e[4], '2'))
    # scheduler.add_process(Process("p5", a[5], e[5], '0'))
    # scheduler.add_process(Process("p6", a[6], e[6], '0'))
    # scheduler.add_process(Process("p7", a[7], e[7], '1'))
    # scheduler.add_process(Process("p8", a[8], e[8], '2'))


    # Run the scheduler
    scheduler.run_scheduler()
