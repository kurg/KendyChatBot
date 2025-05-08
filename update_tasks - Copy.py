from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import logging
from datetime import datetime, timedelta
import sys
import torch

logging.basicConfig(level=logging.INFO, format="%(message)s")

# Load DialoGPT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

chat_history_ids = None  # Stores conversation history

def load_tasks(filename):
    with open(filename, "r") as file:
        return json.load(file)

def save_tasks(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def mark_in_progress(filename, task_name):
    """Update a task's status to 'in progress'."""
    tasks_data = load_tasks(filename)

    for task in tasks_data["tasks"]:
        if task["name"].lower() == task_name.lower():
            task["status"] = "in progress"
            logging.info(f"🚀 Task '{task_name}' is now in progress!")
            save_tasks(filename, tasks_data)
            return

    logging.info(f"❌ Task '{task_name}' not found!")

def update_task(filename, task_name):
    """Mark a task as completed."""
    tasks_data = load_tasks(filename)
    today = datetime.today().strftime("%Y-%m-%d")

    for task in tasks_data["tasks"]:
        if task["name"].lower() == task_name.lower():
            if task["status"] == "in progress":
                task["history"].append(today)
                task["status"] = "completed"
                logging.info(f"✅ '{task_name}' marked as completed on {today}")
                save_tasks(filename, tasks_data)
                return
            else:
                logging.info(f"⚠ '{task_name}' is not in progress yet!")
                return

    logging.info(f"❌ Task '{task_name}' not found!")

def get_tasks_by_date(filename, date):
    """Retrieve tasks completed on a specific date."""
    tasks_data = load_tasks(filename)
    tasks_on_date = [task for task in tasks_data["tasks"] if date in task.get("history", [])]
    return tasks_on_date if tasks_on_date else f"No tasks recorded for {date}."

def get_tasks_by_category(filename, category):
    """Retrieve tasks that belong to a specific category."""
    tasks_data = load_tasks(filename)
    tasks_in_category = [task for task in tasks_data["tasks"] if task["category"].lower() == category.lower()]
    return tasks_in_category if tasks_in_category else f"No tasks found in the category '{category}'."

def get_pending_tasks(filename):
    """Retrieve all tasks that are still pending."""
    tasks_data = load_tasks(filename)
    pending_tasks = [task for task in tasks_data["tasks"] if task["status"].lower() == "pending"]
    return pending_tasks if pending_tasks else "✅ No pending tasks!"

def get_in_progress_tasks(filename):
    """Retrieve all tasks that are in progress."""
    tasks_data = load_tasks(filename)
    in_progress_tasks = [task for task in tasks_data["tasks"] if task["status"].lower() == "in progress"]
    return in_progress_tasks if in_progress_tasks else "✅ No tasks in progress!"

def get_all_tasks_sorted(filename):
    """Retrieve all tasks sorted by last done date."""
    tasks_data = load_tasks(filename)

    # Extract last done date (if available)
    def last_done_date(task):
        return max(task["history"], default="2000-01-01")  # Defaults to very old date if no history

    # Sort tasks by last completion date (most recent first)
    sorted_tasks = sorted(tasks_data["tasks"], key=last_done_date, reverse=True)

    return sorted_tasks if sorted_tasks else "❌ No tasks found!"

def get_chatbot_response(user_input):
    """Generates a chatbot response using DialoGPT."""
    global chat_history_ids

    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    response_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    chat_history_ids = response_ids  # Update history
    return response

# Execute commands
if __name__ == "__main__":
    filename = "schedule.json"

    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])  # Capture full user input

        # Task-related commands
        if command.lower().startswith("get_tasks_by_date"):
            date_requested = command.split(" ", 1)[1]
            print(get_tasks_by_date(filename, date_requested))
        elif command.lower().startswith("get_tasks_by_category"):
            category_requested = command.split(" ", 1)[1]
            print(get_tasks_by_category(filename, category_requested))
        elif command.lower() == "get_pending_tasks":
            print(get_pending_tasks(filename))
        elif command.lower() == "get_in_progress_tasks":
            print(get_in_progress_tasks(filename))
        elif command.lower() == "get_all_tasks_sorted":
            print(get_all_tasks_sorted(filename))
        elif command.lower().startswith("mark_in_progress"):
            task_requested = command.split(" ", 1)[1]
            mark_in_progress(filename, task_requested)
        else:
            update_task(filename, command)

    else:
        # If no known task command is recognized, treat input as a chatbot query
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("👋 Chatbot: Goodbye!")
                break
            print(f"🤖 Chatbot: {get_chatbot_response(user_input)}")