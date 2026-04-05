import os
from crewai import Task
from agents import Bias_lens,Explainer, Fix_advisor ,Updater ,Log_generator ,Log_insights

os.makedirs("task_output", exist_ok=True)
                                   #BIAS LENS (AGENT 1)

Bias_detection = Task(

       # DESCRIPTION OF FOR BIASLENS AGENT 
 
  description = """
  Your analysis should:
    1. Identify the sector of the provided dataset and model:
      - Medical (diagnosis/treatment prediction)
      - Bank Loan (loan approval/risk scoring)
      - Job Hiring (candidate screening/selection)

    2. Extract and validate sensitive attributes based on sector:

      *Medical:
        - Gender, Age group, Ethnicity, Socio-economic status, Pre-existing conditions, Location
      *Bank Loan:
        - Gender, Age, Income level, Occupation, Location, Credit score, Education
      *Hiring:
        - Gender, Age, Education (college tier), Experience, Career gaps, Location, Name indicators

    3. Perform data distribution analysis:
      - Compute counts and percentages for each sensitive group
      - Identify underrepresented and overrepresented groups
      - Detect missing or skewed data distributions and the null values and the values that are not in the range of the data.

    4. Perform outcome-based analysis:

      *Medical:
        - Compare diagnosis accuracy across groups
        - Compare treatment allocation rates
        - Analyze false positives/false negatives per group

      *Bank Loan:
        - Compare approval vs rejection rates across groups
        - Analyze risk score distribution per group
        - Identify threshold-based disparities

      *Hiring:
        - Compare selection vs rejection rates
        - Analyze shortlisting patterns
        - Evaluate filtering criteria impact

    5. Detect bias patterns:
      - Statistical disparity between groups
      - Unequal error rates
      - Favoritism or discrimination trends

    6. Identify root causes of bias:
      - Historical imbalance in training data
      - Presence of proxy variables (e.g., location, college)
      - Label bias from human decisions
      - Data quality issues or missing values

    7. Flag each sensitive attribute with bias status (YES/NO)

    Focus on identifying statistically significant and sector-specific unfair patterns.""",
     
 # EXPECTED OUTPUT FOR BIASLENS
 
  expected_output="""   
   A comprehensive bias detection report containing:

    - Identified sector (Medical / Bank Loan / Hiring)

    - Sensitive attributes analyzed:
      - List with descriptions

    - Data distribution summary:
      - Group-wise counts and percentages
      - Underrepresented groups clearly highlighted

    - Outcome analysis:

     1. Medical:
        - Diagnosis accuracy per group
        - Treatment allocation rates
        - Error rate comparison (FPR, FNR)

      2.Bank Loan:
        - Approval/rejection rates per group
        - Risk score distribution
        - Threshold disparities

      3.Hiring:
        - Selection/rejection rates
        - Shortlisting trends
        - Filtering bias patterns

    - Detected bias patterns:
    - Clear statements of unfair differences

    - Root cause analysis:
      - Data imbalance
      - Proxy feature influence
      - Historical or labeling bias

    - Bias flags:
      - Attribute-wise YES/NO bias indicator

    - Supporting statistical evidence and comparisons. """,
  agent=Bias_lens ,
  output_file="task_output/log_analysis.md",
)

                               # EXPLAINER (AGENT 2)

