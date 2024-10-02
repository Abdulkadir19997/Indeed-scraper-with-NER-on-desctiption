from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Function to clean text by removing extra newlines and spaces
def clean_text(text):
    return ' '.join(text.split()).replace('&nbsp;', '')

# Function to close cookie consent or banners if they appear
def handle_popup(driver):
    try:
        # Wait for the cookie consent or popup banner and click "Accept" or close it
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_button.click()
        time.sleep(1)  # Wait for the banner to disappear
    except Exception as e:
        # If no banner appears, just continue
        pass

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
url = 'https://uk.indeed.com/jobs?q=private+client+solicitor&l=England&sc=0bf%3Aexrec%28%29%3B&vjk=510078d1db3d7788'
driver.get(url)
handle_popup(driver)

data = []
while True:
    try:
        # Find all job cards on the page
        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.cardOutline.tapItem")
        for job_card in job_cards:
            try:
                # Extract job information
                job_title_element = job_card.find_element(By.CSS_SELECTOR, "h2.jobTitle")
                job_title = clean_text(job_title_element.text.replace(' - job post', '').strip())
                company_element = job_card.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']")
                company_name = clean_text(company_element.text.strip())
                location_element = job_card.find_element(By.CSS_SELECTOR, "div[data-testid='text-location']")
                location = clean_text(location_element.text.strip())
                job_link_element = job_card.find_element(By.CSS_SELECTOR, "a.jcs-JobTitle")
                job_link = job_link_element.get_attribute("href")

                job_link_element.click()
                time.sleep(2)  # Wait for the job details to load
                description_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div#jobDescriptionText"))
                )
                full_description = clean_text(description_element.text.strip())
                driver.back()
                time.sleep(2)

                # Store the extracted information
                job_data = {
                    'Law Firm': company_name,
                    'Title': job_title,
                    'Location': location,
                    'Website': job_link,
                    'Description': full_description
                }
                data.append(job_data)
            except Exception as e:
                print(f"Error processing a job card: {e}")

        # Find and click the 'Next Page' link
        next_page_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='pagination-page-next']"))
        )
        if next_page_link:
            next_page_link.click()
            time.sleep(2)
        else:
            break
    except Exception as e:
        print(f"Error navigating pages or extracting data: {e}")
        break

# Save the extracted data to a CSV file
df = pd.DataFrame(data)
df.to_csv('scraped_data.csv', index=False, quoting=1, quotechar='"')
print("Data saved to 'scraped_job_listings.csv'")
driver.quit()
