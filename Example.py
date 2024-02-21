
import math

def pert(tasks, dependencies):
    task_data={}
    #Calcular el tiempo esperado de cada tarea y su varianza
    for task, (o,p,m) in tasks.items():
        tiempo_esperado = (o + 4*m + p)/6
        varianza = (m-o)**2/36
        task_data[task] = {
            "tiempo_esperado": float(tiempo_esperado),
            "varianza": float(varianza),
            "empiezo_mas_temprano": 0,
            "empiezo_mas_tarde": 24,
            "termino_mas_temprano": float(tiempo_esperado),
            "termino_mas_tarde": 24,
            "holgura": 0
        }

    #Calcular el empiezo mas temprano y el termino mas temprano de cada tarea
    for _ in range(len(task_data)):
        for task, dependent_tasks in dependencies.items():
            for dependent_task in dependent_tasks:
                if task_data[task]["empiezo_mas_temprano"] < task_data[dependent_task]["termino_mas_temprano"]:
                    task_data[dependent_task]["empiezo_mas_temprano"] = task_data[task]["termino_mas_temprano"] 
                task_data[dependent_task]["termino_mas_temprano"] = max(task_data[dependent_task]["empiezo_mas_temprano"] + task_data[dependent_task]["tiempo_esperado"], task_data[task]["termino_mas_temprano"])

    #Calcular el empiezo mas tarde, el termino mas tarde y la holgura de cada tarea
    for task in reversed(sorted(task_data, key=lambda x: task_data[x]["termino_mas_temprano"])):
        if not dependencies.get(task):
            task_data[task]["termino_mas_tarde"] = task_data[task]["termino_mas_temprano"]
            task_data[task]["empiezo_mas_tarde"] = task_data[task]["termino_mas_tarde"] - task_data[task]["tiempo_esperado"]
        for dependent_task in dependencies.get(task, []):
            task_data[dependent_task]["termino_mas_tarde"] = min(
                task_data[dependent_task]["termino_mas_tarde"], 
                task_data[task]["empiezo_mas_tarde"]
            )
            task_data[dependent_task]["empiezo_mas_tarde"] = task_data[dependent_task]["termino_mas_tarde"] - task_data[dependent_task]["tiempo_esperado"]
            task_data[dependent_task]["holgura"] = task_data[dependent_task]["empiezo_mas_tarde"] - task_data[dependent_task]["empiezo_mas_temprano"]

    return task_data

#Definir las tareas y las dependencias de cada tarea
tasks = {
    "A": (3,7,5),
    "B": (2,6,4),
    "C": (4,8,6),
    "D": (2,6,4),
    "E": (3,7,5),
    "F": (2,6,4),
}

dependencies = {
    "A": [],
    "B": ["A"],
    "C": ["A"],
    "D": ["B"],
    "E": ["C"],
    "F": ["D","E"],
}

results = pert(tasks, dependencies)

for task, data in results.items():
    print(f"Tarea: {task}")
    print(f"Tiempo esperado: {data['tiempo_esperado']}")
    print(f"Varianza: {data['varianza']}")
    print(f"Empiezo mas temprano: {data['empiezo_mas_temprano']}")
    print(f"Empiezo mas tarde: {data['empiezo_mas_tarde']}")
    print(f"Termino mas temprano: {data['termino_mas_temprano']}")
    print(f"Termino mas tarde: {data['termino_mas_tarde']}")
    print(f"Holgura: {data['holgura']}")
    print("\n")
