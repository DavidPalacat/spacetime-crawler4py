import re
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page.
    # Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    pagesLinks = []
    pageCon = urllib.request.urlopen(resp)  # open a connection to the current url
    pageContent = None
    resultCode = pageCon.getcode()

    if resultCode == 200:  # successful read of url
        pageContent = pageCon.read()
        pageHTML = BeautifulSoup(pageContent, 'html.parser')  # parse html
        for link in pageHTML.find_all('a'):  # for each parsed link
            pLink = link.get('href')
            if pLink != url and is_valid(pLink):  # not the link we came from and is a valid link
                pagesLinks.append(pLink)  # add to our list of links

    return pagesLinks


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if re.match(
                r".*\.(css|js|bmp|gif|jpe?g|ico"
                + r"|png|tiff?|mid|mp2|mp3|mp4"
                + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                + r"|epub|dll|cnf|tgz|sha1"
                + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False
        for domain in {".ics.uci.edu/", ".cs.uci.edu/", ".informatics.uci.edu/",
                       ".stat.uci.edu/"}:  # Check if one of the following domains is in the parsed input url.
            if domain not in parsed.netloc:
                continue
            return True
        return False
    except TypeError:
        print("TypeError for ", parsed)
        raise
