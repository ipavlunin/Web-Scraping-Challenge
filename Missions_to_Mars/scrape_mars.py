#import required libraries
import os
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver  
import requests as req
import pandas as pd


def scrape():
    # Chromedriver execution
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # URL path
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)

    # Save html and parser
    html = browser.html
    soup = bs(html, "html.parser")

    # get first news date from the url
    news_date = soup.find('li', class_='slide').find('div', class_="list_date").text
    # get first news title from the url
    news_title = soup.find('div',class_="list_text").find('div', class_="content_title").text
    # get first news text from the url
    news_text = soup.find('div',class_="list_text").find('div',class_="article_teaser_body").text
    
    # URL path
    url2 = "https://www.jpl.nasa.gov/spaceimages/"

    # Visiting url2 to click and response
    browser.visit(url2)
    browser.find_by_id('full_image').click()
    time.sleep(3)

    # Clicking on more info button
    browser.links.find_by_partial_text('more info').click()

    # Getting image URL
    featured_image_url = browser.find_by_xpath("//img[@class='main_image']")._element.get_attribute("src")
    
    # URL path
    url3 = "https://space-facts.com/mars/"

    # Finding all tables on a web page
    table = pd.read_html(url3)

    # Pick first table (Mars facts)
    table[0].columns = ['Parameter', 'Value']
    fact_table = table[0]

    # Converting DataFrame to HTML table
    table_html = fact_table.to_html()

    # Getting mars facts table data from the web page
    browser.visit(url3)

    html = browser.html
    soup = bs(html, "html.parser")

    tables = soup.findChildren('table')
    table_data=[]
    table1 = tables[0]
    rows = table1.findChildren(['th', 'tr'])   

    for row in rows:
        title = row.find('td', class_="column-1").text.strip()
        value = row.find('td', class_="column-2").text.strip()
        table_data.append({'Parameter': title, 'Value': value})

    table_data

    # URL path
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    browser.url
    html = browser.html

    # Parsering and scrapping list of images
    soup = bs(html, "html.parser")
    images = soup.find_all('div', class_="description")
    link = f"https://astrogeology.usgs.gov"
    time.sleep(3)

    # Looping thorugh images list, pick href and add it to link, visit new link, scrap for image url and title, append to a list
    hem_img_urls = []
    for image in images:
        img_link = f"{link}{image.find('a')['href']}"
        browser.visit(img_link)
        img_url = browser.find_by_xpath("//img[@class='wide-image']")._element.get_attribute("src")
        title = browser.find_by_xpath("//h2[@class='title']").text
        title = title.rstrip('Enhanced')
        hem_img_urls.append({"title" : title, "img_url" : img_url})
    hem_img_urls
    time.sleep(3)

    # DataBase dictionary
    mars_web_dict={
    'news_date': news_date, 'news_title': news_title, 'news_text': news_text,
    'featured_image_url': featured_image_url,
    'row1_title': table_data[0]['title'], 'row1_value': table_data[0]['value'],
    'row2_title': table_data[1]['title'], 'row2_value': table_data[1]['value'],
    'row3_title': table_data[2]['title'], 'row3_value': table_data[2]['value'], 
    'row4_title': table_data[3]['title'], 'row4_value': table_data[3]['value'], 
    'row5_title': table_data[4]['title'], 'row5_value': table_data[4]['value'], 
    'row6_title': table_data[5]['title'], 'row6_value': table_data[5]['value'], 
    'row7_title': table_data[6]['title'], 'row7_value': table_data[6]['value'], 
    'row8_title': table_data[7]['title'], 'row8_value': table_data[7]['value'], 
    'row9_title': table_data[8]['title'], 'row9_value': table_data[8]['value'],  
    'url1_title': hem_img_urls[0]['title'], 'url1_img': hem_img_urls[0]['img_url'],
    'url2_title': hem_img_urls[1]['title'], 'url2_img': hem_img_urls[1]['img_url'],
    'url3_title': hem_img_urls[2]['title'], 'url3_img': hem_img_urls[2]['img_url'],
    'url4_title': hem_img_urls[3]['title'], 'url4_img': hem_img_urls[3]['img_url']              
    }
    browser.quit()
    
    return mars_web_dict