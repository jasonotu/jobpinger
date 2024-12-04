def scrape_jazzhr(url, employer, keywords):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job in soup.find_all('h4', class_='list-group-item-heading'):
        title = job.find('a').text.strip()
        job_url = job.find('a')['href']
        if any(keyword.lower() in title.lower() for keyword in keywords):
            jobs.append({
                'title': title,
                'url': job_url,
                'employer': employer
            })
    return jobs