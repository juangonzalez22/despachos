import matplotlib.pyplot as plt
import numpy as np
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]

def generate_process_colors(process_ids: list[str]) -> dict:
    cmap = plt.get_cmap("tab10")
    sorted_pids = sorted(process_ids, key=natural_sort_key)
    return {p_id: cmap(i % 10) for i, p_id in enumerate(sorted_pids)}

def plot_gantt_charts(results: dict):
    if not results:
        return

    first_algo_key = list(results.keys())[0]
    process_ids = list(results[first_algo_key]["metrics"]["processes"].keys())
    process_ids.sort(key=natural_sort_key, reverse=True)
    
    color_map = generate_process_colors(process_ids)

    for algo_name, data in results.items():
        gantt_data = data.get("gantt", [])
        max_time = max((block["end"] for block in gantt_data), default=10)

        fig, ax = plt.subplots(figsize=(11, 4), num=f"Gantt - {algo_name}")

        for block in gantt_data:
            p_id = block["id"]
            start = block["start"]
            duration = block["end"] - block["start"]
            y_pos = process_ids.index(p_id)

            ax.broken_barh(
                [(start, duration)],
                (y_pos - 0.35, 0.7),
                facecolors=color_map[p_id],
                edgecolors="black",
                linewidth=0.9
            )

            if duration > 0:
                ax.text(
                    start + duration / 2,
                    y_pos,
                    f"{duration}",
                    ha="center",
                    va="center",
                    color="white",
                    fontweight="bold",
                    fontsize=8
                )

        ax.set_title(f"Diagrama de Gantt - {algo_name}", fontsize=13, fontweight="bold", pad=10)
        ax.set_yticks(range(len(process_ids)))
        ax.set_yticklabels(process_ids, fontweight="bold")
        
        step = 1 if max_time <= 25 else max(2, max_time // 15)
        ax.set_xticks(range(0, max_time + 2, step))
        ax.set_xlim(0, max_time + 1)
        
        ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
        ax.set_xlabel("Tiempo (Unidades de CPU)", fontweight="bold")

        plt.tight_layout()
        plt.show(block=False)

def plot_comparison_chart(results: dict):
    if not results:
        return

    algos = list(results.keys())
    avg_system_times = [data["metrics"]["avg_system_time"] for data in results.values()]
    avg_waiting_times = [data["metrics"]["avg_waiting_time"] for data in results.values()]

    x = np.arange(len(algos))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5), num="Comparativa de Rendimiento")
    
    rects1 = ax.bar(x - width/2, avg_system_times, width, label="Tiempo de Sistema Promedio (TAT)", color="#3498db", edgecolor="black", linewidth=0.5)
    rects2 = ax.bar(x + width/2, avg_waiting_times, width, label="Tiempo de Espera Promedio (WT)", color="#e74c3c", edgecolor="black", linewidth=0.5)

    ax.set_ylabel("Tiempo Promedio", fontweight="bold")
    ax.set_title("Comparativa de Rendimiento entre Algoritmos", fontsize=13, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(algos, fontsize=10, fontweight="bold")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    ax.bar_label(rects1, fmt="%.2f", padding=3, fontsize=9)
    ax.bar_label(rects2, fmt="%.2f", padding=3, fontsize=9)

    plt.tight_layout()
    plt.show()