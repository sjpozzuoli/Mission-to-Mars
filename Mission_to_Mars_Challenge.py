#!/usr/bin/env python
# coding: utf-8

# In[4]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[5]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[6]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[7]:


slide_elem.find('div', class_='content_title')


# In[8]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[9]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[10]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[14]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[15]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[16]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[13]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[14]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the html with soup
html = browser.html
image_soup = soup(html, 'html.parser')

# Find the number of pictures to scan
image_count = len(image_soup.select('div.item'))

# for loop over each picture
for i in range(image_count):
    # Create an empty dict to hold the search results
    hemispheres = {}
    
    # Get link to picture
    image_link = image_soup.select('div.description a')[i].get('href')
    browser.visit(f'https://marshemispheres.com/{image_link}')
    
    # Parse the new html page
    html = browser.html
    moon_image_soup = soup(html, 'html.parser')
    
    # Get the full image link
    image_url = moon_image_soup.select_one("div.downloads ul li a").get('href')
    
    # Get the full image title
    image_title = moon_image_soup.select_one("h2.title").get_text()
    
    # Add results to hemipsheres dictionary
    hemispheres = {
        'img_url': url + image_url,
        'title': image_title}
    
    # Append results dict to hemisphere image urls list
    hemisphere_image_urls.append(hemispheres)
    
    # Return to main page
    browser.back()


# In[15]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[16]:


# 5. Quit the browser
browser.quit()


# In[ ]:




