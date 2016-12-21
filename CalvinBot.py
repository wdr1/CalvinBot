import urllib2
import pprint
import re
from datetime import date
import ConfigParser
import argparse

from bs4 import BeautifulSoup
import praw

pp = pprint.PrettyPrinter(indent=4)

def main():
    # Basic config 
    Config = ConfigParser.ConfigParser()
    Config.read("calvinbot.config")
    username = Config.get('Global', 'username')
    password = Config.get('Global', 'password')
    useragent = Config.get('Global', 'useragent')
    client_id = Config.get('Global', 'client_id')
    client_secret = Config.get('Global', 'client_secret')

    # CLI options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug',
        help="Print debugging & if submitting, switch to /r/calvinbot",
        action="store_true"
    )
    parser.add_argument(
        '-n', '--dryrun',
        help="Don't submit new post",
        action="store_true"
    )

    # Which subreddit
    args = parser.parse_args()
    subreddit = 'calvinandhobbes'
    if args.debug:
        subreddit = 'calvinbot'

    # Today's URL & Title
    d = date.today()
#    d = d - timedelta(days=2)
    stripURL = d.strftime("http://www.gocomics.com/calvinandhobbes/%Y/%m/%d")
    print "stripURL: '%s'" % stripURL
    stripTitle = d.strftime("Calvin & Hobbes for %B %e, %Y")

    # Get the URL of the actual strip
    req = urllib2.Request(stripURL, None, { 'User-Agent' : 'CalvinBot 1.0' })
    response = urllib2.urlopen(req)
    html = response.read()
    imageURL = extract_high_rez_image_url(html)
    
    print "Posting to '%s', '%s', '%s'" % (subreddit, stripTitle, imageURL)

    # Post it to Reddit
    r = praw.Reddit(user_agent=useragent,
                    username=username,
                    password=password,
                    client_id=client_id,
                    client_secret=client_secret
    )
    r.login(username, password, disable_warning=True)
    if not args.dryrun:
        r.submit(subreddit, stripTitle, url=imageURL)

# Old extraction method (lower rez image)
def extract_image_url(html):
    soup = BeautifulSoup(html, "html.parser")
    url_meta = soup.find('meta', attrs={'property': 'og:image', 'content': True})
    url = url_meta['content']
    return url

def extract_high_rez_image_url(html):
    print "Looking for hi rez urls, yo"
    soup = BeautifulSoup(html, "html.parser")
    tag = ( soup.findAll("img", { "class" : "strip" }) )[1]
    pp.pprint(tag)
    url = tag['src']
    # Trick RES into displaying the imagine inline
    url += '.jpg'
    
    return url
    
def pull_rss():
    feed = feedparser.parse( RSS_FEED )
    for entry in feed.entries:
        print "====="
        pp.pprint(entry)

if __name__ == "__main__":
    main()
