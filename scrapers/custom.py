def scrape_custom(base_url, employer, keywords):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for title_tag in soup.find_all('h3'):
        title = title_tag.text.strip()
        url_tag = title_tag.find_next_sibling('a', class_='job-url')
        if url_tag:
            url = url_tag['href']
            if any(keyword.lower() in title.lower() for keyword in keywords):
                jobs.append({
                    'title': title,
                    'url': url,
                    'employer': employer
                })
    return jobs
