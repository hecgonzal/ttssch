from TheWarders import DebugMessages
from datetime import datetime
from JSONdsOfTime import JSONHandler
from TomorrowsLegendaryTales import TaskData

class TaskController: #Class to manage task retrival, removal, and storage. Knows about other JSON Handler and DailyTasks classes, but is unkown to everything
    def __init__(self,logger:DebugMessages):
        self.tasks={} #Dictionary to hold tasks, task_id as the key, DailyTasks object as the value
        self.logger=logger
        self.error_type = "Object"
        self.log_type = "Object"        
class ObjectManipulation(TaskController):
    def __init__(self, logger: DebugMessages, json_handler: JSONHandler):
        super().__init__(logger)
        self.storage = json_handler


    def remove_task(self,task_id):
        if task_id in self.tasks: #checks if task_id exists in the tasks dictionary, this pervents a KeyError if the task_id is not found
            del self.tasks[task_id] #Deletes the task with the given task_id from the tasks dictionary
            self.logger.log_process(4, self.log_type, task_id)
            return True
        self.logger.log_error(1, self.error_type, task_id)
        return False #By returning flase, we can easily loop and have a user try again
    
    def add_task(self,task): #Adds a task to the current task object dictionary
        if task.task_id in self.tasks:
            self.logger.log_error(8, "TaskData", task.task_id)  # Duplicate Task ID
            return False
        self.tasks[task.task_id] = task
        try:
            self.storage.save_all_tasks(self.tasks.values())  # Save current tasks before adding new one
            self.logger.log_process(3, self.log_type, len(self.tasks))
        except Exception as e:
            self.logger.log_error(3, self.error_type, str(e))
    def create_task_manual(self):
        while True:
            task_name = input("Enter a task name: ").strip()
            if task_name:
                break
            print("Task name cannot be empty.")
        while True: #loops until the user can type in a proper date
            task_date = input("Enter task date (YYYY-MM-DD) or leave blank for today: ").strip()
            if task_date == "":
                task_date = datetime.today().strftime("%Y-%m-%d")
                print(f"Using today's date: {task_date}")
                break
            try:
                dt_check = datetime.strptime(task_date, "%Y-%m-%d")
                if dt_check.date() < datetime.today().date():
                    print("Task date cannot be in the past.")
                    continue
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
        while True: #loop until user gives proper time; loop minimizes repitition of data entry which is my biggest annoyance with schedulers
            start_time = input("Enter start time (HH:MM): ")
            try:
                datetime.strptime(f"{task_date} {start_time}", "%Y-%m-%d %H:%M")
                break
            except ValueError:
                print("Invalid time format. Use HH:MM.")
        while True: # Loop until we get a valid time that's after start time
            end_time = input("Enter end time (HH:MM): ").strip()
            try:
                # Parse end time the same way
                end_dt = datetime.strptime(f"{task_date} {end_time}", "%Y-%m-%d %H:%M")
                start_dt = datetime.strptime(f"{task_date} {start_time}", "%Y-%m-%d %H:%M")
                # Check that end time is after start time
                if end_dt <= start_dt:  # <= means "less than or equal to"
                    print("End time must be after start time. Try again.")
                    continue  # Ask for end time again
                break  # Exit loop
            except ValueError:
                print("Invalid time format. Please use HH:MM.")
        while True: # Loop until we get a non-empty description
            description = input("Enter a description: ").strip()
            if description:
                break
            print("Description cannot be empty.")

        task_id = TaskData.generate_id()
        try:
            task = TaskData(
                task_id=task_id,
                task_name=task_name,
                task_date=task_date,
                start_time=start_time,
                end_time=end_time,
                description=description,
                logger=self.logger
            )
        except ValueError as ve:
            print(f"Unexpected error creating task: {ve}, back to coding")
        self.add_task(task)
        self.logger.log_process(5, self.log_type, f"{task_name} ({task_id}) created.")
        return task
       
    def edit_task(self, task_id: str, field_name: str, new_value):
        if task_id not in self.tasks:
            self.logger.log_error(1, self.error_type, task_id)  # Task ID not found
            return False
        task = self.tasks[task_id]
        editable_fields = {
            "task_name": "task_name",
            "task_date": "task_date",
            "start_time": "start_time",
            "end_time": "end_time",
            "description": "description"
        }
        if field_name not in editable_fields:
            self.logger.log_error(6, self.error_type, field_name)
            return False
        try:
            setattr(task, editable_fields[field_name], new_value) # Set the new value; triggers validation in TaskData properties
            self.logger.log_process(5, self.log_type, f"Task {task_id} updated: {field_name} -> {new_value}")
            return True
        except Exception as e:
            self.logger.log_error(3, self.error_type, str(e))
            return False    
