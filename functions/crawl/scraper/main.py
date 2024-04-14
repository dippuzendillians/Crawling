import json
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import re


def sanitize_text(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text




headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}


def craw_subsequent_links(url, start_time, timeout,data, visited=None):
    if visited is None:
        visited = []

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    a_tags = soup.find_all("a")
    hrefs = set(a.get("href") for a in a_tags if a.get("href"))

    for href in hrefs:
        if time.time() - start_time > timeout:
            break
        # Resolve relative URLs and remove fragments
        full_url = urljoin(url, href.split("#")[0])
        # Avoid crawling external links or revisiting pages
        if (
            full_url not in visited
            and urlparse(full_url).netloc == urlparse(url).netloc
        ):
            print(f"Crawling: {full_url}")
            n_response = requests.get(full_url, headers=headers)
            n_soup = BeautifulSoup(n_response.text, "html.parser")
            visited.append(full_url)
            data.append(
                {
                    "url": full_url,
                    "title": n_soup.title.text.strip() if n_soup.title else "No Title",
                    "content": sanitize_text(n_soup.get_text()),
                }
            )
            # Recursively crawl subsequent links
            try:
                data.extend(craw_subsequent_links(full_url, start_time, visited,data=data))
            except:
                continue


def lambda_handler(event, context):

    url = event["url"]
    timeout = int(event["timeout"])
    job_id = event["job_id"]
    data = []
    start_time = time.time()
    craw_subsequent_links(url, start_time, timeout,data)

    requests.post(
        f"https://dippuzen.com/api/crawl/{job_id}",
        json={"duration": round(time.time() - start_time, 2), "scraped_items": len(data), "data": data},
    )

    return {"statusCode": 200, "body": json.dumps({"data": data})}


