from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in the background
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")  # Suppress logs

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open LinkedIn AI Engineer job listings
job_listings_url = "https://www.linkedin.com/jobs?q=AI+Engineer"
driver.get(job_listings_url)

# Wait for job listings to load
try:
    # Increase wait time if necessary
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
    )

    # Extract job descriptions (Adjust the element selector according to LinkedIn's structure)
    job_descriptions = []
    jobs = driver.find_elements(By.CLASS_NAME, "job-card-list__description")  # Adjust class as per inspection

    for job in jobs:
        job_descriptions.append(job.text)

    # Save job descriptions to a text file
    with open("job_descriptions.txt", "w", encoding="utf-8") as f:
        for jd in job_descriptions:
            f.write(jd + "\n\n")

    print(f"✅ Successfully saved {len(job_descriptions)} job descriptions to job_descriptions.txt")

except Exception as e:
    print(f"❌ Failed to retrieve job listings. Error: {e}")

finally:
    driver.quit()  # Close browser
