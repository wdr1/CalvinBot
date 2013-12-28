import urllib2
import pprint
from datetime import date

from bs4 import BeautifulSoup
import praw

pp = pprint.PrettyPrinter(indent=4)

def main():
    # Today's URL & Title
    d = date.today()
    stripURL = d.strftime("http://www.gocomics.com/calvinandhobbes/%Y/%m/%d")
    print "stripURL: '%s'" % stripURL
    stripTitle = d.strftime("Calvin & Hobbes for %B %e, %Y")

    # Get the URL of the actual strip
    req = urllib2.Request(stripURL, None, { 'User-Agent' : 'CalvinBot 1.0' })
    response = urllib2.urlopen(req)
    html = response.read()
    imageURL = extract_image_url(html)
    print "Posting '%s', '%s'" % (stripTitle, imageURL)

    # Post it to Reddit
    r = praw.Reddit(user_agent="CalvinBot")
    r.login('calvinbot', 'webpasswd')
    r.submit('calvinbot', stripTitle, url=imageURL)
    
def extract_image_url(html):
    soup = BeautifulSoup(html)
    url_meta = soup.find('meta', attrs={'property': 'og:image', 'content': True})
    url = url_meta['content']
    return url
    
def pull_rss():
    feed = feedparser.parse( RSS_FEED )
    for entry in feed.entries:
        print "====="
        pp.pprint(entry)

if __name__ == "__main__":
    main()
