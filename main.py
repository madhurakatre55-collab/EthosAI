import os
from crewai import Crew,from crewai import Crew, Process, Agent, Task, TaskOutput, CrewOutput





# Form the crew with a generic process
Ethos_crew = Crew(
  agents=[Bias_lens, Explainer, Fix_advisior, Updater, Log_generator, Log_insights],
  tasks=[Bias_detection,Explains_issue,Fix_advise,Updates_dataset,Log_generation,Log_insights],
  process=Process.sequential,
  respect_context_window=True,
  verbose=True,
  cache=True,
  memory=True,
  max_rpm=70,
  manager_agent=None,
  planning=True
)

# Execute the crew
result = Ethos_crew.kickoff()

# Accessing the type-safe output
task_output: TaskOutput = result.tasks[0].output
crew_output: CrewOutput = result.output