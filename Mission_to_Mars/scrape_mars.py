# Import Dependencies
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def init_browser():
    
#Scraping All Data
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()


# ## NASA Mars News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html

    time.sleep(1)

    soup = bs(html, "html.parser")

    #article = soup.find("div", class_='list_text')
    #news_title = article.find("div", class_="content_title").text
    #news_p = article.find("div", class_ ="article_teaser_body").text

    article = soup.select_one("ul.item_list li.slide")
    news_title = article.find("div", class_="content_title").get_text()
    news_p = article.find("div", class_ ="article_teaser_body").get_text()



# ## JPL Mars Space Images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    img_html = browser.html

    time.sleep(1)

    soup = bs(img_html, 'html.parser')
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url


# ## Mars Facts

    url_facts = "https://space-facts.com/mars/"
    tables = pd.read_html(url_facts)[0]
    tables.columns = ['Description', 'Value']
    tables.set_index('Description', inplace=True)
    mars_facts = tables.to_html()


# ## Mars Hemispheres

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    time.sleep(1)

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


# Store in a Dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data


if __name__ == '__main__':
    scrape()
