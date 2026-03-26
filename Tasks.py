import os
from crewai import Task
from agents import log_analyzer

os.makedirs("task_outputs",exist_ok=Ture)





 task1 = Task(
  description='Description1',
  agent=agent1,
  expected_output='ExpectedOutput1'
)

# Define your tasks
task1 = Task(
  description='Description1',
  agent=agent1,
  expected_output='ExpectedOutput1'
)
task2 = Task(
  description='Description2',
  agent=agent2,
  expected_output='ExpectedOutput2'
)


# Define your tasks
task1 = Task(
  description='Description1',
  agent=agent1,
  expected_output='ExpectedOutput1'
)
task2 = Task(
  description='Description2',
  agent=agent2,
  expected_output='ExpectedOutput2'
)