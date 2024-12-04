def scrape_successfactors(url, employer, keywords):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(5)

    jobs = []
    
    while True:
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-automation-id="jobTitle"]')
        for job in job_elements:
            title = job.text.strip()
            job_url = job.get_attribute('href')
            if any(keyword.lower() in title.lower() for keyword in keywords):
                jobs.append({
                    'title': title,
                    'url': job_url,
                    'employer': employer
                })

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.paginationArrow[aria-label="Next Page"]'))
            )
            next_button.click()
            time.sleep(5)
            current_page += 1
        except Exception:
            break

    driver.quit()
    return jobs