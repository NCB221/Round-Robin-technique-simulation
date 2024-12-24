import threading
import time
from queue import Queue

# Process structure
class Process:
    def __init__(self, id, burst_time, arrival_time):
        self.id = id
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turn_around_time = 0
        self.waiting_time = 0
        self.status = "waiting"

# Global variables
current_time = 0  # Current time in the simulator
mtx = threading.Lock()  # Mutual exclusion for synchronization

# Function to display status of processes
def print_status(processes):
    # Sleep to simulate the passage of time
    time.sleep(1)
    for process in processes:
        print(f"At time {current_time}, process P{process.id} is {process.status}")
        print(f"Thread ID {threading.get_ident()} is working")
    print()

# Function to simulate the Round Robin scheduling
def Round_Robin(processes, quantum_time):
    global current_time
    mtx.acquire()  # Lock the mutex to ensure exclusive access
    inQueue = [False] * len(processes)  # Array to check if the process has been in the ready queue or not

    ready_queue = Queue()  # Queue for ready processes
    for i, process in enumerate(processes):
        if process.arrival_time <= current_time:
            ready_queue.put(process)
            process.status = "ready"
            inQueue[i] = True

    while not ready_queue.empty():
        processing_process = ready_queue.get()  # Pointer to hold the process currently running
        processing_process.status = "running"  # Update status to running
        print_status(processes)  # Print the current status
        if processing_process.remaining_time > quantum_time:
            processing_process.remaining_time -= quantum_time
            current_time += quantum_time  # Update the current time
        else:
            # Process with remaining time less than quantum time will be terminated afterward
            current_time += processing_process.remaining_time
            processing_process.remaining_time = 0  # Process finishes execution
            processing_process.status = "terminated"  # Update status to terminated
            processing_process.completion_time = current_time

        # Loop to check if it is time for a process to enter the ready queue
        for i, process in enumerate(processes):
            if process.arrival_time <= current_time and process.remaining_time > 0 and not inQueue[i]:
                ready_queue.put(process)
                process.status = "ready"
                inQueue[i] = True

        # Process that was running but has not finished yet will be pushed back to ready queue
        if processing_process.remaining_time > 0:
            ready_queue.put(processing_process)
            processing_process.status = "ready"  # Update status to ready

    print_status(processes)  # Print the final status
    mtx.release()  # Unlock the mutex

# Function to calculate Turnaround Time and Waiting Time
def TAT_and_WT(processes):
    mtx.acquire()  # Lock the mutex to ensure exclusive access
    for process in processes:
        process.turn_around_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turn_around_time - process.burst_time

    total_TAT = sum(process.turn_around_time for process in processes)
    total_WT = sum(process.waiting_time for process in processes)

    print(f"Average Turnaround Time = {total_TAT / len(processes)}")
    print(f"Average Waiting Time = {total_WT / len(processes)}")
    print(f"Thread ID {threading.get_ident()} is working")
    mtx.release()  # Unlock the mutex

if __name__ == "__main__":
    #sample input
    quantum_time = 2
    processes = [
        Process(1, 5, 0),
        Process(2, 4, 1),
        Process(3, 2, 2),
        Process(4, 1, 4)
    ]

    # Create two threads
    thread1 = threading.Thread(target=Round_Robin, args=(processes, quantum_time))
    thread2 = threading.Thread(target=TAT_and_WT, args=(processes,))

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()
