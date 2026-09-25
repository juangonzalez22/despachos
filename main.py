import os
from utils.reader import load_processes_from_csv
from utils.visualizer import plot_gantt_charts, plot_comparison_chart
from algorithms.fifo import run_fifo
from algorithms.round_robin import run_round_robin

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "procesos.csv")

    print(f"Cargando datos desde: {file_path}")
    
    try:
        processes = load_processes_from_csv(file_path)
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return

    quantum = 2

    results = {
        "FIFO": run_fifo(processes),
        f"Round Robin (Q={quantum})": run_round_robin(processes, quantum=quantum)
    }

    print("\n" + "="*55)
    print("      RESUMEN DE MÉTRICAS POR ALGORITMO")
    print("="*55)
    
    for algo_name, data in results.items():
        print(f"\n--- {algo_name} ---")
        print(f"{'Proceso':<10}{'T. Sistema (TAT)':<20}{'T. Espera (WT)':<20}")
        print("-" * 55)
        
        p_metrics = data["metrics"]["processes"]
        for p_id in sorted(p_metrics.keys()):
            m = p_metrics[p_id]
            print(f"{p_id:<10}{m['system_time']:<20.2f}{m['waiting_time']:<20.2f}")
            
        print("-" * 55)
        print(f"Promedio T. Sistema: {data['metrics']['avg_system_time']:.2f}")
        print(f"Promedio T. Espera:  {data['metrics']['avg_waiting_time']:.2f}")

    plot_gantt_charts(results)
    plot_comparison_chart(results)

if __name__ == "__main__":
    main()