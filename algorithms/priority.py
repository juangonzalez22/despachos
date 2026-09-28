import copy

def run_priority(processes: list[dict]) -> dict:
    unvisited = copy.deepcopy(processes)
    unvisited.sort(key=lambda x: x["arrival"])

    current_time = 0
    gantt = []
    metrics_by_process = {}

    while unvisited:
        ready_procs = [p for p in unvisited if p["arrival"] <= current_time]

        if not ready_procs:
            current_time = unvisited[0]["arrival"]
            continue

        ready_procs.sort(key=lambda x: x["priority"])
        chosen_proc = ready_procs[0]

        start_time = current_time
        end_time = start_time + chosen_proc["burst"]

        system_time = end_time - chosen_proc["arrival"]
        waiting_time = start_time - chosen_proc["arrival"]

        current_time = end_time

        unvisited.remove(chosen_proc)

        gantt.append({
            "id": chosen_proc["id"],
            "start": start_time,
            "end": end_time
        })

        metrics_by_process[chosen_proc["id"]] = {
            "system_time": system_time,
            "waiting_time": waiting_time
        }

    total_procs = len(processes)
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