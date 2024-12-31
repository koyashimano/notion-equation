from urllib.parse import urlparse


def extract_page_id(url):
    parsed_url = urlparse(url)
    last_part = parsed_url.path.split("/")[-1]
    page_id = last_part[-32:]
    return page_id
