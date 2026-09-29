import csv
import os

def load_processes_from_csv(file_path: str) -> list[dict]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo '{file_path}' no fue encontrado.")

    processes = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        required_headers = {"Proceso", "Tiempo_CPU", "Tiempo_Llegada", "Prioridad"}
        if not required_headers.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"El CSV debe contener las columnas: {required_headers}")

        for row in reader:
            try:
                process = {
                    "id": str(row["Proceso"]).strip(),
                    "burst": int(row["Tiempo_CPU"]),
                    "arrival": int(row["Tiempo_Llegada"]),
                    "priority": int(row["Prioridad"])
                }
                
                if process["burst"] <= 0 or process["arrival"] < 0:
                    raise ValueError(f"Tiempos inválidos en el proceso {process['id']}")
                    
                processes.append(process)

            except ValueError as e:
                raise ValueError(f"Error procesando la fila {row}: {e}")

    processes.sort(key=lambda x: x["arrival"])
    return processes

