'''
--- Web scraper for imdb ---

Description: 
A tool that uses requests to scrape any given imdb page for a link to its associated trailer.

'''

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
    
def videoScraper(ID):

    ua = UserAgent()

    headers = {'User-Agent': f'{ua.chrome}'}
    response = requests.get(f'https://www.imdb.com/title/{ID}/', headers=headers)

    if response.status_code == 200: 
    
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            JScript = str(soup.find(id='__NEXT_DATA__'))
            DEFIndex = JScript.index('DEF_480p')
            JScript = JScript[DEFIndex : (DEFIndex + 654)]
        except:
            return None # No Trailer Exists
        
        videoElementPassOne = re.search(r"https:\/\/imdb-video\.media-imdb\.com[^\"]*", JScript) # obtains video using regular expression
        
        videoElementPassTwo = videoElementPassOne.group() 
        videoElementPassTwo = videoElementPassTwo.replace("\\u0026", "&")

        return videoElementPassTwo
    
    print("Bad Repsonse")
    return None

if __name__ == '__main__':
     
    print (videoScraper('tt0367413')) # replace with any valid imdb movie id
    



    


