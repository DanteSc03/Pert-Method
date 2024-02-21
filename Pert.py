
import math
import pandas as pd


def pert(tasks, dependencies):
    task_data={}
    #Calculate the expected time, variance and standard deviation of each task
    for task, times in tasks.items():
        O, P, M = times
        expected_time = (O + M*4 + P)/6
        variance = ((P-O)**2)/36
        standard_deviation = math.sqrt(variance)
        # Convert to float and round to two
        float(expected_time)
        float(variance)
        float(standard_deviation)
        expected_time = round(expected_time, 2)
        variance = round(variance, 2)
        standard_deviation = round(standard_deviation, 2)
        # Add the task data to the currently empty dictionary
        task_data[task] = {
            "expected_time": float(expected_time),
            "variance": float(variance),
            "standard_deviation": float(standard_deviation),
            "earliest_start": 0,
            "latest_start": None,
            "earliest_finish": float(expected_time),
            "latest_finish": None,
            "slack": 0
        }


    dependencies = {key: [dep] if isinstance(dep, str) else dep for key, dep in dependencies.items()}
    #Calculate the earliest start and earliest finish of each task
    for _ in range(len(task_data)):
        for task in task_data:
            if task in dependencies:
                earliest_start = max([task_data[dep]["earliest_finish"] for dep in dependencies[task]], default=0)
                task_data[task]["earliest_start"] = earliest_start
                task_data[task]["earliest_finish"] = earliest_start + task_data[task]["expected_time"]

    project_duration = max(task_data[task]["earliest_finish"] for task in task_data)


    for task in task_data:
        task_data[task]["latest_finish"] = project_duration

    # Calculate the latest start, finish and slack of each task
    for _ in range(len(task_data)):
        for task in task_data:
            if task not in dependencies or not dependencies[task]:
                continue
            for dep in dependencies[task]:
                task_data[dep]["latest_finish"] = min(task_data[dep]["latest_finish"], task_data[task]["earliest_start"])
                task_data[dep]["latest_start"] = task_data[dep]["latest_finish"] - task_data[dep]["expected_time"]
                task_data[dep]["slack"] = task_data[dep]["latest_start"] - task_data[dep]["earliest_start"]


    return task_data

#Define the tasks
tasks = {
    "A": (2, 8, 5),
    "B": (3, 10, 4),
    "C": (5, 10, 6),
    "D": (1, 10, 4),
    "E": (2, 9, 5),
    "F": (3, 8, 4),
}

# Define the dependencies
dependencies = {
    "A": [],
    "B": [],
    "C": "A",
    "D": "B",
    "E": ["C"],
    "F": ["D"],
}

results = pert(tasks, dependencies)


#Print the results
results_df = pd.DataFrame.from_dict(results, orient='index')
print(results_df)

results_df.to_csv('results.csv')

