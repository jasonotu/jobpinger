def scrape_workday(base_url, employer, keywords):
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

    driver.get(base_url)
    time.sleep(5)

    jobs = []
    total_pages = 1
    
    try:
        pagination_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-uxi-widget-type="paginationPageButton"]')
        if pagination_buttons:
            total_pages = int(pagination_buttons[-1].get_attribute('aria-label').split()[-1])
    except Exception as e:
        print("Error finding pagination buttons:", e)

    for current_page in range(1, total_pages + 1):
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-automation-id="jobTitle"]')
        for job in job_elements:
            title = job.text
            url = job.get_attribute('href')
            if any(keyword.lower() in title.lower() for keyword in keywords):
                jobs.append({
                    'title': title,
                    'url': url,
                    'employer': employer
                })

        if current_page < total_pages:
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-uxi-element-id^="page "]'))
                )
                next_button.click()
                time.sleep(5)
            except Exception as e:
                print("Error clicking next button:", e)
                break

    driver.quit()
    return jobs
