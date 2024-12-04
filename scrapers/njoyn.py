def scrape_njoyn(base_url, employer, keywords):
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for row in soup.find_all('tr'):
        job_link = row.find('a')
        td_elements = row.find_all('td')

        if len(td_elements) > 1 and job_link:
            title = td_elements[1].text.strip()
            relative_url = job_link['href']

            full_url = urljoin(base_url, relative_url)

            if any(keyword.lower() in title.lower() for keyword in keywords):
                jobs.append({
                    'title': title,
                    'url': full_url,
                    'employer': employer
                })
    return jobs