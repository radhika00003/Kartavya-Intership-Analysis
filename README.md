# Kartavya.ai Internship Intelligence System

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
