import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def generate_process_colors(process_ids: list[str]) -> dict:
    """
    Genera un mapa de colores único para cada proceso.
    """
    cmap = plt.get_cmap("tab10")
    colors = {}
    for i, p_id in enumerate(sorted(process_ids)):
        colors[p_id] = cmap(i % 10)
    return colors


def plot_gantt_charts(results: dict):
    """
    Genera una figura con los diagramas de Gantt para cada algoritmo cargado.
    """
    num_algos = len(results)
    if num_algos == 0:
        return

    fig, axes = plt.subplots(num_algos, 1, figsize=(12, 3 * num_algos), sharex=False)
    if num_algos == 1:
        axes = [axes]

    first_algo_key = list(results.keys())[0]
    process_ids = list(results[first_algo_key]["metrics"]["processes"].keys())
    process_ids.sort(reverse=True)
    
    color_map = generate_process_colors(process_ids)

    for ax, (algo_name, data) in zip(axes, results.items()):
        gantt_data = data["gantt"]

        max_time = max(block["end"] for block in gantt_data) if gantt_data else 10

        for block in gantt_data:
            p_id = block["id"]
            start = block["start"]
            duration = block["end"] - block["start"]
            y_pos = process_ids.index(p_id)

            ax.broken_barh(
                [(start, duration)],
                (y_pos - 0.4, 0.8),
                facecolors=color_map[p_id],
                edgecolors="black",
                linewidth=0.8
            )

        ax.set_title(f"Diagrama de Gantt - {algo_name}", fontsize=12, fontweight="bold")
        ax.set_yticks(range(len(process_ids)))
        ax.set_yticklabels(process_ids)
        ax.set_xticks(range(0, max_time + 2, 1))
        ax.set_xlim(0, max_time + 1)
        ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)
        ax.set_xlabel("Tiempo (Unidades de CPU)")

    plt.tight_layout()
    plt.show()


def plot_comparison_chart(results: dict):
    algos = list(results.keys())
    avg_system_times = [data["metrics"]["avg_system_time"] for data in results.values()]
    avg_waiting_times = [data["metrics"]["avg_waiting_time"] for data in results.values()]

    x = np.arange(len(algos))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    
    rects1 = ax.bar(x - width/2, avg_system_times, width, label="Tiempo de Sistema Promedio (TAT)", color="#3498db")
    rects2 = ax.bar(x + width/2, avg_waiting_times, width, label="Tiempo de Espera Promedio (WT)", color="#e74c3c")

    ax.set_ylabel("Tiempo Promedio")
    ax.set_title("Comparativa de Rendimiento entre Algoritmos", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(algos, fontsize=11)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Añadir las etiquetas con el valor exacto sobre cada barra
    ax.bar_label(rects1, fmt="%.2f", padding=3)
    ax.bar_label(rects2, fmt="%.2f", padding=3)

    plt.tight_layout()
    plt.show()
