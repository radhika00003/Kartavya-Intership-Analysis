# Kartavya.ai Internship Analysis

## 📋 Overview
The **Kartavya.ai Internship Intelligence System** is a specialized market analysis tool built to automate the collection of internship data across India. It aggregates real-time listings from **LinkedIn**, **Internshala**, and **Unstop** to provide actionable hiring insights.

This system uses a **"Hybrid Scraping Engine"** to bypass modern anti-bot protections and features a **Zero-Dependency Architecture** to run flawlessly on any machine (including macOS with Python 3.13) without crashing.

## 🚀 Key Features
* **Hybrid Scraping:**
    * **LinkedIn:** Uses the hidden Guest API to fetch data directly (bypassing login/auth-walls).
    * **Internshala:** Uses a Selenium "Text Search" strategy to extract stipend/duration even if the UI changes.
    * **Unstop:** Uses a "Link Hunter" algorithm to identify opportunities amidst dynamic content.
* **Crash-Proof Analysis:** Calculates Average Stipend, Top Domains, and Trends using pure Python logic (removing the need for heavy libraries like `pandas` or `numpy` that cause installation conflicts).
* **Auto-Reporting:**
    * **CSV Export:** Saves a clean dataset for Excel/Google Sheets.
    * **PDF Insights:** Generates a strategic summary report with recommendations.
* **Cloud Sync:** Includes an automated script to create a GitHub repository and upload your reports/code instantly.

## 🛠️ Prerequisites
* **Python 3.8+** installed.
* **Google Chrome** browser installed.
* **GitHub Account** (optional, for the upload feature).

## 📦 Installation

1.  **Clone or Download** this repository.
2.  Open your terminal or command prompt in the project folder.
3.  **Install the required lightweight libraries:**

```bash
pip install selenium requests beautifulsoup4 fpdf webdriver-manager
````

## ▶️ Usage Instructions

### Step 1: Run the Intelligence System

This script collects data, analyzes it, and generates the reports.

```bash
python main.py
```

  * **What to expect:**
      * You will see logs in the terminal as it fetches data from LinkedIn.
      * A **Chrome window** will open for Internshala/Unstop. **DO NOT CLOSE IT.** Let it scroll and collect data automatically.
      * Once finished, two files will be generated: `Kartavya_Final_Data_[Date].csv` and `Kartavya_Insights_Report.pdf`.


## 📂 Output Files

| File Name | Description |
| :--- | :--- |
| `Kartavya_Final_Data_[DATE].csv` | Master dataset containing Title, Company, Platform, Stipend, and Apply Links. |
| `Kartavya_Insights_Report.pdf` | Executive summary with market statistics, average stipend calculations, and hiring advice. |

## 🔧 Troubleshooting

**Q: LinkedIn shows "0 Listings"?**

  * A: LinkedIn limits Guest API calls per IP address. If this happens, wait 10 minutes or switch to a different network (e.g., mobile hotspot).

**Q: GitHub Upload says "Not Found"?**

  * A: This means your Token is invalid or lacks permissions. Generate a **Classic Token** (not Fine-grained) and ensure the **`repo`** checkbox is ticked in GitHub Developer Settings.

**Q: The Browser closes immediately?**

  * A: This is normal if the scraping finishes quickly. If no data is saved, check your internet connection.

## ⚖️ Disclaimer

This tool is intended for **internal market research purposes only**.

  * **Compliance:** The tool respects `robots.txt` policies and includes rate-limiting to be polite to host servers.
  * **Data Usage:** Do not use scraped data for commercial resale or spamming.

-----

*Generated for Kartavya.ai Intern Acquisition Strategy*
