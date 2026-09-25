import copy

def run_fifo(processes: list[dict]) -> dict:

    procs = copy.deepcopy(processes)
    
    procs.sort(key=lambda x: x["arrival"])

    current_time = 0
    gantt = []
    metrics_by_process = {}

    for p in procs:
        if current_time < p["arrival"]:
            current_time = p["arrival"]

        start_time = current_time
        end_time = start_time + p["burst"]

        system_time = end_time - p["arrival"]
        waiting_time = start_time - p["arrival"] 

        gantt.append({
            "id": p["id"],
            "start": start_time,
            "end": end_time
        })

        metrics_by_process[p["id"]] = {
            "system_time": system_time,
            "waiting_time": waiting_time
        }

        current_time = end_time

    total_procs = len(procs)
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

