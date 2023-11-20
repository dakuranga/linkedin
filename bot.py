import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
]

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")

linkedin_email = "ashish.paliwal@linksft.com"
linkedin_password = "Arleen@linksofttech8741$"

email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "session_key"))
)
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "session_password"))
)
sign_in_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Sign in']"))
)
email_input.send_keys(linkedin_email)
password_input.send_keys(linkedin_password)
sign_in_button.click()

input_file_path = "C:/Users/ashis/Downloads/urls.txt"

try:
    with open(input_file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]
except FileNotFoundError:
    print(f"File not found: {input_file_path}")
    driver.quit()
    exit()

def scrape_linkedin_company(url):
    driver.get(url)
    time.sleep(5)

    error_message_selector = '//h2[contains(@class, "artdeco-empty-state__headline") and contains(text(), "isn’t available")]'

    try:
        error_message = driver.find_element_by_xpath(error_message_selector)
        if error_message:
            return "N/A", "N/A"  
    except Exception:
        pass 

    size_selector = '//span[contains(@class, "t-normal t-black--light link-without-visited-state link-without-hover-state")]'
    industry_selector = '//div[contains(@class, "org-top-card-summary-info-list__info-item")][text()[normalize-space()]]'

    try:
        industry = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, industry_selector))
        ).text.strip()
    except Exception as e:
        print(f"Could not retrieve industry for {url}. Error: {e}")
        industry = "N/A"

    try:
        size = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, size_selector))
        ).text.strip()
    except Exception as e:
        print(f"Could not retrieve size for {url}. Error: {e}")
        size = "N/A"

    wait_time = random.uniform(2, 5)
    time.sleep(wait_time)
    return industry, size

data = {"URL": [], "Industry": [], "Company Size": []}

for url in urls:
    industry, size = scrape_linkedin_company(url)
    data["URL"].append(url)
    data["Industry"].append(industry)
    data["Company Size"].append(size)

df = pd.DataFrame(data)
excel_filename = "linkedin_companies.xlsx"
df.to_excel(excel_filename, index=False)
print(f"Data exported to {excel_filename}")

driver.quit()
