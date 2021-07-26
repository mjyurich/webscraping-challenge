#import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup 
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    #set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_info = {}

def scrape_info():

    browser = init_browser()

#Start by visiting the mars news url

    #Visit the Mars url
    news_url = "http://redplanetscience.com/"
    browser.visit(news_url)

    #Create an HTML object
    html = browser.html

    #Use beautiful soup to make data look nicer
    news_soup = BeautifulSoup(html, "html.parser")
    

    #Pull the first news title and its paragraph
    result = news_soup.select_one('div.list_text')
    news_title = result.find('div', class_='content_title').get_text()
    news_p = result.find('div', class_='article_teaser_body').get_text()

    mars_info["news_title"] = news_title
    mars_info["news_paragraph"] = news_paragraph

# Visit the next website to obtain image

    #Visit the image website
    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Use beautiful soup to parse data
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    #Find the current image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    mars_info["featured_image_url"] = img_url_rel

#Visit the Mars Facts URL

    #Visit the mars facts website
    mars_url = 'https://galaxyfacts-mars.com/'
    browser.visit(mars_url)

    #Create a table with the data
    mars_facts = pd.read_html(mars_url)[0]
    mars_facts.columns=['Description', 'Mars', 'Earth']
    mars_facts.set_index('Description')

    #Convert dataframe into html format
    mars_facts.to_html("mars_table.html")
    
    mars_info["mars_facts"] = mars_facts

#visit the info on mars hemispheres
    
    #link to hemisphere url
    hemi_url = 'https://marshemispheres.com/'
    browser.visit(hemi_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemi_data = soup.find_all('div', class_='item')

    hemisphere_img = []

    for data in range(len(hemi_data)):
        
        hemi_button = browser. find_by_css("a.product-item img")[data].click()
            
                
        html = browser.html
        hemi_soup = BeautifulSoup(html, 'html.parser')
                            
        hemi_img = hemi_soup.find('img', class_='wide-image')['src']
                                    
        img_title = browser.find_by_css('.title').text
                                            
        hemisphere_img.append({"title": img_title,
                            "img_url": hemi_img})
                                                    
        mars_info["hemispheres_info"] = hemisphere_img

    browser.quit()

    return mars_info

if __name__ == "__name__":
    print(mars_info)
