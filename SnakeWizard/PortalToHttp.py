from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from TheWarders import DebugMessages
from HandsOfFate import ObjectManipulation, ObjectOrganization
from JSONdsOfTime import JSONHandler
from TomorrowsLegendaryTales import TaskData


#StartUp Sequence

# Create FastAPI instance and establish middleware
app = FastAPI() #web server instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #API can be called from any origing
    allow_methods=["*"], #Any HTTP method is valid ex: GET, POST, DELETE, etc
    allow_headers=["*"], #Any headers are valid
)
#Intialize Instances of Logger, Object Organization, JSON Storage Handler, and Object Manipulation
# These instances will be used throughout the API to manage tasks and log actions
logger = DebugMessages(debug=True) #Debug just means everything gets logged to the console
org = ObjectOrganization(logger)
storage = JSONHandler(logger)
manip = ObjectManipulation(logger, storage)


#Load Saved Tasks from JSON Storage into current scope, prints confirmation in console
loaded_tasks = storage.load_all_tasks()

org.sync_tasks(loaded_tasks) #sync loaded tasks into organization module
manip.tasks = org.tasks  # sync shared state across modules

#manip.create_task_manual()  # Example of creating a task manually
#org.sync_tasks(manip.tasks.values()) #After every add, edit, or remove Tasks MUST BE INGESTED to keep every module in sync. Kind of annoying but currently it makes bug fixing very easy.

@app.get("/tasks")
def get_all_tasks():
    tasks = org.get_tasks()
    return [task.to_dictionary() for task in tasks]

@app.post("/tasks")
def create_task(task: dict):
    new_task = TaskData.from_dictionary(task, logger)
    manip.add_task(new_task)
    org.sync_tasks(manip.tasks.values())
    return {"status": "created", "task_id": new_task.task_id}

@app.put("/tasks/{task_id}")
def edit_task(task_id: str, updates: dict):
    for field, value in updates.items():
        manip.edit_task(task_id, field, value)

    org.sync_tasks(manip.tasks.values())
    return {"status": "updated", "task_id": task_id}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    manip.remove_task(task_id)
    org.sync_tasks(manip.tasks.values())
    return {"status": "deleted", "task_id": task_id}

@app.get("/tasks/search")
def search_tasks(q: str, mode: str = "any"):
    matches = org.search_tasks(q, mode)
    tasks = org.get_tasks(matches)
    return [task.to_dictionary() for task in tasks]
