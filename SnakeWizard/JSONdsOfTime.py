import os
import json
from typing import List

from TheWarders import DebugMessages
from TomorrowsLegendaryTales import TaskData


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(SCRIPT_DIR, "test_tasks.json")

class JSONHandler:  # Manages Saving and Loading from JSON
    def __init__(self, logger: DebugMessages):
        self.filename = TASKS_FILE
        self.logger = logger 
        self.error_type = "JSONHandler"
        self.log_type = "JSONHandler"

    def save_all_tasks(self, tasks: List['TaskData']):
        try:
            data = [task.to_dictionary() for task in tasks]
            filepath = os.path.abspath(self.filename)
            file_exists = os.path.exists(filepath)
            self.logger.log_process(4, self.log_type, filepath)  # attempting save
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            file_size = os.path.getsize(filepath)
            if not file_exists:
                self.logger.log_process(5, self.log_type, filepath)  # new file created
            self.logger.log_process(7, self.log_type, len(tasks), filepath, file_size)  # tasks saved
        except PermissionError as e:
            self.logger.log_error(1, self.error_type, str(e))  # failed to save tasks
            raise
        except IOError as e:
            self.logger.log_error(4, self.error_type, str(e))  # I/O error
            raise
        except Exception as e:
            self.logger.log_error(5, self.error_type, str(e))  # unexpected error
            raise

    def load_all_tasks(self) -> List['TaskData']:
        tasks: List['TaskData'] = []
        filepath = os.path.abspath(self.filename)
        try:
            self.logger.log_process(3, self.log_type, filepath)  # attempting load
            if not os.path.exists(filepath):
                self.logger.log_process(5, self.log_type, filepath)  # no file found
                return tasks
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for item in data:
                try:
                    task = TaskData.from_dictionary(item, self.logger)
                    tasks.append(task)
                except ValueError as ve:
                    self.logger.log_error(1, "TaskData", ve)
                    continue
            file_size = os.path.getsize(filepath)
            self.logger.log_process(6, self.log_type, len(tasks), filepath, file_size)  # loaded successfully
            return tasks
        except json.JSONDecodeError as e:
            self.logger.log_error(3, self.error_type, str(e))
            raise
        except IOError as e:
            self.logger.log_error(4, self.error_type, str(e))
            raise
        except Exception as e:
            self.logger.log_error(5, self.error_type, str(e))
            raise