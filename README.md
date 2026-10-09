# FinTech_Fraud-Detection-Risk-Analysis
Send anomalous transaction rows to Gemini to write an Automated Risk Explanation Report detailing why a specific transaction appears fraudulent and recommending whether to freeze or approve the account. 
```markdown
# FinTech Fraud Detection & Risk Analysis Dashboard

An AI-augmented financial transaction surveillance and fraud investigation platform built with **Streamlit**, **Pandas**, and **Google Gemini (`gemini-3.5-flash-lite`)**. 

The system automates the detection of suspicious financial activities using statistical baseline modeling and leverages large language models to generate audit-ready risk explanations and operational triage recommendations (Freeze vs. Approve).

---

## Key Features

- **Automated Behavioral Baselines:** Computes historical spending profiles (`Avg_Spend`) per user and dynamically derives spending spike ratios (`Spike_Ratio = Amount / Avg_Spend`).
- **Dual-Layer Anomaly Filtering:** Instantly isolates high-risk transactions based on known rule flags (`Flagged_Status == 1`) and statistical anomaly thresholds (`Spike_Ratio >= 3.0x`).
- **Interactive Analyst Workbench:** Clean, responsive UI for compliance officers to inspect individual suspicious transactions alongside critical transaction metadata (merchant category, location, account age).
- **AI-Powered Risk Briefs:** Programmatic reasoning via `gemini-3.5-flash-lite` that synthesizes anomaly metrics into an executive root-cause explanation and issues a definitive triage verdict (`FREEZE` vs. `APPROVE`).
- **Security-First Architecture:** Adheres to enterprise secret isolation standards; API keys can be supplied via runtime UI input or loaded securely via an untracked `.env` file.

---

## Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Data Engineering & Analytics:** [Pandas](https://pandas.pydata.org/)
- **Large Language Model API:** [Google Generative AI SDK](https://ai.google.dev/) (`gemini-3.5-flash-lite`)
- **Environment Management:** [python-dotenv](https://github.com/theskumar/python-dotenv)
- **Runtime Environment:** Python 3.14+

---

## Project Structure

```text
├── .gitignore                      # Excludes .env, virtual environments, and cache
├── .env.example                    # Sample environment template (no credentials)
├── app.py                          # Main Streamlit application and AI pipeline
├── fintech_fraud_transactions.csv  # Synthetic financial transaction dataset
├── requirements.txt                # Production Python dependencies
└── README.md                       # Project documentation

```

---

## Getting Started

### 1. Prerequisites

* Python 3.11 or higher (Python 3.14 compatible)
* A Google AI Studio API key (obtainable at [aistudio.google.com](https://aistudio.google.com/))

### 2. Clone the Repository

```bash
git clone [https://github.com/Ambii/FinTech_Fraud-Detection-Risk-Analysis.git](https://github.com/Ambii/FinTech_Fraud-Detection-Risk-Analysis.git)
cd FinTech_Fraud-Detection-Risk-Analysis

```

### 3. Create and Activate a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate

```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate

```

### 4. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## Configuration

You can supply your Google Gemini API key using either of the following methods:

### Option A: Local `.env` File (Recommended for Local Dev)

Create a `.env` file in the project root:

```env
GEMINI_API_KEY="your_actual_api_key_here"

```

*(The `.env` file is excluded from Git via `.gitignore` to prevent secret leaks.)*

### Option B: In-App UI Configuration

Run the dashboard and paste your API key directly into the secure password field located in the sidebar.

---

## Running the Application

Launch the Streamlit web server:

```bash
streamlit run app.py

```

The application will launch in your default web browser at `http://localhost:8501`.

---

## How It Works

1. **Ingestion & Baseline Modeling:**
The dataset is loaded into Pandas. Transactions are grouped by `User_ID` to calculate per-user baseline averages, computing each transaction's deviation multiple (`Spike_Ratio`).
2. **Surveillance Queue:**
Transactions breaching compliance criteria are surfaced in the suspicious ledger.
3. **Analyst Selection:**
The investigator selects a flagged record from the interactive selector to inspect the user's spending context.
4. **LLM Executive Brief:**
Clicking **Generate Risk Report** passes structured transaction metrics to `gemini-3.5-flash-lite`. The model generates an analysis detailing the potential fraud typology (e.g., account takeover, structuring, card-not-present fraud) and issues a freeze/approve recommendation.

---

## Model Whitelist & Hackathon Compliance

This application adheres to hackathon submission requirements:

* **Approved Model:** Google Gemini `gemini-3.5-flash-lite`
* **Secret Isolation:** API keys are excluded from source control.
* **In-App LLM Integration:** Programmatic API execution directly tied to data pipeline operations.

---

## License

This project is licensed under the MIT License — see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

```

```
