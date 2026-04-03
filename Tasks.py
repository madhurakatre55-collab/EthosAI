import os
from crewai import Task
from agents import Bias_lens,Explainer, Fix_advisor ,Updater ,Log_generator ,Log_insights


 #Agent1 (Bias_lens) tasks defined 
Bias_detection = Task(
  description = """
  
  
  
  
  
  
  
  
  
  """,
  expected_output="""   
  
  
  
  
  
  """,
  agent=Bias_lens ,
  output_file="task_output/log_analysis.md",
)

#Agent2 (Explainer)tasks defined 
Explains_issues = Task (
  description ="""
  
  
  
  
  
  
  
  
  """,
  expected_output ="""
  
  
  
  
  
  """,
  agent = Explainer, 
  context = [ Bias_detection ] ,
  output_file ="task_output/Explnation_issue.md",
)

#Agent3 (Fix advisor)tasks defined 
Correction_advise = Task (
  description ="""
  
  
  
  
  
  
  
  
  """,
  expected_output ="""
  
  
  
  
  
  """,
  agent = Fix_advisor, 
  context = [ Bias_detection,Explains_issues] ,
  output_file ="task_output/correction_advise.md",
)

#Agent4 (Updater) tasks defined 
Updates_data = Task (
  description ="""
  
  
  
  
  
  
  
  
  """,
  expected_output ="""
  
  
  
  
  
  """,
  agent = Updater, 
  context = [ Bias_detection,Explains_issues,Correction_advise] ,
  output_file ="task_output/updates_made.md",
)

#Agent5 (Log_generator) tasks defined 
Log_generation = Task (
  description ="""
  
  
  
  
  
  
  
  
  """,
  expected_output ="""
  
  
  
  
  
  """,
  agent = Log_generator, 
  context = [ Bias_detection,Explains_issues,Correction_advise, Updates_data] ,
  output_file ="task_output/generates_logs.md",
)

#Agent6 (Log_Insights) tasks defined 
Insights_data = Task (
  description ="""
  
  
  
  
  
  
  
  
  """,
  expected_output ="""
  
  
  
  
  
  """,
  agent = Log_Insights, 
  context = [ Bias_detection,Explains_issues,Correction_advise, Updates_data,Insights_data] ,
  output_file =" task_output/generates_logs.md",
)



