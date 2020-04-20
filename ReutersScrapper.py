
# coding: utf-8

# In[1]:


import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import numpy as np
import pandas as pd
import time



#print(html)


# In[80]:


chromedriver = "F:\chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get("https://in.reuters.com/search/")
elem = driver.find_element_by_id('newsSearchField')
elem.send_keys('Article 370')
elem.send_keys(u'\ue007')

elm=driver.find_element_by_class_name('search-result-more-txt')

while True:
    elm = driver.find_element_by_class_name('search-result-more-txt')
    if 'search-result-more-txt search-result-no-more' in elm.get_attribute('class'):
        break;
    elm.click()
    
time.sleep(2)    
print(driver.current_url)
#url=driver.current_url+'/all'
url=driver.current_url

r1 = requests.get(url)
html = driver.page_source
#print(html)
coverpage = html

soup1 = BeautifulSoup(coverpage, 'html5lib')

coverpage_news = soup1.find_all('h3', class_='search-result-title')
number_of_articles=len(coverpage_news)
print(number_of_articles)

#int(coverpage_news)

#type(coverpage_news)

#number_of_articles = 5

news_contents = []
list_links = []
list_titles = []

for n in np.arange(0, number_of_articles):
    
    link = coverpage_news[n].find('a')['href']
    title = coverpage_news[n].find('a').get_text()
    list_titles.append(title)

    link = coverpage_news[n].find('a')['href']
    link="https://in.reuters.com/" + link
    list_links.append(link)

    article = requests.get(link)
    article_content = article.content

    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='StandardArticleBody_body')
    x = body[0].find_all('p')

    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
        
    news_contents.append(final_article)
    print(title)


# In[81]:


# df_features
df_features = pd.DataFrame(
     {'Article Content': news_contents 
    })

# df_show_info
df_show_info = pd.DataFrame(
    {'Article Title': list_titles,
     'Article Link': list_links,
    'Article Content': news_contents})


# In[82]:


df_features


# In[83]:


df_show_info



# In[79]:
print("end")

df_show_info.to_csv(r'I:\News_.csv', index=False) 

