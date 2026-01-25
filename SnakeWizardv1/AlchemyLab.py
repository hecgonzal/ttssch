from HandsOfFate import ObjectManipulation, ObjectOrganization
from JSONdsOfTime import JSONHandler
from TheWarders import DebugMessages

logger = DebugMessages(debug=True) #Need to load on api
Jsonds = JSONHandler(logger)
hands = ObjectManipulation(logger, Jsonds)  # Create an instance of ObjectManipulation
hands.create_task_manual()