import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs

def scrape():

    mars_data = {}

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find_all("div", class_="content_title")[1].text
    mars_data["news_title"] = news_title
    news_para = soup.find("div", class_="article_teaser_body").text
    mars_data["news_para"] = news_para

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    html = browser.html
    soup = bs(html, "html.parser")

    featured_image = soup.find_all("a", class_="fancybox")[1]["data-fancybox-href"]
    featured_image_url = "https:/www.jpl.nasa.gov" + featured_image
    mars_data["featured_image_url"] = featured_image_url

    url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(url)

    mars_df = mars_facts[0]
    mars_df.columns = ["Description", "Mars"]
    mars_df.set_index("Description", inplace=True)
    mars_html = mars_df.to_html()

    mars_data["mars_facts"] = mars_html

    url3 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url3)
    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere = {}
    hemisphere_image_urls = []
    array = soup.find_all("div", class_="item")

    for img in array:
        title = img.find("h3").text
        hemisphere["title"] = title
        imgurl = img.find("a", class_="itemLink product-item")["href"]
        browser.visit("https://astrogeology.usgs.gov" + imgurl)

        imgurl = browser.html
        soup = bs(imgurl, "html.parser")
        image_url = "https://astrogeology.usgs.gov" + soup.find("img", class_="wide-image")["src"]
        hemisphere["img_url"] = image_url

        hemisphere_image_urls.append(hemisphere)
    
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    
    browser.quit()

    return mars_data    
