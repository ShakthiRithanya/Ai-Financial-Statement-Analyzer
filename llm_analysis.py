import google.generativeai as genai
import os
from prompts import (
    PERFORMANCE_SUMMARY_PROMPT,
    RED_FLAG_DETECTOR_PROMPT,
    STRENGTH_AND_MOAT_PROMPT,
    VERDICT_PROMPT
)

def get_llm_analysis(api_key, financial_data_str, model_name="gemini-1.5-flash"):
    """
    Orchestrates the 3 separate LLM calls plus the final verdict.
    """
    try:
        genai.configure(api_key=api_key)
        
        # Clean the model name - sometimes names come with 'models/' prefix
        clean_name = model_name.split('/')[-1]
        model = genai.GenerativeModel(clean_name)
        
        results = {}
        
        # 1. Performance Summary
        resp1 = model.generate_content(PERFORMANCE_SUMMARY_PROMPT.format(financial_data=financial_data_str))
        results['performance'] = resp1.text

        # 2. Red Flags
        resp2 = model.generate_content(RED_FLAG_DETECTOR_PROMPT.format(financial_data=financial_data_str))
        results['red_flags'] = resp2.text

        # 3. Strengths
        resp3 = model.generate_content(STRENGTH_AND_MOAT_PROMPT.format(financial_data=financial_data_str))
        results['strengths'] = resp3.text
        
        # 4. Final Verdict
        verdict_input = VERDICT_PROMPT.format(
            performance_summary=results['performance'],
            red_flags=results['red_flags'],
            strengths=results['strengths']
        )
        resp4 = model.generate_content(verdict_input)
        results['verdict'] = resp4.text
        
        return results
    except Exception as e:
        return {"error": str(e)}

def list_available_models(api_key):
    """
    Returns a list of model names that support content generation.
    """
    try:
        genai.configure(api_key=api_key)
        models = [m.name.split('/')[-1] for m in genai.list_models() 
                  if 'generateContent' in m.supported_generation_methods]
        return models if models else ["gemini-1.5-flash", "gemini-pro"]
    except:
        return ["gemini-1.5-flash", "gemini-pro"]

def format_data_for_llm(df, ratios_df):
    """
    Converts dataframes to a string summary for the LLM to ingest.
    """
    summary = "FINANCIAL STATEMENT DATA:\n"
    summary += df.to_string()
    summary += "\n\nCALCULATED FINANCIAL RATIOS:\n"
    summary += ratios_df.to_string()
    return summary
