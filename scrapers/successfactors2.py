def scrape_successfactors2(url, employer, keywords):
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
    total_pages = 1 

    try:
        pagination_links = driver.find_elements(By.CSS_SELECTOR, 'a[rel="nofollow"]')
        if pagination_links:
            total_pages = max(int(link.text) for link in pagination_links if link.text.isdigit())
    except Exception as e:
        print(f"Error finding total pages: {e}")

    current_page = 1
    while current_page <= total_pages:        
        job_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.jobTitle.visible-phone'))
        )
        
        for job in job_elements:
            title_link = job.find_element(By.CSS_SELECTOR, 'a.jobTitle-link')
            title = title_link.get_attribute('innerText').strip()
            job_url = title_link.get_attribute('href')
            
            if any(keyword.lower() in title.lower() for keyword in keywords):
                jobs.append({
                    'title': title,
                    'url': job_url,
                    'employer': employer
                })

        current_page += 1
        if current_page <= total_pages:
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.paginationItemLast'))
                )
                next_button.click()
                time.sleep(5)
            except Exception:
                break

    driver.quit()
    return jobs