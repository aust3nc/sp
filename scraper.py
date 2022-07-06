import requests
from bs4 import BeautifulSoup
import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession

class S:
    #start html session
    def get_source(self, url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
    #return user query
    def get_query(self):
        return input("Enter a search query: ")
    #get list of links from google query
    def scrape_google(self):
        q = self.get_query()
        query = urllib.parse.quote_plus(q)
        response = self.get_source("https://www.google.com/search?q=" + query)
        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                        'https://google.', 
                        'https://webcache.googleusercontent.', 
                        'http://webcache.googleusercontent.', 
                        'https://policies.google.',
                        'https://support.google.',
                        'https://maps.google.')
        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)
        return links
    #write output of first 15 links to file
    def make_query(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        urls = self.scrape_google()
        for url in urls[:20]:
            request = urllib.request.Request(url, None, headers) 
            response = urllib.request.urlopen(request)
            parsed = BeautifulSoup(response, 'html.parser')
            for strings in parsed.find_all('p'):
                #text = strings.get_text()
                file_object = open('raw.txt', 'a')
                # Append 'hello' at the end of file
                file_object.write(strings.get_text())
            file_object.close()
    #open file and read contents
    def verify_text(self):
        with open('raw.txt', "r") as f: 
            print(f.read())
