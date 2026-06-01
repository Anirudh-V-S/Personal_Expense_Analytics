# Personal Expense Analytics Dashboard 📊

**Intern ID:** `CITS2983`  
**Host Organization:** CodTech IT Solutions  
**Internship Domain:** Data Analytics  
**Author:** Anirudh V S

An advanced, submission-ready **Personal Expense Analytics Dashboard** developed for a Data Analytics Internship. Built with Python and Streamlit, this application converts raw financial transaction logs into rich visual intelligence.

---

## 🌟 Key Features

1. **Executive Overview Dashboard**:
   * Frosted-glass KPI cards tracking Total Spent, Average Transaction, Largest Expense, and Transaction Count.
   * Rolling 7-day average spending curves to isolate trend patterns.
   * Interactive payment method donut charts.
   * High-resolution hierarchical category & merchant share treemaps.

2. **Categorical Expenditures & Activity Analysis**:
   * Interactive horizontal bar chart highlighting category limits.
   * Weekly Activity Heatmap demonstrating what categories are spent on which weekdays.
   * Categorical details variance tables with count, average, and percent shares.

3. **Temporal Habit Mapping**:
   * Month-on-Month spend changes (Bar & Line overlays).
   * Day of Week breakdowns (Monday - Sunday) detailing transaction counts and averages.
   * Weekend vs. Weekday behavioral analysis cards.

4. **Budget & Savings Estimator**:
   * Dynamic budget configurations for each unique category.
   * Savings Rate and net-savings calculator based on estimated monthly income.
   * Dual horizontal budget variance charts (green = on track, orange = critical, red = over budget).

5. **Advanced Predictive Analytics (Weekly Forecasting)**:
   * **Ordinary Least Squares (OLS) Linear Regression model** fitted to weekly aggregations.
   * Forecasts upcoming 4-week expense rates with an accuracy check (R² score) and rate interpretation.

6. **Ledger Logs & Export Systems**:
   * Searchable and filterable data tables.
   * Cleaned ledger downloader in CSV format.
   * Comprehensive analytical summary report exporter (.txt).

---

## 📂 Project Structure

```text
Personal_Expense_Analytics/
│
├── app.py                      # Dashboard application entry point
├── requirements.txt            # Python environment dependencies
├── README.md                   # Project documentation
│
├── data/
│   └── sample_expenses.csv     # 6-month synthetic ledger containing 285 transactions
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Fuzzy schema matching & validation module
│   ├── preprocessing.py        # Cleans types, filters anomalies, extracts time features
│   ├── analytics.py            # Aggregations, budget analytics, and OLS regression model
│   ├── visualizations.py       # Custom premium-themed Plotly charts
│   ├── helpers.py              # CSS injectors, KPI card builders, text report generators
│   └── generate_data.py        # Script used to generate the realistic sample data
│
└── report/
    └── project_report.md       # Comprehensive internship project report
```

---

## 📋 Schema & Dataset Format

The data mapping engine handles structural differences in columns automatically (case-insensitive, ignores spacing, spaces, and underscores). The required columns are:

| Standard Name | Sample Mapped Variations | Description |
| :--- | :--- | :--- |
| **Date** | `date`, `transaction_date`, `dt`, `timestamp` | YYYY-MM-DD date format |
| **Category** | `category`, `type`, `class`, `expense category` | Grocery, Rent, Utilities, etc. |
| **Amount** | `amount`, `cost`, `spent`, `price` | Non-negative numeric cost |
| **Payment_Method** | `payment_method`, `mode`, `method` | Credit Card, UPI, Debit Card, Cash |
| **Merchant** | `merchant`, `description`, `vendor`, `payee` | Place/Store of transaction |
| **Account** (Optional) | `account`, `wallet`, `bank` | Source (e.g., Primary checking) |

---

## ⚙️ Installation & Usage Guide

### Prerequisites
* Python 3.8 or higher installed on your system.

### Step 1: Clone or Extract the Workspace
Navigate to the directory containing the code files:
```bash
cd d:/CodTEchIT_INTERN/Personal_Expense_Analytics
```

### Step 2: Establish a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit Application
```bash
streamlit run app.py
```

The application will launch automatically in your default web browser (usually at `http://localhost:8501`).

---

## 🔮 Future Improvements

1. **OCR Expense Ingestion**: Add optical character recognition to extract expense records directly from uploaded receipt images.
2. **Database Integration**: Store transaction logs in an SQLite or PostgreSQL database for persistence rather than memory-only state.
3. **Multi-User Portals**: Support multiple user profiles with private login systems and encrypted data.
4. **Machine Learning Classifiers**: Train a Random Forest or BERT-based NLP model to automatically classify merchant strings into categories (e.g. mapping "Starbucks" to "Dining Out").

---

## 👤 Author Information

* **Name**: Anirudh V S
* **Intern ID**: `CITS2983`
* **GitHub Profile**: [Anirudh-V-S](https://github.com/Anirudh-V-S)
* **Internship Provider**: CodTech IT Solutions
