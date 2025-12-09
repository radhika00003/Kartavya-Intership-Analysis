import csv
import time
import requests
import re
import math
from datetime import date
from collections import Counter
from bs4 import BeautifulSoup
from fpdf import FPDF

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
OUTPUT_CSV = f"Kartavya_Final_Data_{date.today()}.csv"
OUTPUT_PDF = "Kartavya_Insights_Report.pdf"

class KartavyaSystem:
    def __init__(self):
        print("--- SYSTEM STARTING (DEEP SCAN MODE) ---")
        self.dataset = []
        
        # Setup Chrome
        self.options = Options()
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        
        try:
            self.service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=self.service, options=self.options)
        except Exception as e:
            print(f"   > Driver Error: {e}")

    # ---------------------------------------------------
    # 1. LINKEDIN (API METHOD - PROVEN TO WORK)
    # ---------------------------------------------------
    def scrape_linkedin(self):
        print("\n[1/3] Scraping LinkedIn (Via API)...")
        base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=intern&location=India&start={}"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}

        for position in [0, 25, 50, 75]:
            try:
                response = requests.get(base_url.format(position), headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                jobs = soup.find_all('li')
                
                for job in jobs:
                    try:
                        title = job.find('h3', class_='base-search-card__title').text.strip()
                        company = job.find('h4', class_='base-search-card__subtitle').text.strip()
                        link = job.find('a', class_='base-card__full-link')['href']
                        
                        self.dataset.append({
                            "Platform": "LinkedIn",
                            "Title": title,
                            "Company": company,
                            "Stipend": "Undisclosed",
                            "Link": link
                        })
                    except: continue
                time.sleep(1)
            except: break
            
        print(f"   > LinkedIn: Collected {len([x for x in self.dataset if x['Platform']=='LinkedIn'])} listings.")

    # ---------------------------------------------------
    # 2. INTERNSHALA (TEXT SEARCH - NEW STRATEGY)
    # ---------------------------------------------------
    def scrape_internshala(self):
        print("\n[2/3] Scraping Internshala (Deep Scan)...")
        url = "https://internshala.com/internships/"
        
        try:
            self.driver.get(url)
            print("   > Waiting 8 seconds for page load...")
            time.sleep(8)
            
            # Close popup
            try:
                self.driver.find_element(By.CLASS_NAME, "ic-24-cross").click()
            except: pass

            # METHOD: Get all text blocks that contain "Months" (Duration) or "₹" (Stipend)
            # This ignores class names entirely
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find the main container by ID if possible, else generic
            containers = soup.find_all('div', class_='individual_internship')
            
            print(f"   > Found {len(containers)} potential containers.")
            
            count = 0
            for card in containers:
                try:
                    # Title/Company usually in heading tags
                    title_tag = card.find('h3')
                    company_tag = card.find('p', class_='company-name')
                    
                    if title_tag and company_tag:
                        title = title_tag.text.strip()
                        company = company_tag.text.strip()
                        
                        # Find Stipend in text
                        text = card.get_text()
                        stipend = "Unpaid"
                        if " /" in text or "Lump" in text or "₹" in text:
                            # Extract pattern like "₹ 10,000 /month"
                            match = re.search(r'₹\s?[\d,]+(?:\s?/-)?(?:\s?/(?:month|week))?', text)
                            if match:
                                stipend = match.group(0)
                            elif "Unpaid" in text:
                                stipend = "Unpaid"

                        self.dataset.append({
                            "Platform": "Internshala",
                            "Title": title,
                            "Company": company,
                            "Stipend": stipend,
                            "Link": "internshala.com"
                        })
                        count += 1
                except: continue
            
            print(f"   > Internshala: Collected {count} listings.")
            
        except Exception as e:
            print(f"   > Internshala Error: {e}")

    # ---------------------------------------------------
    # 3. UNSTOP (SCROLL & GRAB)
    # ---------------------------------------------------
    def scrape_unstop(self):
        print("\n[3/3] Scraping Unstop (Aggressive Scroll)...")
        url = "https://unstop.com/internships?filters=open"
        try:
            self.driver.get(url)
            print("   > Waiting 10 seconds for dynamic content...")
            time.sleep(10)
            
            # Aggressive Scrolling
            for i in range(5):
                self.driver.execute_script(f"window.scrollTo(0, {(i+1)*500});")
                time.sleep(1)
            
            # Try getting cards by broader selection
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # Look for ANY div that has 'opportunity' in class
            cards = soup.select("div[class*='opportunity']")
            
            count = 0
            for card in cards:
                try:
                    text = card.get_text(separator='|')
                    parts = text.split('|')
                    
                    # Heuristic: Title is usually the first long string
                    title = "Unknown"
                    company = "Unstop Partner"
                    
                    for part in parts:
                        if len(part) > 5 and "Intern" in part:
                            title = part
                            break
                    
                    if title != "Unknown":
                        self.dataset.append({
                            "Platform": "Unstop",
                            "Title": title,
                            "Company": company,
                            "Stipend": "Disclosed on Apply",
                            "Link": "unstop.com"
                        })
                        count += 1
                        if count >= 30: break
                except: continue
                
            print(f"   > Unstop: Collected {count} listings.")
            
        except Exception as e:
            print(f"   > Unstop Error: {e}")

    # ---------------------------------------------------
    # 4. REPORT GENERATOR
    # ---------------------------------------------------
    def generate_report(self):
        print("\n--- GENERATING REPORT ---")
        if not self.dataset: return

        # CSV Save
        try:
            with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Platform","Title","Company","Stipend","Link"])
                writer.writeheader()
                writer.writerows(self.dataset)
            print(f"   > CSV Saved: {OUTPUT_CSV}")
        except: pass

        # Analysis
        total = len(self.dataset)
        categories = Counter()
        total_stipend = 0
        paid_count = 0

        for item in self.dataset:
            t = item['Title'].lower()
            if 'software' in t or 'dev' in t or 'data' in t: categories['Tech'] += 1
            elif 'market' in t or 'sales' in t: categories['Marketing'] += 1
            elif 'hr' in t: categories['HR'] += 1
            elif 'finance' in t: categories['Finance'] += 1
            else: categories['Other'] += 1
            
            # Simple Stipend Math
            s = str(item['Stipend'])
            nums = re.findall(r'\d+', s.replace(',', ''))
            if nums:
                val = int(nums[0])
                if val > 500: 
                    total_stipend += val
                    paid_count += 1
        
        avg = int(total_stipend / paid_count) if paid_count > 0 else 0
        top = categories.most_common(1)[0] if categories else ("None", 0)

        # PDF Creation
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Kartavya.ai Internship Report", ln=1, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Total Analyzed: {total}", ln=1)
            pdf.cell(0, 10, f"Top Domain: {top[0]} ({top[1]} listings)", ln=1)
            if avg > 0:
                pdf.cell(0, 10, f"Average Stipend: INR {avg:,} / month", ln=1)
            else:
                pdf.cell(0, 10, f"Average Stipend: Data Unavailable (Mostly Unpaid)", ln=1)
            
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Listings Found:", ln=1)
            pdf.set_font("Arial", size=10)
            
            for i, row in enumerate(self.dataset[:15]):
                txt = f"{i+1}. [{row['Platform']}] {row['Title']} ({row['Stipend']})"
                clean = txt.encode('latin-1', 'ignore').decode('latin-1')
                pdf.cell(0, 8, clean, ln=1)
                
            pdf.output(OUTPUT_PDF)
            print(f"   > PDF Saved: {OUTPUT_PDF}")
        except Exception as e:
            print(f"   > PDF Error: {e}")

    def close(self):
        try:
            self.driver.quit()
        except: pass

if __name__ == "__main__":
    bot = KartavyaSystem()
    bot.scrape_linkedin()    
    bot.scrape_internshala() 
    bot.scrape_unstop()
    bot.generate_report()
    bot.close()