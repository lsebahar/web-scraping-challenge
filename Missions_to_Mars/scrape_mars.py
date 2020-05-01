# Dependencies
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from selenium import webdriver
from requests import get
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    ### NASA MARS NEWS

    # Copying URL into a variable
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Visiting URL with browser
    browser.visit(url)

    # Using specific CSS class to find first title
    news_title = browser.find_by_css('div[class="content_title"] a').text

    # Using specific CSS class to find first article teaser
    news_p = browser.find_by_css('div[class="article_teaser_body"]').text

    ### SPACE IMAGES - FEATURED IMAGE

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # Visiting URL for image we want to copy
    browser.visit(image_url)

    #Inspected id tag on button to enlarge image
    browser.find_by_id("full_image").click()

    # Used inspector to find div id that contains image; refined to copy source URL
    featured_image_url = browser.find_by_id("fancybox-lock").find_by_tag('img')['src']

    # Copying URL into a variable
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'

    # Visiting the page on browser
    browser.visit(mars_twitter_url)

    # Finding the text, the constructing a path to retrieve text from HTML/CSS
    mars_weather = browser.find_by_tag('article').find_by_css('span[class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"]')[4].text

    ### MARS FACTS

    # Setting URL as variable
    mars_facts_url = 'https://space-facts.com/mars/'

    # Using Pandas to pull table as HTML table string
    tables = pd.read_html(mars_facts_url)

    # Converting to DataFrame
    df = pd.DataFrame(tables[0])
    df.columns = ['Attribute', 'Value']
    df.set_index('Attribute', inplace=True)

    # Converting to HTML, deleting spaces
    html_table = df.to_html().replace('\n','')

    ### MARS HEMISPHERES
    #hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Navigating to browser
    #browser.visit(hemisphere_url)

    # Create lists to drop in titles/links
    #titles = []
    #img_links = []

    # Looping through item classes & gathering titles/links
    #for x in range(4):
        #hem = browser.find_by_css('div[class="item"]')[x].find_by_tag('h3').text
        #pic = browser.find_by_css('div[class="item"]')[x].find_by_tag('a')["href"]
        #titles.append(hem)
        #img_links.append(pic)

    # Creating list for dictionaries
    #hemisphere_image_urls = []

    # Creating dictionary
    #for x in range(4):
        #dic = {'title': titles[x], "img_url": img_links[x]}
        #hemisphere_image_urls.append(dic)

    py_dict = {"News_Title": news_title,
        "News_Paragraph": news_p,
        "Mars_Featured_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Facts_Table": html_table,
        #"Mars Hemispheres": hemisphere_image_urls
    }

    browser.quit()

    return py_dict