class ObjectOrganization(TaskController):
    def get_tasks(self, task_ids=None, return_as_dict=False): #returns list of task objects. If task_ids is None, returns all tasks
        if task_ids is None:
            result_dict = self.tasks.copy()
            self.logger.log_process(2, self.log_type, f"Retrieved all {len(result_dict)} tasks.")
            return result_dict if return_as_dict else list(result_dict.values())
        if isinstance(task_ids, str):
            task_ids = [task_ids]
        result_dict = {}
        for tid in task_ids:
            if tid in self.tasks:
                result_dict[tid] = self.tasks[tid]
            else:
                self.logger.log_error(1, self.error_type, tid)  # log missing task_id

        self.logger.log_process(2, self.log_type, f"Retrieved {len(result_dict)} of {len(task_ids)} requested tasks.")
        return result_dict if return_as_dict else list(result_dict.values())
    def sort_tasks(self,tasks, key): #logic for options to return a sorted list of task objects based on user choice
        if key == "datetime":
            return sorted(tasks, key=lambda t: (t.task_date, t.start_time))
        elif key == "date":
            return sorted(tasks, key=lambda t: t.task_date)
        elif key == "taskname":
            return sorted(tasks, key=lambda t: t.task_name.lower())
        elif key == "starttime":
            return sorted(tasks, key=lambda t: t.start_time)
        elif key == "endtime":
            return sorted(tasks, key=lambda t: t.end_time)
        else:
            self.logger.log_error(10, self.error_type,key)
            return list(tasks)  # Return unsorted if invalid key

    def detect_conflicts(self, task, ignore_id: str | None = None) -> list[str]:
        conflicts: list[str] = []
        try:
            task_start, task_end = TaskData.time_format(task.task_date, task.start_time, task.end_time)
        except Exception:
            return conflicts
        for other_id, other in self.tasks.items():
            if ignore_id and other_id == ignore_id:
                continue
            if other.task_date != task.task_date:
                continue
            try:
                other_start, other_end = TaskData.time_format(
                    other.task_date, other.start_time, other.end_time
                )
            except Exception:
                continue

            # Core overlap logic
            if task_start < other_end and other_start < task_end:
                conflicts.append(other_id)

        return conflicts

    def sync_tasks(self, tasks: list[TaskData]) -> None:
        tasks= list(tasks)
        if not tasks: #prevents sync from clearing all tasks if an empty list is passed
            return
        self.tasks.clear()
        for task in tasks:
            self.tasks[task.task_id] = task
    def export_tasks(self) -> list[TaskData]:
        return list(self.tasks.values())  

    def search_tasks(self, keywords: str | list[str], mode: str = "any") -> list[str]: #Searches tasks for keywords, returns list of matching task IDs
        if not keywords:
            return []
        if isinstance(keywords, str):
                keywords = [keywords.lower()]
        else:
                keywords = [k.lower() for k in keywords]
        TaskSearchResult = []
        for task_id, task in self.tasks.items():
            task_text = (
                f"{task.task_name} "
                f"{task.task_date} "
                f"{task.start_time} "
                f"{task.end_time} "
                f"{task.description}"
            ).lower()
            if mode == "all":
                if all(k in task_text for k in keywords):
                    TaskSearchResult.append(task_id)
            elif mode == "any":
                if any(k in task_text for k in keywords):
                    TaskSearchResult.append(task_id)
        return TaskSearchResult