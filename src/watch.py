"""
    Monitors documents and publishes changes to GitHub
"""

import sys
import time
import logging
import textwrap
import requests
import base64
import json

from goose import Goose
from slugify import slugify
from pattern.web import URL

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

auth_token = sys.argv[1]
REPOSITORY_API_URL = "https://api.github.com/repos/shbhrsaha/terms-of-service-watchdog"
WAIT_TIME = 3600

def get_file(github_location):
    """
        Returns file contents and metadata from GitHub
    """
    url = "%s/contents%s" % (REPOSITORY_API_URL, github_location)
    response = requests.get(url, auth=(auth_token, 'x-oauth-basic'))
    return response.json()

def create_file(github_location, content):
    """
        Creates a file on GitHub and returns False if it already exists
    """
    params = {
        "message" : "Creating file",
        "content" : base64.b64encode(content)
    }
    url = "%s/contents%s" % (REPOSITORY_API_URL, github_location)
    r = requests.put(url, auth=(auth_token, 'x-oauth-basic'), data=json.dumps(params))
    response = r.json()
    if "content" in response:
        return True

    return False

def update_file(github_location, content_new, sha):
    """
        Update a file that already exists on GitHub
    """
    params = {
        "message" : "Update at %s" % str(int(time.time())),
        "content" : base64.b64encode(content_new),
        "sha" : sha
    }
    url = "%s/contents%s" % (REPOSITORY_API_URL, github_location)
    r = requests.put(url, auth=(auth_token, 'x-oauth-basic'), data=json.dumps(params))
    response = r.json()
    if "content" in response:
        return True

    return False


url_file_contents = base64.b64decode(get_file("/urls.txt")["content"])
urls = [url for url in url_file_contents.split("\n") if url]

g = Goose()
tw = textwrap.TextWrapper(width=80, replace_whitespace=False, drop_whitespace=False)


while True:
    for url in urls:
        logging.info("Processing %s" % url)

        url_obj = URL(url)
        domain = url_obj.domain
        path = url_obj.path
        doc_code = slugify("-".join(path))+"-doc.txt"
        github_location = "/content/%s/%s" % (slugify(domain), doc_code)

        try:
            content_new = g.extract(url=url).cleaned_text.encode('ascii', 'replace')
            content_new = "\n".join(tw.wrap(content_new))
            content_new = "[ TOS Watchdog retrieved from: %s ] \n\n %s" % (url, content_new)
        except:
            logging.info("Content retrieval failed")
            continue

        doc_file = get_file(github_location)

        if "content" in doc_file:
            logging.info("File exists")
            content_old = base64.b64decode(doc_file["content"])
            if content_old != content_new:
                logging.info("Updating file")
                update_file(github_location, content_new, doc_file["sha"])
            else:
                logging.info("No new content detected")

        else:
            logging.info("Creating file")
            create_file(github_location, content_new)

    logging.info("Sleeping for an hour")
    time.sleep(WAIT_TIME)