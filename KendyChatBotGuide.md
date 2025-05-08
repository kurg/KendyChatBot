KendyChatBot Guide

Introduction:
KendyChatBot helps track tasks, update activity logs, and retrieve important information from schedule.json.

Setup Instructions:
1. Open PowerShell and go to your chatbot folder:
   cd D:\KendyChatBot
2. Run:
   python update_tasks.py
   This displays your schedule.json data.

Core Functions:
- Update a task: python update_tasks.py "Task Name"
  Example: python update_tasks.py "Cycling"
- Retrieve tasks by date: python update_tasks.py get_tasks_by_date YYYY-MM-DD
- Retrieve tasks by category: python update_tasks.py get_tasks_by_category "Category Name"
- Get pending tasks: python update_tasks.py get_pending_tasks
- Check overdue tasks: python update_tasks.py check_reminders

Troubleshooting:
- If PowerShell says "Errno 2: No such file or directory," make sure you're inside D:\KendyChatBot
  cd D:\KendyChatBot
- If JSON errors occur:
  - Open schedule.json in Notepad.
  - Check commas and brackets for correctness.

Future Enhancements:
- Adding an "in progress" task feature.
- Advanced sorting options.

Conclusion:
Your chatbot is ready! Use this guide anytime you need help.
