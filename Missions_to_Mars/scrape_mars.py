import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# def mars_news()


def scrape():
    # Visit the NASA Mars News Site and scrape the latest News Title and Paragraph Text
    browser = init_browser()
    # create mars_data dict that we can insert into mongo
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    # create a soup object from the html
    soup = BeautifulSoup(html, 'html.parser')
    mars_data_scrape = {}
    news_article = soup.find("div", class_='list_text')
    news_title = news_article.find("div", class_="content_title").text
    news_p = news_article.find('div', class_="article_teaser_body").text
    mars_data_scrape['title'] = news_title
    mars_data_scrape['p'] = news_p
    # print(mars_data_scrape['title'])
    # print(mars_data_scrape['p'])

    # Visit the url for JPL and scrape the Featured Space Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    # Find 'FULL IMAGE' button and have splinter click it
    full_img_button = browser.links.find_by_partial_text('FULL IMAGE')
    full_img_button.click()
    time.sleep(1)

    # Find 'more info' button and have splintr click
    more_info_element = browser.links.find_by_partial_text('more info')
    more_info_element.click()
    time.sleep(1)
    # Get the result html with beautiful soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Use beautiful soup to find full size jpeg image
    figure_element = soup.find('figure', class_='lede')
    full_image_url = figure_element.a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{full_image_url}'
    mars_data_scrape['img_url'] = featured_image_url
    # print(mars_data_scrape['img_url'])

    # Visit the url and scrape Mars Facts
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #browser = Browser('chrome', **executable_path, headless=False)
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    df = pd.read_html(url)
    mars_facts_df = df[0]
    mars_facts_df.columns = ['Description', 'Values']
    mars_facts_df = mars_facts_df.set_index('Description', drop=True)
    html = mars_facts_df.to_html()
    mars_data_scrape['table'] = html
    # print(mars_data_scrape['table'])

    # Visit the url for Mars Hemispheres and scrape the hemispheres
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #browser = Browser('chrome', **executable_path, headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    hemispheres = soup.find_all('h3')
    # print(hemispheres)

    hemisphere_dict = {}
    hemisphere_image_urls = []
    for hemisphere in hemispheres:
        title = hemisphere.get_text()
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        img_url = browser.links.find_by_partial_text('Sample')['href']
        hemisphere_dict = {'title': title, 'url': img_url}
        hemisphere_image_urls.append(hemisphere_dict)
        browser.visit(url)
        mars_data_scrape['hemispheres'] = hemisphere_image_urls
    print(mars_data_scrape['hemispheres'])

    browser.quit()

    return mars_data_scrape
