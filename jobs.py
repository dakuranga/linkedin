import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

try:
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    linkedin_email = "ashish.paliwal@linksft.com"
    linkedin_password = "Arleen@linksofttech8741$"

    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "session_key")))
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "session_password")))
    sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Sign in']")))

    email_input.send_keys(linkedin_email)
    password_input.send_keys(linkedin_password)
    sign_in_button.click()

    job_search_url = "https://www.linkedin.com/jobs/search/?currentJobId=3736772758&keywords=oscp&origin=SWITCH_SEARCH_VERTICAL"
    driver.get(job_search_url)
    time.sleep(5)

    job_data = []

    # Maximum number of pages to scrape
    max_pages = 1
    current_page = 1

    while current_page <= max_pages:
        # Scroll through the page to load all job postings
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(3)

        job_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'job-card-list__title')]")

        for job_element in job_elements:
            job_element.click()
            time.sleep(2)

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2.t-24.t-bold")))

                job_title = driver.find_element(By.CSS_SELECTOR, "h2.t-24.t-bold").text
                company_name = driver.find_element(By.CSS_SELECTOR, "a.link-without-visited-state.inline-block.t-black").text.strip()

                job_details = driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__primary-description div").text.strip()
                location = job_details.split('·')[1].strip()

                company_info = driver.find_element(By.CSS_SELECTOR, "li.job-details-jobs-unified-top-card__job-insight + li span").text.strip().split('·')
                company_size = company_info[0].strip()
                company_industry = company_info[1].strip()

                company_linkedin_url = driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__primary-description a.app-aware-link").get_attribute('href')

                job_data.append({
                    'Job Title': job_title,
                    'Company Name': company_name,
                    'Location': location,
                    'Company Size': company_size,
                    'Company Industry': company_industry,
                    'Company Linkedin': company_linkedin_url,
                })
            except Exception as e:
                # Handle the exception (e.g., log an error message)
                print(f"An error occurred while processing a job listing: {e}")

        # Check if there's a "Next" button
        next_page_button = driver.find_element(By.XPATH, f'//button[@aria-label="Page {current_page + 1}"]')
        if next_page_button.is_enabled():
            next_page_button.click()
            time.sleep(5)
            current_page += 1
        else:
            print(f"Could not find button for page {current_page + 1}. Ending scraping.")
            break

except KeyboardInterrupt:
    # Handle keyboard interrupt (e.g., save data to Excel)
    print("Keyboard interrupt detected. Saving data to Excel...")
    df = pd.DataFrame(job_data)
    df.to_excel("job_data.xlsx", index=False)
    print("Data saved to Excel.")
    driver.quit()
    sys.exit(0)  # Exit the script gracefully
else:
    # If the loop completes without interruption, save data to Excel and quit
    df = pd.DataFrame(job_data)
    df.to_excel("job_data.xlsx", index=False)
    print("Data saved to Excel.")
    driver.quit()
