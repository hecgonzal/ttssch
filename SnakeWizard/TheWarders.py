from datetime import datetime

class DebugMessages:
    def __init__(self, debug: bool = True):
        self.debug = debug
        self.error_log: list[str] = []
        self.process_log: list[str] = []
        self.error_code: int = 0
        self.process_code: int = 0
        self.TaskData_errors_outstring = {
            1: "[{timestamp}][Task Data Error] Invalid Task ID ({}): must be a valid UUID string.",
            2: "[{timestamp}][Task Data Error] Invalid Task Name: cannot be empty.",
            3: "[{timestamp}][Task Data Error] Invalid Task Date ({}): must be in YYYY-MM-DD format.",
            4: "[{timestamp}][Task Data Error] Task Start Time format invalid ({}): must be HH:MM.",
            5: "[{timestamp}][Task Data Error] Task End Time format invalid ({}): must be HH:MM.",
            6: "[{timestamp}][Task Data Error] End time must be after start time. Start: {}, End: {}.",
            7: "[{timestamp}][Task Data Error] Task Description is not a string or empty string. Task Description: {}",
            8: "[{timestamp}][Task Data Error] Duplicate Task ID detected: {}",
            9: "[{timestamp}][Task Data Error] Task date cannot be in the past: {}",
            10: "[{timestamp}][Task Data Error] Unknown validation error: {}",
            11: "[{timestamp}][Task Data Error] Task creation failed due to multiple invalid fields."
        }

        self.JSONHandler_errors_outstring = {
            1: "[{timestamp}][JSON Handler Error] Failed to save tasks to file: {}",
            2: "[{timestamp}][JSON Handler Error] Failed to load tasks from file: {}",
            3: "[{timestamp}][JSON Handler Error] JSON decode error: {}",
            4: "[{timestamp}][JSON Handler Error] IOError during file operation: {}",
            5: "[{timestamp}][JSON Handler Error] Unexpected error: {}"
        }

        self.JSONHandler_process_outstring = {
            1: "[{timestamp}][JSON Handler Process] Task successfully loaded from JSON file: {}",
            2: "[{timestamp}][JSON Handler Process] Task successfully saved to JSON file: {}",
            3: "[{timestamp}][JSON Handler Process] attempting to load JSON file: {}",
            4: "[{timestamp}][JSON Handler Process] attempting to save JSON file: {}",
            5: "[{timestamp}][JSON Handler Process] No storage file found at {}, creating new JSON file.",
            6: "[{timestamp}][JSON Handler Process] Loaded {} tasks from {} (size: {} bytes)",
            7: "[{timestamp}][JSON Handler Process] Saved {} tasks to {} (size: {} bytes)"
        }
        self.Object_error = {
            1: "[{timestamp}][Object Error] Task ID not found in tasks dictionary.",
            2: "[{timestamp}][Object Error] Task not found in tasks dictionary.",
            3: "[{timestamp}][Object Error] Failed to add task Object to JSON storage: {}",
            4: "[{timestamp}][Object Error] Failed to remove task from instance storage: {}",
            5: "[{timestamp}][Object Error] Invalid sort key provided: {}",
            6: "[{timestamp}][Object Error] Invalid Field Edit Attempted: {}"
        }
        self.Object_log = {
            1: "[{timestamp}][Object Log] Task added with ID: {}",
            2: "[{timestamp}][Object Log] Tasks Loaded Successfully from Storage: {}",
            3: "[{timestamp}][Object Log] {} tasks saved to storage successfully.",
            4: "[{timestamp}][Object Log] Task removed with ID: {}",
            5: "[{timestamp}][Object Log] Task created: {}"
        }
    
    def log_error(self, error_code: int,error_type: str = "", *args ):
        if error_type == "TaskData":
            error_msg_shell = self.TaskData_errors_outstring[error_code]
        elif error_type == "JSONHandler":
            error_msg_shell = self.JSONHandler_errors_outstring[error_code]
        elif error_type == "Object":
            error_msg_shell = self.Object_error[error_code]
        else:
            raise ValueError(f"Invalid error_type: {error_type}")
        message = error_msg_shell.format(timestamp=datetime.now(),*args)
        self.error_log.append(message)
        if self.debug:
            self.error_log.append(message)
    
    def log_process(self, process_code: int,process_type: str = "", *args ):
        if process_type == "JSONHandler": process_msg_shell = self.JSONHandler_process_outstring[process_code]
        elif process_type == "Object": process_msg_shell = self.Object_log[process_code]
        else: raise ValueError(f"Invalid process_type: {process_type}")
        message = process_msg_shell.format(timestamp=datetime.now(),*args)
        self.process_log.append(message)
        if self.debug:
            self.error_log.append(message)

    def clear_log(self):
        self.error_log.clear()

    #--------- Print Logs ---------#
    def print_error_logs(self):
        for log in self.error_log:
            print(log)
    def print_process_logs(self):
        for log in self.process_log:
            print(log)
    def full_logs_print(self):
        master_log=self.error_log + self.process_log
        master_log.sort(key=lambda msg: msg.split(']')[0].strip('[')) #Sorts by timestamp
        for log in master_log:
            print(log)