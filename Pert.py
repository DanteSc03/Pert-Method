
import math

def pert(tasks, dependencies):
    task_data={}
    #Calcular el tiempo esperado de cada tarea y su variance
    for task, times in tasks.items():
        O, P, M = times
        expected_time = (O + M*4 + P)/6
        float(expected_time)
        expected_time = round(expected_time, 2)
        variance = ((P-O)**2)/36
        float(variance)
        variance = round(variance, 2)
        standard_deviation = math.sqrt(variance)
        float(standard_deviation)
        standard_deviation = round(standard_deviation, 2)
        task_data[task] = {
            "expected_time": float(expected_time),
            "variance": float(variance),
            "standard_deviation": float(standard_deviation),
            "earliest_start": 0,
            "latest_start": 30,
            "earliest_finish": float(expected_time),
            "latest_finish": 30,
            "slack": 0
        }

    #Calcular el empiezo mas temprano y el termino mas temprano de cada tarea
    for _ in range(len(task_data)):
        for task, dependent_tasks in dependencies.items():
            for dependent_task in dependent_tasks:
                if task_data[task]["earliest_start"] < task_data[dependent_task]["earliest_finish"]:
                    task_data[dependent_task]["earliest_start"] = task_data[task]["earliest_finish"] 
                task_data[dependent_task]["earliest_finish"] = max(task_data[dependent_task]["earliest_start"] + task_data[dependent_task]["expected_time"], task_data[task]["earliest_finish"])

    #Calcular el empiezo mas tarde, el termino mas tarde y la slack de cada tarea
    for task in reversed(sorted(task_data, key=lambda x: task_data[x]["earliest_finish"])):
        if not dependencies.get(task):
            task_data[task]["latest_finish"] = task_data[task]["earliest_finish"]
            task_data[task]["latest_start"] = task_data[task]["latest_finish"] - task_data[task]["expected_time"]
        for dependent_task in dependencies.get(task, []):
            task_data[dependent_task]["latest_finish"] = min(
                task_data[dependent_task]["latest_finish"], 
                task_data[task]["latest_start"]
            )
            task_data[dependent_task]["latest_start"] = task_data[dependent_task]["latest_finish"] - task_data[dependent_task]["expected_time"]
            task_data[dependent_task]["slack"] = task_data[dependent_task]["latest_start"] - task_data[dependent_task]["earliest_start"]

    return task_data

#Definir las tareas
tasks = {
    "A": (2, 7, 5),
    "B": (3, 6, 4),
    "C": (5, 8, 6),
    "D": (1, 6, 4),
    "E": (2, 7, 5),
    "F": (3, 6, 4),
}

# Definir las dependencias de cada tarea
dependencies = {
    "A": [],
    "B": ["A"],
    "C": ["A"],
    "D": ["B"],
    "E": ["C"],
    "F": ["D","E"],
}

results = pert(tasks, dependencies)

print(results)

for task, data in results.items():
    print(f"Task: {task}")
    print(f"Expected Time: {data['expected_time']}")
    print(f"Variance: {data['variance']}")
    print(f"Standard Deviation: {data['standard_deviation']}")
    print(f"Earliest Start: {data['earliest_start']}")
    print(f"Latest Start: {data['latest_start']}")
    print(f"Earliest Finish: {data['earliest_finish']}")
    print(f"Latest Finish: {data['latest_finish']}")
    print(f"Slack: {data['slack']}")
    print("\n")
