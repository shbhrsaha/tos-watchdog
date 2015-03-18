"""
    Reads domains from stdin and prints URLs of their terms of service
    and privacy policies to stdout

    Usage:
        python src/domains-to-urls.py < src/alexa-top-100.txt > urls.txt
"""

import sys
import logging
from pattern.web import URL, DOM, abs, plaintext

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

TERMS_KEYWORD = "terms"
PRIVACY_KEYWORD = "privacy"

def select_best(a_list, base_url, keyword=TERMS_KEYWORD):
    """
        Given a list of 'a' elements,
        returns the one that best first the given term
    """
    if not a_list:
        return None

    if len(a_list) == 1:
        return get_absolute_url(a_list[0], base_url)

    for a in a_list:
        full_url_str = get_absolute_url(a, base_url)
        full_url = URL(full_url_str)

        if full_url.domain != base_url.domain:
            continue

        if keyword == TERMS_KEYWORD:
            if "terms of service" in a.string.lower():
                return full_url_str
        if keyword == PRIVACY_KEYWORD:
            if "privacy policy" in a.string.lower():
                return full_url_str

    return None

def get_absolute_url(relative_url, base_url):
    """
        Returns the absolute URL given base and relative URLs
    """
    return abs(relative_url.attributes.get('href',''), base=base_url.redirect or base_url.string)

for line in sys.stdin:
    domain = line.replace("\n","")
    logging.info(domain)
    url_home = URL("http://"+domain)
    try:
        html_home = url_home.download()
    except:
        continue
    dom_home = DOM(html_home)

    a_terms = [a for a in dom_home('a') if TERMS_KEYWORD in a.attributes.get('href','')]
    a_privacy = [a for a in dom_home('a') if PRIVACY_KEYWORD in a.attributes.get('href','')]

    terms_url = select_best(a_terms, url_home, TERMS_KEYWORD)
    privacy_url = select_best(a_privacy, url_home, PRIVACY_KEYWORD)

    if terms_url:
        print terms_url
    if privacy_url:
        print privacy_url