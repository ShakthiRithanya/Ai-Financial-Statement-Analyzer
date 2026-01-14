import pdfplumber
import pandas as pd
import io

def extract_tables_from_pdf(pdf_file):
    """
    Extracts all tables from a PDF file and returns a list of Pandas DataFrames.
    """
    all_dataframes = []
    
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table:
                    # Clean the table data
                    df = pd.DataFrame(table[1:], columns=table[0])
                    # Remove empty columns and rows
                    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
                    if not df.empty:
                        all_dataframes.append(df)
    
    return all_dataframes

def simple_pdf_text_extraction(pdf_file):
    """
    Fall-back if tables aren't detected perfectly: extract text and search for keywords.
    """
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text
