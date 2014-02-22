import urllib2
import pprint
import re
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
    imageURL = extract_high_rez_image_url(html)
    # Trick RES into displaying the imagine inline
    imageURL += '?f.jpg'
    print "Posting '%s', '%s'" % (stripTitle, imageURL)

    # Post it to Reddit
    r = praw.Reddit(user_agent="CalvinBot")
    r.login('calvinbot', 'webpasswd')
    
    # Production
    r.submit('calvinandhobbes', stripTitle, url=imageURL)

    # Testing
    #    r.submit('calvinbot', stripTitle, url=imageURL)
    

# Old extraction method (lower rez image)
def extract_image_url(html):
    soup = BeautifulSoup(html)
    url_meta = soup.find('meta', attrs={'property': 'og:image', 'content': True})
    url = url_meta['content']
    return url

def extract_high_rez_image_url(html):
    soup = BeautifulSoup(html)
    tag = soup.find(src=re.compile("width=900"))
    url = tag['src']
    url = re.sub('\?width=900', '', url)
    return url
    
def pull_rss():
    feed = feedparser.parse( RSS_FEED )
    for entry in feed.entries:
        print "====="
        pp.pprint(entry)

if __name__ == "__main__":
    main()