Explains_issues = Task (
 
 # DESCRIPTION FOR EXPLAINER

  description ="""
  Your analysis should:
      1. Take bias detection results as input

      2. Identify the sector:
         - Medical / Bank Loan / Hiring

      3. Compute fairness metrics:

       *Medical:
         - Error rate difference (FPR, FNR)
         - Equal opportunity difference
         - Treatment allocation fairness

       *Bank Loan:
         - Approval rate difference
         - Disparate impact ratio
         - Statistical parity difference

       *Hiring:
         - Selection rate difference
         - Representation ratio
         - Disparate impact ratio

      4. Normalize metrics into an overall fairness score (0 to 100)

      5. Compare metrics with fairness thresholds:
         - Identify acceptable vs unacceptable disparities 
         - And consequences of it 

      6. Classify severity:
         - Low / Medium / High bias

      7. Interpret results in very  simple language such that consider the user is 10 years old kid and dont have any knowledge of AI,ml,models and data science :
         - Explain why bias exists and how it is affecting the model and the data and the people 
         - Identify affected groups and the reason for it 

      8. Explain real-world impact:

        *Medical:
         - Misdiagnosis, unequal treatment

        *Bank Loan:
         - Financial exclusion

        *Hiring:
         - Unfair hiring decisions

      Focus on combining technical fairness evaluation with human-readable explanation.""",
 
    # EXPECTED OUTPUT FOR EXPLAINER

    expected_output ="""
  A detailed fairness and explanation report containing:

      1. Sector identified

      2. Fairness score (0 to 100)

      3. Metric breakdown:

        *Medical:
          - Error rate differences
          - Opportunity gaps

        *Bank Loan:
          - Approval disparities
          - Impact ratios

        *Hiring:
          - Selection disparities
          - Representation imbalance

      4. Group-wise comparisons

      5. Bias severity:
         - Low / Medium / High

      6. Explanation of why bias is occurring

      7. Affected groups clearly identified

      8. Real-world impact:

        *Medical:
          - Health risks

        *Bank Loan:
          - Financial inequality

        *Hiring:
          - Opportunity loss

      9. Simple summary of the issue

      
      
      10. Identify acceptable vs unacceptable disparities 
         - And consequences of it and explain it  
      
      
      11. Explain why bias exists and how it is affecting the model and the data and the people 
         - Identify affected groups and the reason for it

      12. Clear conclusion . """,
  agent = Explainer, 
  context = [ Bias_detection ] ,
  output_file ="task_output/Explnation_issue.md",
)

                            # FIXADVISIOR (AGENT 3)

Correction_advise = Task (

  # DESCRIPTION OF TASKS  FOR FIXADVISIOR AGENT 

  description ="""
  Your analysis should:
      1. Review bias detection and fairness reports

      2. Identify root causes of bias for the sector

      3. Fixing the data sets 
         - Fix the given data by adding the missing facts or add the facts that are not present in the data 
         - Rectifing the bias causing facts and te facts that are missing in the data
         - Update model parameters

      4. Generate mitigation strategies:

        *Medical:
          - Balance dataset across patient groups
          - For all bias causing parameters
          - Improve representation
          - Adjust diagnostic thresholds

        *Bank Loan:
          - Remove proxy variables (location, education)
          - For all bias causing parameters
          - Balance approval data
          - Apply fairness constraints

        *Hiring:
          - Remove sensitive attributes (gender, name)
          - For all bias causing parameters
          - Focus on skill-based filtering
          - Reduce keyword bias

      4. Evaluate each solution:
          - Effectiveness
          - Risk to performance
          - Implementation complexity

      5. Rank solutions
          - That can be efficetively impoeve the unbiasness in the model 
          - Try to rank them according to the effectiveness and risk to performance and implementation complexity

      6. Recommend best solution
          -That can considered for everyone and  can be implemented easily and  should not have any side effects     

      7. Ask for human approval:
          - Approve / Modify / Reject

      8. Prepare final action plan

  
      Focus on safe, practical, and explainable bias mitigation. """,

  # EXPECTED OUTPUT FOR FIXADVISIOR
 
  expected_output ="""
 A detailed bias mitigation report containing:

      1. Sector identified

      2. Root cause of bias

      3. List of suggested fixes:
         - Explanation for each

      4. Evaluation:
         - Effectiveness
         - Risk level
         - Complexity

      5. Ranked solutions

      6. Recommended fixs and also in detailed formate such that user is a beginner

      7. Expected improvement

      8. Human approval request:
         - Approve / Modify / Reject

      9. Final action plan.  """,
  agent = Fix_advisor, 
  context = [ Bias_detection,Explains_issues] ,
  output_file ="task_output/correction_advise.md",
)

                              # UPDATER (AGENT 4)

