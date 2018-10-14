#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:00:42 2018

@author: luisa
"""
import sys
import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import difflib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import unicodedata
import numpy
import zipfile


# Driver
def open_driver():
    path = '/anaconda3/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : '/input/raw_data'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path = path,chrome_options=chrome_options)
    print('Chrome driver is good to go!')
    return driver
   


def scrape_tourism():
    driver = open_driver()    
    url = "http://api.worldbank.org/v2/en/indicator/ST.INT.ARVL?downloadformat=csv"
    driver.get(url)
    zf = zipfile.ZipFile('input/raw_data/API_ST.INT.ARVL_DS2_en_csv_v2_10139871.zip')      
    return(zf)




if __name__ == "__main__":
    
    # Set directory
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    print(path)
    os.chdir(path[:-6])
    
    
    tourism = scrape_tourism()
    tourism.to_cvs('raw_data/tourism.csv')




'''
<a href="http://api.worldbank.org/v2/en/indicator/ST.INT.ARVL?downloadformat=csv" data-customlink="fd:right rail:en:csv" data-text="CSV" data-reactid="298">CSV</a>


for i in range(len(restaurant_ranking['restaurant'].tolist())):
    matches = difflib.get_close_matches(restaurant_ranking['restaurant'].tolist()[i],restaurant_unique)
    restaurant_ranking.add(matches)


for i in range(len(restaurant_ranking['restaurant'].tolist())):
    matches = difflib.get_close_matches(restaurant_ranking['restaurant'].tolist()[i],restaurant_ranking['restaurant'].tolist())
    print(i,matches)
'''
#

'''
  

  os.getcwd    
dir = os.getcwd()
data.to_csv(dir + "/restaurant_" + str(year) + ".csv")    




'''