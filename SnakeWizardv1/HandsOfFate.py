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

    def edit_task(self, task_id: str, field_name: str, new_value):
        if task_id not in self.tasks:
            self.logger.log_error(1, self.error_type, task_id)  # Task ID not found
            return False
        task = self.tasks[task_id]
        editable_fields = {
            "task_name": "task_name",
            "task_date": "task_date",
            "task_start_time": "task_start_time",
            "task_end_time": "task_end_time",
            "task_description": "task_description",
            "task_summary": "task_summary"
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
    def sync_tasks(self, tasks: list[TaskData]) -> None:
            tasks= list(tasks)
            if not tasks: #prevents sync from clearing all tasks if an empty list is passed
                return
            self.tasks.clear()
            for task in tasks:
                self.tasks[task.task_id] = task
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

    def detect_conflicts(self, task, ignore_id: str | None = None) -> list[str]:
        conflicts: list[str] = []
        try:
            task_start, task_end = TaskData.time_format(
                task.task_date,
                task.task_start_time,
                task.task_end_time
            )
        except Exception:
            return conflicts

        for other_id, other in self.tasks.items():
            if ignore_id and other_id == ignore_id:
                continue
            if other.task_date != task.task_date:
                continue
            try:
                other_start, other_end = TaskData.time_format(
                    other.task_date,
                    other.task_start_time,
                    other.task_end_time
                )
            except Exception:
                continue

            # Core overlap logic
            if task_start < other_end and other_start < task_end:
                conflicts.append(other_id)

        return conflicts

    def export_tasks(self) -> list[TaskData]:
        return list(self.tasks.values())  