Updates_data = Task (

  # DESCRIPTION OF TASKS FOR UPDATE AGENTS

  description ="""
  Your execution should:
      1. Receive approved fix from FixAdvisor

      2. Apply changes:
         - Modify dataset by rebalancing, cleaning, processing, pre_processing 
         - Remove or adjust features and feature engineering
         - Update model parameters

      3. Retrain or update the model
         - Update model parameters and retrain the model 
         - Till the model is updated and bias is reduced 
         - Till the model reaches compatable efficiency   

      4. only tell the difference between before vs after results

      Focus on improving fairness while maintaining performance.  """,

 # EXPECTED OUTPUT FOR UPDATER

  expected_output ="""
 A model update report containing:

     1. Description of applied changes

     2. Updated dataset/model details

     3. Fairness improvement comparison:
        - Before vs After

     4. Bias reduction summary

     5. Any trade-offs observed

     6. Final conclusion on model improvement .  """,
 
  agent = Updater, 
  context = [ Bias_detection,Explains_issues,Correction_advise] ,
  output_file ="task_output/updates_made.md",
)

                    # LOG GENERATOR (AGENT 5)

Log_generation = Task (
  description ="""
  
  Your task should:
      1. Capture every model interaction in real-world usage

      2. Record:
         - Input features
         - Sensitive attributes (if available)
         - Model prediction/output
         - Confidence score (if applicable)

      3. Attach timestamps to each record

      4. Maintain sector identification

      5. Store logs in structured format (JSON/CSV)

      6. Ensure:
         - Data consistency
         - No missing critical fields

      Focus on creating a complete and reliable log history .""",

 # EXPECTED OUTPUT FOR LOG GENERATOR

  expected_output ="""
  
  A structured log dataset containing:

        1.Unique record ID

        2.Sector identifier

        3.Input features

        4.Sensitive attributes

         5.Model output/prediction

        6.Confidence score (if available)

        7.Timestamp

        8.Properly formatted log file

        9.Continuous and consistent entries.  """,
  agent = Log_generator, 
  context = [ Bias_detection,Explains_issues,Correction_advise, Updates_data] ,
  output_file ="task_output/generates_logs.md",
)

             # LOG INSIGHTS (AGENT 6) 

 
Insights_data = Task (

 # DESCRIPTION FOR LOG INSIGHTS
 
  description ="""
 Your analysis should:
      1. Load and process log data

      2. Identify sector

      3. Perform time-based analysis:
         - Track behavior changes over time

      4. Perform group-wise analysis:

         *Medical:
         - Diagnosis/treatment trends

         *Bank Loan:
         - Approval trends

         *Hiring:
         - Selection trends

      5. Detect emerging bias:
         - Increasing disparities
         - Drift in fairness

      6. Identify anomalies:
         - Sudden spikes/drops
         - Inconsistent behavior

      7. Compare real-world results with expected fairness

      Focus on continuous monitoring and early detection of bias.  """,

 # EXPECTED OUTPUT FOR LOG INSIGHTS
 
  expected_output ="""
  A log analysis report containing:

  1. Sector identified

  2. Log summary:
      - Total records
      - Time duration

  3. Time-based trends

  4. Group-wise statistics:

        *Medical:
          - Diagnosis distribution

        *Bank Loan:
          - Approval trends
  
        *Hiring:
          - Selection trends

  5. Emerging bias patterns

  6. Detected anomalies

  7. Bias drift alerts

  8. Final summary of system behavior. """,
  agent = Log_insights, 
  context = [ Bias_detection,Explains_issues,Correction_advise, Updates_data,Log_generation ] ,
  output_file =" task_output/generates_logs.md",
)



