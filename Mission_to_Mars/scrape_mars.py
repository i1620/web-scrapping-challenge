# Import Dependencies
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape():
#Scraping All Data
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html

    soup = bs(html, "html.parser")

    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    print(news_title)
    print(news_p)


# ## JPL Mars Space Images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    img_html = browser.html

    soup = bs(img_html, 'html.parser')
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url

    print(featured_image_url)


# ## Mars Facts

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html

    table = pd.read_html(facts_url)
    mars_facts = table[2]
    mars_facts

    mars_facts.columns = ['Description','Value']

    mars_facts.set_index('Description', inplace=True)
    mars_facts

    mars_facts.to_html('table.html')


# ## Mars Hemispheres

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    soup = bs(html, "html.parser")

    hemisphere_image_urls = []

    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    print(hemisphere_image_urls)

# scrape()