## Import modules
import time
import json
from datetime import datetime
import winsound

## Function to play sound
def play_sound():
    winsound.PlaySound("MyBeep.wav", winsound.SND_FILENAME)

## Ask for name if first use and remember it
user_name = input("Please enter your name: ")
try:
    with open("user_name.txt", "r") as file:
        user_name = file.read().strip()
except FileNotFoundError:
    user_name = input("It seems this is your first time using the program. Please enter your name: ")
    with open("user_name.txt", "w") as file:
        file.write(user_name)

## Welcoming the User
print(f"Hey {user_name}! Welcome to the Task Timer!")

## only show the text for the first time
try:
    with open("first_time.txt", "r") as file:
        first_time = file.read().strip()
except FileNotFoundError:
    print("This program will help you track the time you spend on different tasks.")
    with open("first_time.txt", "w") as file:
        file.write("not_first_time")

## Divinding the texts
print("--" * 50)

## The three functions

print("Please enter the letter associated with the action you want to take: /n")

print("A.Start a new task")
print("B.View today's summary")
print("C.Exit")

action = input("Enter your choice (A/B/C): ").strip().upper()

## First function
def start_new_task():
    task_name = input("Enter the name of the task: ")
    task_duration = int(input("Enter the duration of the task in minutes: "))
    print(f"Task '{task_name}' started for {task_duration} minutes.")
    print(start_timer(task_duration * 60))
    play_sound()
    print(f"Task '{task_name}' completed.")
    # Log the task
    log_entry = {
        "task_name": task_name,
        "task_duration": task_duration,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open("task_log.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(log_entry)

    with open("task_log.json", "w") as file:
        json.dump(data, file, indent=4)

## 2nd Function: View today's summary
def view_summary():
    try:
        with open("task_log.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No task log found.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    total_duration = 0
    tasks_today = []

    for entry in data:
        if entry["start_time"].startswith(today):
            tasks_today.append(entry)
            total_duration += entry["task_duration"]

    if tasks_today:
        print(f"Tasks completed today ({today}):")
        for task in tasks_today:
            print(f"- {task['task_name']} for {task['task_duration']} minutes")
        print(f"Total time spent today: {total_duration} minutes")
    else:
        print("No tasks completed today.")

## Exit function
def exit_program():
    print("Thank you for using the Task Timer. Goodbye!")
    exit()

## Start the timer
def start_timer(duration):
    for x in range(duration, 0, -1):
        seconds = x % 60
        minutes = int(x / 60) % 60
        hours = int(x / 3600)
        print(f"Time left: {hours:02d}:{minutes:02d}:{seconds:02d}", end="\r")
        time.sleep(1)


## Executing Functions
if action == "A":
    start_new_task()
elif action == "B":
    view_summary()