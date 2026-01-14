# AI Financial Statement Analyzer

An AI-powered junior financial analyst that extracts data from PDF/Excel/CSV reports and provides deep financial insights using Google Gemini.

## 🚀 Features
- **File Parsing**: Auto-extracts tables from PDFs and structured Excel/CSV files.
- **Financial Normalization**: Automatically identifies key line items (Revenue, Net Income, FCF, etc.).
- **Ratio Analysis**: Computes Profitability, Liquidity, Solvency, and Efficiency ratios.
- **AI Intelligence**: 3-stage LLM analysis (Performance, Risks, Strengths) + Final Verdict.
- **Interactive Dashboard**: Visualizes trends with Plotly and Streamlit.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Data**: Pandas, NumPy
- **Extraction**: PDFPlumber
- **AI**: Google Gemini (generativeai)

## 📦 Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🔑 Configuration
- You will need a **Google Gemini API Key**.
- Obtain one from [Google AI Studio](https://aistudio.google.com/).
- Enter it in the sidebar of the application.

## 📂 Project Structure
- `app.py`: Main UI and dashboard.
- `data_processing.py`: Normalization and cleaning logic.
- `ratio_analysis.py`: Calculation of financial ratios.
- `llm_analysis.py`: Orchestrates AI calls.
- `pdf_extractor.py`: Table extraction from PDFs.
- `prompts.py`: Professional financial analysis prompts.
- `utils.py`: Helpers and demo data.
