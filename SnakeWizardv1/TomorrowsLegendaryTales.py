
from datetime import datetime
import uuid
from EmptyTitleOptions import Empty_Title
from TheWarders import DebugMessages
class TaskData:
    def __init__(self, task_id: str, task_name: str, task_date: str,
                 task_start_time: str, task_end_time: str, task_description: str, task_summary: str, task_tags: list[str] = [],
                 logger: DebugMessages, debug: bool = True):
        self.logger = logger
        self.debug = debug
        #Private Variable Declarations
        self._task_id: str = None
        self._task_name: str = None
        self._task_date: str = None
        self._task_start_time: str = None
        self._task_end_time: str = None
        self._task_description: str = None
        self._task_summary: str = None
        self._task_tags: list[str] = []
        #Assigning setters
        self.task_id = task_id
        self.task_name = task_name
        self.task_date = task_date
        self.task_start_time = task_start_time
        self.task_end_time = task_end_time
        self.task_description = task_description
        self.task_summary = task_summary
        self.task_tags = task_tags
    
    #Properties to Police Data
    @property #ID
    def task_id(self):
        return self._task_id
    @task_id.setter
    def task_id(self, id):
        try:
            uuid.UUID(id)
            self._task_id = id
        except ValueError: #If the value is not a valid UUID, generate a new one
            self.logger.log_error(1, "TaskData", id)
            self._task_id = TaskData.generate_id()

    @property #Title
    def task_name(self):
        return self._task_name
    @task_name.setter
    def task_name(self, title):
        title = (title or "").strip()
        title = title or Empty_Title()
        self._task_name = title[:80] #Change here for Title Length

    @property #Date
    def task_date(self):
        return self._task_date
    @task_date.setter
    def task_date(self, date):
        if not date:
            self._task_date = datetime.today().strftime('%Y-%m-%d')
        try:
            datetime.strptime(date, '%Y-%m-%d')
            self._task_date = date
        except ValueError:
            self._task_date = datetime.today().strftime('%Y-%m-%d')

    @property #Start Time
    def task_start_time(self):
        return self._task_start_time

    @task_start_time.setter
    def task_start_time(self, time):
        try:
            datetime.strptime(time, '%H:%M')
            self._task_start_time = time
            return
        except Exception:
            self.logger.log_error(4, "TaskData", time)
        if not time or ":" not in time:
            self._task_start_time = "00:00"
            return
        hour, *rest = time.split(":")
        try:
            hour_int = int(hour)
        except ValueError:
            hour_int = 0
        minutes_raw = rest[0] if rest and rest[0].isdigit() else "00"
        minutes_int = int(minutes_raw)
        self._task_start_time = f"{hour_int:02d}:{minutes_int:02d}"


    @property #End Time
    def task_end_time(self):
        return self._task_end_time
    @task_end_time.setter
    def task_end_time(self, time):
        try:
            datetime.strptime(time, '%H:%M')
            self._task_end_time = time
            return
        except Exception:
            self.logger.log_error(5, "TaskData", time)  # corrected error code

        if not time or ":" not in time:
            self._task_end_time = "00:00"
            return
        hour, *rest = time.split(":")
        try:
            hour_int = int(hour)
        except ValueError:
            hour_int = 0
        minutes_raw = rest[0] if rest and rest[0].isdigit() else "00"
        minutes_int = int(minutes_raw)
        self._task_end_time = f"{hour_int:02d}:{minutes_int:02d}"
    
    @property #Description
    def task_description(self):
        return self._task_description
    @task_description.setter
    def task_description(self, description):
        if description is None:
            description = ""  # allow empty strings
        try:
            description = str(description)
        except Exception as e:
            self.logger.log_error(3, "TaskData", str(e))
            description = ""
        self._task_description = description

    @property #Summary
    def task_summary(self):
        return self._task_summary
    @task_summary.setter
    def task_summary(self, summary):
        self._task_summary = str(summary or "")

    @staticmethod
    def generate_id(): #Generates a unique ID for each task
        return str(uuid.uuid4()) #Returns a unque string like a3d5f891-2c4b-4e8f-9a1b-3c6f4e5d6e7f--or something I havent actually checked the format, technically I never need to see it
    
    @property #Tags
    def task_tags(self):
        return self._task_tags
    @task_tags.setter
    def task_tags(self, tags):
        if tags is None:
            self._task_tags = []
            return
        if not isinstance(tags, list):
            self._task_tags = []
            return
        cleaned_tags = []
        for tag in tags:
            try:
                clean = str(tag).strip()
                if clean:
                    cleaned_tags.append(clean)
            except Exception:
                self.logger.log_error(12, "TaskData", str(tag))
                continue
        self._task_tags = cleaned_tags

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
            "task_start_time": self.task_start_time,
            "task_end_time": self.task_end_time,
            "task_description": self.task_description,
            "task_summary": self.task_summary,
            "task_tags": self.task_tags
        } #Basically labels the data

    @classmethod
    def from_dictionary(cls, data, logger:DebugMessages): #Creates a task from a dictionary which makes it easy to create objects from JSON later
        return cls(
            task_id=data["task_id"],
            task_name=data["task_name"],
            task_date=data["task_date"],
            task_start_time=data["task_start_time"],
            task_end_time=data["task_end_time"],
            task_description=data["task_description"],
            task_summary=data["task_summary"],
            task_tags=data.get("task_tags", []),
            
            logger=logger
        ) #Returns an instance of TaskData created from the dictionary
