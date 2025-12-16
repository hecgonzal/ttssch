import re #Currently unused, may be useful for input validation later
import uuid
from datetime import datetime

class DailyTasks: #Class for an individual task, purely a data structure. TaskControler will manage these objects
    #I am adding validation for date and time inputs here for several reason:
    #Prevents imported files from containting old and useless events
    #Avoids me typing in a validation everytime data is called

    def __init__(self,task_id,task_name,task_date, start_time, end_time, description): #Intialize all parts of the task we need stored
        start_dt = datetime.strptime(f"{task_date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{task_date} {end_time}", "%Y-%m-%d %H:%M")
        if end_dt <= start_dt:
            raise ValueError("End time must be after start time.")
        dt_check = datetime.strptime(task_date, "%Y-%m-%d")
        if dt_check.date() < datetime.today().date():
            raise ValueError("Task date cannot be in the past.")
        self.task_id = task_id #EX: "a3d5f891-2c4b-4e8f-9a1b-3c6f4e5d6e7f", unquie identifier for each task so that one can actually be removed, called, or modified. Dictionary key.
        self.task_name = task_name #EX: "Go to the Gym", name of each task, since this wont be index does not need to be unique
        self.task_date = task_date #EX: "2024-06-15", pretty self explanatory, will be modified into datetime object later for data validation
        # converted to datetime only when doing comparisons or validation
        self.start_time = start_time #EX: "14:00", start time of task, may adjust formatting, currently unsure of best way to take time inputs (24hr vs am/pm, not sure if restricting user input expentesvely is a good idea)
        self.end_time = end_time #EX: "15:00"
        self.description = description #EX: "Leg day at the gym"

    @staticmethod #If a method doesnt touch object state, make it static
    def generate_id(): #Generates a unique ID for each task
        return str(uuid.uuid4()) #Returns a unque string like a3d5f891-2c4b-4e8f-9a1b-3c6f4e5d6e7f--or something I havent actually checked the format, technically I never need to see it
    #gives flexibility for storing data on device or potentially in a cloud if I wanna get fancy
    
    
    @staticmethod #Note to self, instance methods modify an object state, class methods modify a class state, and static methods are just functions inside a class
    def time_format(date_str,start_str,end_str): #Formats time strings into datetime objects
    #Single source for time parsing which means any problems with time formatting can be fixed here and avoids duplication
        start=datetime.strptime(date_str + ' ' + start_str, '%Y-%m-%d %H:%M') #Date String + Start Time String
        end=datetime.strptime(date_str + ' ' + end_str, '%Y-%m-%d %H:%M')   #Date String + End Time String
        return start,end

    def to_dictionary(self): #Translates task info into dictionary which makes adding to JSON later easier. Dict for storage, list for exposure
        #Objects are for python to adjust, lists and dicts are for moving data around
        #ANY PROBLEMS WITH JSON SERIALIZATION CAN BE FIXED HERE (probably)
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "task_date": self.task_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "description": self.description
        } #Returns {'task id': '...', 'task_name': '...', 'task_date': '...', 'start_time': '...', 'end_time': '...', 'description': '...'}

    @classmethod #Gives function access to the class variables (like task_id, task_name, etc)
    def from_dictionary(cls, data): #Creates a task from a dictionary which makes it easy to create objects from JSON later
        return cls(
            task_id=data["task_id"],
            task_name=data["task_name"],
            task_date=data["task_date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            description=data["description"]
        ) #Returns an instance of DailyTasks created from the dictionary
    
    def test_task(self): #For debug purposes, returns a string with all task info
        return f"Task: {self.task_name}, Date: {self.task_date}, {self.start_time} - {self.end_time}, Description: {self.description}"


class TaskControler: #Class to manage task retrival, removal, and storage
    def __init__(self):
        self.tasks={} #Dictionary to hold tasks, task_id as the key, DailyTasks object as the value
   
   
    #--------CRUD Operations--------#
    def add_task(self,task):
        self.tasks[task.task_id] = task #Adds a task to the dictionary with task_id as key and overwrites if the key somehow already exists
        #key=task.task_id
        #value=task DailyTasks object

    def get_task(self,task_id):
        return self.tasks.get(task_id) #Returns the task with the given task_id or None if not found (used .get() to avoid KeyError in the case of a missing task)

    def get_all_tasks(self):
        return list(self.tasks.values()) #Returns list of all task objects stored in the tasks dictionary did this for a few reasons
    #self.tasks.values() returns a view object that displays a list of all the values in the dictionary
    #By converting it to a list, we get data that is more flexible for saving to JSON
    #Example json.dumps(self.tasks.values()) would raise a TypeError because view objects are not directly serializable to JSON
    #Where as json.dumps(list(self.tasks.values())) works perfectly fine
    #GPT summary of reasons:
    # Returns a list to:
    # - prevent external mutation of internal dict
    # - support JSON serialization
    # - support iteration, sorting, filtering
    
    def remove_task(self,task_id):
        #---- Safely remove a task by its ID ----
        if task_id in self.tasks: #checks if task_id exists in the tasks dictionary, this pervents a KeyError if the task_id is not found
            del self.tasks[task_id] #Deletes the task with the given task_id from the tasks dictionary
            return True
        return False #By returning flase, we can easily loop and have a user try again
    
    def create_task_manual(self):

        #---- Get valid task name ----

        while True:
            task_name = input("Enter a task name: ").strip()
            if task_name:
                break
            print("Task name cannot be empty.")

        # ---- Get Valid Task Date ----

        while True: #loops until the user can type in a proper date
            task_date = input("Enter task date (YYYY-MM-DD): ").strip()
            try:
        # Only valid date format should pass this block
                dt_check = datetime.strptime(task_date, "%Y-%m-%d")
                if dt_check.date() < datetime.today().date():
                    print("Task date cannot be in the past.")
                    continue
                break
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
        
        # ---- Validate Start Time ----

        while True: #loop until user gives proper time; loop minimizes repitition of data entry which is my biggest annoyance with schedulers
            start_time = input("Enter start time (HH:MM): ")
            try:
                datetime.strptime(f"{task_date} {start_time}", "%Y-%m-%d %H:%M")
                break
            except ValueError:
                print("Invalid time format. Use HH:MM.")
        
        # ---- Validate End Time ----
    
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
                
                # Valid end time that's after start time
                break  # Exit loop
            except ValueError:
                print("Invalid time format. Please use HH:MM.")
        
        # ---- Get Description ----
        while True: # Loop until we get a non-empty description
            description = input("Enter a description: ").strip()
            if description:
                break
            print("Description cannot be empty.")

        
        # Generate a unique ID for this task
        task_id = DailyTasks.generate_id()  # Calls the static method
        
        # Create the DailyTasks object
        try:
            task = DailyTasks(
                task_name=task_name,
                task_id=task_id,
                task_date=task_date,
                start_time=start_time,
                end_time=end_time,
                description=description
            )
        except ValueError as ve:
            print(f"Unexpected error creating task: {ve}, back to coding")
        # Add the task to this manager's collection
        self.add_task(task)  # Calls the add_task method above
        
        # Confirmation message
        print(f"✓ Task created: {task_name} on {task_date} from {start_time} to {end_time}")
        
        # Return the created task in case caller needs it
        return task

tc=TaskControler()
tc.create_task_manual()
