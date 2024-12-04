def scrape_rss(base_url, employer, keywords):
    import requests
    import lxml
    from bs4 import BeautifulSoup

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'lxml-xml')

    jobs = []
    for item in soup.find_all('item'):
        title = item.find('title').text.strip()
        link = item.find('link').text.strip().lower()

        if any(keyword.lower() in title.lower() for keyword in keywords):
            jobs.append({
                'title': title,
                'url': link,
                'employer': employer
            })
    return jobs
