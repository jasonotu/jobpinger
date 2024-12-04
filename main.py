import yaml
import argparse
from scrapers import  lever, workday, jazzhr, njoyn, rss, successfactors, successfactors2, custom
from send_mail import send_mail
from halo import Halo

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description='Job Pinger')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show details on what is currently being scraped')
    parser.add_argument('-n', '--no-email', action='store_true', help='Skip sending email notifications')
    args = parser.parse_args()

    config = load_config()
    keywords = config['keywords']
    all_jobs = []
    seen_jobs = set()

    spinner = Halo(text='Searching', spinner='dots')
    if not args.verbose:
        spinner.start()
    for employer, details in config['employers'].items():
        platform = details['platform']
        url = details['url']
        
        if platform == 'jazzhr':
            if args.verbose:
                print(f"Searching {employer} ({platform})")
            jobs = jazzhr.scrape_jazzhr(url, employer, keywords)
            all_jobs.extend(jobs)
        
        elif platform == 'lever':
            if args.verbose:
                print(f"Searching {employer} ({platform})")
            jobs = lever.scrape_lever(url, employer, keywords)
            all_jobs.extend(jobs)

        elif platform == 'workday':
            if args.verbose:
                print(f"Searching {employer} ({platform})")
            jobs = workday.scrape_workday(url, employer, keywords)
            all_jobs.extend(jobs)

        elif platform == 'njoyn':
            if args.verbose:
                print(f"Searching {employer} ({platform})")
            jobs = njoyn.scrape_njoyn(url, employer, keywords)
            all_jobs.extend(jobs)

        elif platform == 'rss':
            if args.verbose:
                print(f"Searching {employer} ({platform})")
            jobs = rss.scrape_rss(url, employer, keywords)
            all_jobs.extend(jobs)

        elif platform == 'successfactors':
            if args.verbose:
                print(f"Searching {employer} ({platform})")
            jobs = successfactors.scrape_successfactors(url, employer, keywords)
            all_jobs.extend(jobs)

        elif platform == 'successfactors2':
            if args.verbose:
                print(f"Searching {employer} ({platform})")
            jobs = successfactors2.scrape_successfactors2(url, employer, keywords)
            all_jobs.extend(jobs)

        elif platform == 'custom':
            if args.verbose:
                print(f"Searching {employer} ({platform})")
            jobs = custom.scrape_custom(url, employer, keywords)
            all_jobs.extend(jobs)
    if not args.verbose:
        spinner.stop()

    # Remove duplicates
    unique_jobs = []
    for job in all_jobs:
        job_identifier = (job['title'], job['url'])
        if job_identifier not in seen_jobs:
            seen_jobs.add(job_identifier)
            unique_jobs.append(job)

    all_jobs = unique_jobs

    if all_jobs:
        print("Found jobs!\n")
        for job in all_jobs:
            print(f"{job['title']} at {job['employer']}: {job['url']}\n")
        if not args.no_email:
            print("Sending pings!")
            subject = "New Job Listings Found!"
            body = "\n".join([f"{job['title']} at {job['employer']}: {job['url']}" for job in all_jobs])
            send_mail(subject, body, [config['receiver_email']])
    else:
        print("No matching jobs found.")

if __name__ == "__main__":
    main()
