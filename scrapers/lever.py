def scrape_lever(base_url, employer, keywords):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for title_tag in soup.find_all('a', class_='posting-title'):
        job_title_element = title_tag.find('h5', {'data-qa': 'posting-name'})
        if job_title_element:
            title = job_title_element.text.strip()
            url = title_tag['href']
            if any(keyword.lower() in title.lower() for keyword in keywords):
                jobs.append({
                    'title': title,
                    'url': url,
                    'employer': employer
                })
    return jobs
