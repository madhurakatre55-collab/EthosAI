import os
from crewai import Task
from agents import Senior_Fairness_Auditor, Updater, Technical_Reporter

os.makedirs("task_output", exist_ok=True)

# 1. CONSOLDATED ANALYSIS TASK (Saves multiple API calls)
Unified_Fairness_Analysis = Task(
    description="""
    Perform a complete, in-depth multi-dimensional fairness audit on the provided dataset: {user_data}.
    
    You MUST complete the following sub-actions in one unified output:
    1. **Statistical Bias Detection**: Quantify bias using parity metrics. Extract sensitive attributes ONLY if present.
    2. **Impact Explanation**: Document technical and socio-economic risks found in this specific data.
    3. **Industrial Mitigation Advisory**: Suggest specific algorithmic adjustments.

    STRICT GROUNDING: ONLY analyze information explicitly present in `{user_data}`. DO NOT hallucinate sectors not found in the input.

    Your final output for THIS task MUST end with a CSV block in this EXACT format (include real data from the input):
    Sector,Attribute,Biased,Fairness_Score,Precision_Metric,Fix_Recommendation
    """,
    expected_output="""
    A technical CSV block representing the comprehensive audit results.
    The LAST lines of your response must be the raw CSV data starting with the header:
    Sector,Attribute,Biased,Fairness_Score,Precision_Metric,Fix_Recommendation
    Followed by data rows. Do NOT use file links. Embed the CSV directly.""",
    agent=Senior_Fairness_Auditor,
    output_file="task_output/consolidated_analysis.csv"
)

# 2. MODEL UPDATE TASK
Updates_data = Task(
    description="""
    Take the approved mitigation strategies from the Unified Fairness Analysis and apply them.
    Focus on improving fairness thresholds and dataset balancing.
    
    Your output MUST follow this EXACT structure:
    1. A short 2-3 sentence summary of changes made.
    2. The separator line: --- DOCUMENT END ---
    3. A Resolution Log CSV with EXACTLY these columns:
    Sector,Attribute,Bias_Detected,Action_Taken,Fairness_After,Status
    """,
    expected_output="""
    A short summary paragraph, then the line '--- DOCUMENT END ---', then a structured CSV Resolution Log.
    The CSV must have real data from the analysis. Do NOT use file links. Embed the CSV directly after the separator.
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

    CRITICAL: After all prose sections, output the EXACT separator line:
    --- DOCUMENT END ---
    Then immediately output the CSV block with these EXACT headers (real data only, no placeholders):
    Sector,Attribute,Sample_Size,Mean_Bias_Offset,Confidence_Interval,Fairness_Score,Fix_Recommendation
    """,
    expected_output="""
    A comprehensive Markdown report with all 6 sections, then the line '--- DOCUMENT END ---',
    then the raw CSV data embedded directly (NOT as a file link). The CSV must contain real metrics from the analysis.
    """,
    agent=Technical_Reporter,
    context=[Unified_Fairness_Analysis],
    output_file="task_output/full_audit_report.md"
)
