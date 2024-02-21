
import math
import pandas as pd

def pert(tasks, dependencies):
    task_data={}
    #Calculate the expected time, variance and standard deviation of each task
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

    #Calculate the earliest start and earliest finish of each task
    for _ in range(len(task_data)):
        for task, dependent_tasks in dependencies.items():
            for dependent_task in dependent_tasks:
                if task_data[task]["earliest_finish"] < task_data[dependent_task]["earliest_start"]:
                    task_data[dependent_task]["earliest_start"] = task_data[task]["earliest_finish"] 
                task_data[dependent_task]["earliest_finish"] = max(task_data[dependent_task]["earliest_start"] + task_data[dependent_task]["expected_time"], task_data[task]["earliest_finish"])

    #Calculate the latest start, latest finish and slack of each task
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
            task_data[dependent_task]["slack"] = round(task_data[dependent_task]["slack"], 2)

    return task_data

#Definir las tareas
tasks = {}
dependencies = {}
number_of_tasks = int(input("Enter the number of tasks you have: "))
for i in range(number_of_tasks):
    task = input("Enter the name of the task(ex: A, B): ")
    optimistic_time = float(input("Enter the optimistic time: "))
    pessimistic_time = float(input("Enter the pessimistic time: "))
    most_likely_time = float(input("Enter the most likely time: "))
    tasks[task] = [optimistic_time, pessimistic_time, most_likely_time]

# Definir las dependencias de cada tarea
for task in tasks:
    number_of_dependencies = int(input(f"Enter the number of dependencies of task {task}: "))
    dependencies[task] = []
    for i in range(number_of_dependencies):
        dependency = input(f"Enter the name of the dependency {i+1}: ")
        dependencies[task].append(dependency)

results = pert(tasks, dependencies)



# Print the Results
results_df = pd.DataFrame.from_dict(results, orient='index')
print(results_df)
