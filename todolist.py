from datetime import datetime, timedelta
from dbtools import (get_engine, get_early_task, get_task,
                     insert_task, remove_task)

engine = None


def user_menu() -> int:
    """print user menu, wait command"""
    print("1) Today's tasks",
          "2) Week's tasks",
          "3) All tasks",
          "4) Missed tasks",
          "5) Add task",
          "6) Delete task",
          "0) Exit", sep='\n')
    command = ' '
    while command not in '0123456':
        command = input('>')
    return int(command)


def bye():
    """print 'Bye!'"""
    print('\nBye!')
    return False


def print_tasks(tasks):
    """print tasks by number"""
    if tasks:
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.task}")
        print()
    else:
        print("Nothing to do!\n")


def print_tasks_with_day(tasks):
    """print tasks by number with date in 'Day Month_abbreviated' format"""
    if tasks:
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.task}. {task.deadline.strftime('%d %b')}")
        print()
    else:
        print("Nothing to do!\n")


def today_tasks():
    """get task from db engine for deadline = today date"""
    # engine = get_engine()
    today = datetime.today()
    tasks = get_task(engine, deadline=today)
    print(f"\nToday {today.strftime('%d %b')}:")
    print_tasks(tasks)
    return True


def week_tasks():
    """"get tasks from db engine for current week"""
    day = datetime.today()
    for i in range(7):
        date = day + timedelta(days=i)
        tasks = get_task(engine, deadline=date)
        print(f"{date.strftime('%A %d %b')}")
        print_tasks(tasks)
    return True


def all_tasks():
    """get all tasks from db engine"""
    tasks = get_task(engine)
    print("All tasks:")
    print_tasks_with_day(tasks)
    return True


def missed_task():
    """get missed task with deadline earlier than today"""
    tasks = get_early_task(engine, datetime.today())
    print("Missed tasks:")
    print_tasks_with_day(tasks)
    return True


def enter_date():
    """input a date in string format YYYY-MM-DD"""
    print("\nEnter deadline")
    date_string = input(">")
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        # print("Can't date string format can be parsed")
        return datetime.today()
    else:
        return date


def add_task():
    print("\nEnter task")
    task = input(">")
    deadline = enter_date()
    # engine = get_engine()
    insert_task(engine, task, deadline)
    return True


def delete_task():
    """delete task from db engine by number"""
    tasks = get_task(engine)
    print("Choose the number of the task you want to delete:")
    print_tasks_with_day(tasks)
    task_number = int(input('>'))
    if 1 <= task_number <= len(tasks):
        remove_task(engine, tasks[task_number-1])
        # for i, task in enumerate(tasks):
        #     if i == task_number:
        #         remove_task(engine, task)
        #         break
        print("The task has been deleted!\n")
    return True


if __name__ == '__main__':
    menu = {
        0: bye,
        1: today_tasks,
        2: week_tasks,
        3: all_tasks,
        4: missed_task,
        5: add_task,
        6: delete_task}
    engine = get_engine()
    working = True
    while working:
        user_command = user_menu()
        select_command = menu[user_command]
        working = select_command()
