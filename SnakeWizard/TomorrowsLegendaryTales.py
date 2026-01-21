
from datetime import datetime
import uuid
from TheWarders import DebugMessages
class TaskData:
    def __init__(self, task_id: str, task_name: str, task_date: str,
                 start_time: str, end_time: str, description: str,
                 logger: DebugMessages, debug: bool = True):
        self.logger = logger
        self.debug = debug
        self._task_id: str = None
        self._task_name: str = None
        self._task_date: str = None
        self._start_time: str = None
        self._end_time: str = None
        self._description: str = None
        self.task_id = task_id
        self.task_name = task_name
        self.task_date = task_date
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
    
    # ======================== PROPERTIES FOR CONTINUOUS VALIDATION ========================#Assigns properties to each field with validation on call
    @property
    def task_id(self):
        return self._task_id
    @task_id.setter
    def task_id(self, value):
        self._validate_task_id(value)
        self._task_id = value

    @property
    def task_name(self):
        return self._task_name
    @task_name.setter
    def task_name(self, value):
        self._validate_task_name(value)
        self._task_name = value

    @property
    def task_date(self):
        return self._task_date
    @task_date.setter
    def task_date(self, value):
        self._validate_task_date(value)
        self._task_date = value

    @property
    def start_time(self):
        return self._start_time
    @start_time.setter
    def start_time(self, value):
        self._validate_start_time(value)
        self._start_time = value

    @property
    def end_time(self):
        return self._end_time
    @end_time.setter
    def end_time(self, value):
        self._validate_end_time(value)
        self._end_time = value

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        if value is None:
            value = ""  # allow empty strings
        self._validate_description(value)
        self._description = value

    # ======================== VALIDATION METHODS ========================

    def _validate_task_id(self, task_id: str):
        try:
            uuid.UUID(task_id)
        except ValueError:
            self.logger.log_error(1, "TaskData", task_id)

    def _validate_task_name(self, task_name: str):
        if not task_name.strip():
            self.logger.log_error(2, "TaskData", task_name)
        
    def _validate_task_date(self, task_date: str):
        try:
            datetime.strptime(task_date, '%Y-%m-%d')
        except ValueError:
            self.logger.log_error(3, "TaskData", task_date)

    def _validate_start_time(self, start_time: str):
        try:
           datetime.strptime(start_time, '%H:%M')
           return start_time
        except Exception:
            self.logger.log_error(4, "TaskData", start_time)
            if not start_time or ":" not in start_time:
                return "00:00"
            hour, *rest = start_time.split(":")
            try:
                hour_int=int(hour)
            except ValueError:
                hour_int=0
            minutes = rest[0] if rest and rest[0].isdigit() else "00"
            return f"{hour_int:02d}:{minutes:0>2}"

            
    def _validate_end_time(self, end_time: str) -> str:
        # Try to parse valid HH:MM format
        try:
            datetime.strptime(end_time, '%H:%M')
            return end_time  # already valid
        except Exception:
            # Log the malformed input
            self.logger.log_error(5, "TaskData", end_time)

            # Normalize malformed values
            if not end_time or ":" not in end_time:
                return "00:00"

            hour, *rest = end_time.split(":")

            # Parse hour safely
            try:
                hour_int = int(hour)
            except ValueError:
                hour_int = 0

            # Parse minutes safely
            minutes = rest[0] if rest and rest[0].isdigit() else "00"

        # Return normalized HH:MM
        return f"{hour_int:02d}:{minutes:0>2}"

    def _validate_description(self, description: str):
        if not isinstance(description, str):
            self.logger.log_error(7, "TaskData", description)

    @staticmethod
    def generate_id(): #Generates a unique ID for each task
        return str(uuid.uuid4()) #Returns a unque string like a3d5f891-2c4b-4e8f-9a1b-3c6f4e5d6e7f--or something I havent actually checked the format, technically I never need to see it
    #g
    
    
    @staticmethod
    def time_format(date_str,start_str,end_str): #(2024-06-15, 14:00, 15:00) takes in date time strings, returns datetime objects
        start=datetime.strptime(date_str + ' ' + start_str, '%Y-%m-%d %H:%M') #Example: Date String + Start Time String
        end=datetime.strptime(date_str + ' ' + end_str, '%Y-%m-%d %H:%M')   #Date String + End Time String
        return start,end

    def to_dictionary(self): #Puts task instance into a dictionary
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_date": self.task_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": self.description
        } #Basically labels the data

    @classmethod
    def from_dictionary(cls, data, logger:DebugMessages): #Creates a task from a dictionary which makes it easy to create objects from JSON later
        return cls(
            task_id=data["task_id"],
            task_name=data["task_name"],
            task_date=data["task_date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            description=data["description"],
            logger=logger
        ) #Returns an instance of TaskData created from the dictionary
    def return_task(self): #Returns a print string with all task info
        return f"Task: {self.task_name}, Date: {self.task_date}, {self.start_time} - {self.end_time}, Description: {self.description}"

