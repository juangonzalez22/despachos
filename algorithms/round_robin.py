import copy
from collections import deque

def run_round_robin(processes: list[dict], quantum: int = 2) -> dict:
    procs = copy.deepcopy(processes)
    procs.sort(key=lambda x: x["arrival"])

    current_time = 0
    ready_queue = deque()
    unvisited = list(procs)  # Procesos que aún no han entrado a la cola
    
    # Diccionarios de control
    remaining_burst = {p["id"]: p["burst"] for p in procs}
    arrival_times = {p["id"]: p["arrival"] for p in procs}
    original_bursts = {p["id"]: p["burst"] for p in procs}
    completion_times = {}

    gantt = []

    def check_new_arrivals(time_limit):
        nonlocal unvisited, ready_queue
        arrived = [p for p in unvisited if p["arrival"] <= time_limit]
        for p in arrived:
            ready_queue.append(p["id"])
            unvisited.remove(p)

    check_new_arrivals(current_time)

    if not ready_queue and unvisited:
        current_time = unvisited[0]["arrival"]
        check_new_arrivals(current_time)

    while ready_queue or unvisited:
        if not ready_queue:
            current_time = unvisited[0]["arrival"]
            check_new_arrivals(current_time)

        p_id = ready_queue.popleft()
        
        exec_time = min(quantum, remaining_burst[p_id])
        start_time = current_time
        end_time = start_time + exec_time
        
        remaining_burst[p_id] -= exec_time
        current_time = end_time

        gantt.append({
            "id": p_id,
            "start": start_time,
            "end": end_time
        })

        check_new_arrivals(current_time)

        if remaining_burst[p_id] > 0:
            ready_queue.append(p_id)
        else:
            completion_times[p_id] = current_time

    metrics_by_process = {}
    for p_id in original_bursts:
        system_time = completion_times[p_id] - arrival_times[p_id]
        waiting_time = system_time - original_bursts[p_id]
        
        metrics_by_process[p_id] = {
            "system_time": system_time,
            "waiting_time": waiting_time
        }

    total_procs = len(original_bursts)
    avg_system_time = sum(m["system_time"] for m in metrics_by_process.values()) / total_procs
    avg_waiting_time = sum(m["waiting_time"] for m in metrics_by_process.values()) / total_procs

    return {
        "gantt": gantt,
        "metrics": {
            "processes": metrics_by_process,
            "avg_system_time": avg_system_time,
            "avg_waiting_time": avg_waiting_time
        }
    }


if __name__ == "__main__":
    sample_processes = [
        {"id": "P1", "burst": 8, "arrival": 0, "priority": 1},
        {"id": "P2", "burst": 5, "arrival": 1, "priority": 1},
        {"id": "P3", "burst": 4, "arrival": 1, "priority": 2},
        {"id": "P4", "burst": 4, "arrival": 2, "priority": 2},
        {"id": "P5", "burst": 3, "arrival": 2, "priority": 1},
        {"id": "P6", "burst": 6, "arrival": 3, "priority": 3},
    ]

    result = run_round_robin(sample_processes, quantum=2)
    print("--- Resultado Round Robin (Quantum = 2) ---")
    print(f"Tiempo de Sistema Promedio: {result['metrics']['avg_system_time']:.2f}")
    print(f"Tiempo de Espera Promedio:  {result['metrics']['avg_waiting_time']:.2f}")