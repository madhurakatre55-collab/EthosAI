import os
from crewai import Task
from agents import Senior_Fairness_Auditor, Updater, Technical_Reporter

os.makedirs("task_output", exist_ok=True)

# 1. CONSOLDATED ANALYSIS TASK (Saves multiple API calls)
Unified_Fairness_Analysis = Task(
    description="""
    Perform a complete, in-depth multi-dimensional fairness audit on the provided dataset: {user_data}.
    
    You MUST leverage the provided tools (FileReadTool or CSVSearchTool) if paths are provided to scan for deep patterns.
    
    You MUST complete the following sub-actions in one unified output:
    1. **Statistical Bias Detection**: Quantify bias using parity metrics. Extract sensitive attributes ONLY if present.
    2. **Impact Explanation**: Document technical and socio-economic risks found in this specific data.
    3. **Industrial Mitigation Advisory**: Suggest specific algorithmic adjustments.

    STRICT GROUNDING: ONLY analyze information explicitly present in `{user_data}`. If the data is limited to a single sector or attribute, ONLY report on that. DO NOT use generic examples or hallucinate sectors not found in the input. 

    Your final output for THIS task MUST be a concise technical CSV block containing:
    Sector, Attribute, Biased, Fairness_Score, Precision_Metric, Fix_Recommendation
    """,
    expected_output="""
    A technical CSV block representing the comprehensive audit results for parity tracking.
    """,
    agent=Senior_Fairness_Auditor,
    output_file="task_output/consolidated_analysis.csv"
)

# 2. MODEL UPDATE TASK
Updates_data = Task(
    description="""
    Take the approved mitigation strategies from the Unified Fairness Analysis and apply them.
    Focus on improving fairness thresholds and dataset balancing.
    
    You MUST output a "Resolution Log" in CSV format with the following columns:
    Attribute, Action_Taken, Fairness_Before, Fairness_After, Status
    """,
    expected_output="""
    A structured Technical CSV Resolution Log.
    """,
    agent=Updater, 
    context=[Unified_Fairness_Analysis],
    output_file="task_output/resolution_log.csv",
)

# 3. COMPREHENSIVE 6-PAGE REPORT TASK
Comprehensive_Audit_Report = Task(
    description="""
    Synthesize ALL findings from the Unified Fairness Analysis into a professional, data-driven
    Technical Audit Report.
    
    The report MUST be strictly evidence-based and include the following sections:
    1. **Executive Summary**: A high-level view of fairness metrics found in the data.
    2. **Technical Methodology**: Explain how the audit was performed on this specific dataset.
    3. **Data-Driven Deep Dive**: Exhaustive prose analysis of the EXACT findings in the analyzed sector.
    4. **Critical Risk Indicators**: Detailed text on protected attributes found to be biased.
    5. **Strategic Mitigation Roadmap**: A tailored plan to resolve the specific issues identified.
    6. **Ethical Certification Statement**: A summary of compliance alignment.

    ### GRANULAR CSV BLOCK
    At the very end of your report, separated by a line '--- DOCUMENT END ---', you must include a HIGH-RESOLUTION CSV BLOCK.
    This block MUST include granular metrics compared to the analysis block, specifically including:
    Sector, Attribute, Sample_Size, Mean_Bias_Offset, Confidence_Interval, Fairness_Score, Fix_Recommendation
    """,
    expected_output="""
    A comprehensive, 6-page Markdown document including professional headings, detailed technical prose, 
    and the final CSV data block at the end.
    """,
    agent=Technical_Reporter,
    context=[Unified_Fairness_Analysis],
    output_file="task_output/full_audit_report.md"
)
