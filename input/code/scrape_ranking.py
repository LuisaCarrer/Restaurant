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


# Function that gets the years
def get_years():
    years = [i for i in range(2003,2019)]
    return years

# Function to construct the URL for the ranking
def build_url_ranking(year):
    if year <= 2008 or 2011 <= year < 2018:
        url = "https://www.theworlds50best.com/list/past-lists/" + str(year)
    if 2009 <= year <= 2010 :
        url = "https://www.theworlds50best.com/list/past-list/" + str(year)
    if year == 2018:
        url = "https://www.theworlds50best.com/list/1-50-winners#t1-50"
    return url

def clean_string(s):
   s = s.upper()
   s = s.replace("’","'")
   s = s.replace("-"," ")
   return ''.join(c for c in unicodedata.normalize('NFKD', s)
                  if unicodedata.category(c) != 'Mn')

def clean_string_restaurant(s):
    if s == "ALAIN DUCASSE AU PLAZA":
        s = s.replace("ALAIN DUCASSE AU PLAZA","ALAIN DUCASSE AU PLAZA ATHENEE")
    if s == "ARPEGE":
        s = s.replace("ARPEGE", "L'ARPEGE")
    if s == "L'APEGE":
        s = s.replace("L'APEGE", "L'ARPEGE")

    return(s)

def clean_countries(s):
    s = s.strip()
    if s == "Denamrk":
        s = s.replace("Denamrk" , "Denmark")
    if s == "Neitherlands":
        s = s.replace("Neitherlands" , "Netherlands")
    if s == "New York - USA":
        s = s.replace("New York - USA" , "USA")
    if s == "UK":
        s = s.replace("UK" , "United Kingdom")
    if s == "England":
        s = s.replace("England" , "United Kingdom")
    if s == "USA":
        s = s.replace("USA" , "United States")
    if s == "UAE":
        s = s.replace("UAE" , "United Arab Emirates")
    if s == "The Test Kitchen":
        s = s.replace("The Test Kitchen" , "South Africa")
    return(s)


# Scrape yearly ranking of restaurants and locations data
def scrape_restaurant(url, year):

    html = requests.get(url)
    soup = bs(html.text, "lxml")

    # get for each year(different webpage) the relevant string info
    restaurant = [i.text.strip() for i in soup.find_all('h2')]
    if year == 2018:
        restaurant = restaurant[1:]
    restaurant_ascii = [clean_string(i) for i in restaurant]
    restaurant_ascii = [clean_string_restaurant(i) for i in restaurant_ascii]
    location = [i.text.strip() for i in soup.find_all('h3')]


   # sometimes they provide both city and country, other only the latter
   # clean this
    string_length = 0
    for i in range(len(location)):
        if len(location[i].split(","))==1:
            string_length =  string_length + 1
            print(location[i],year,restaurant[i])
            location[i] = location[i]+", "+location[i]

    # split info into city and country
    city = [i.split(",")[0] for i in location]
    country = [i.split(",")[1] for i in location]
    country = [clean_countries(i) for i in country]

    #construct dataframe
    data = pd.DataFrame({"restaurant" : restaurant,
                           "city" : city,
                           "country" : country,
                           "cleaned_restaurant" : restaurant_ascii})
    # create ranking and year columns
    data['ranking'] = data.index +1
    data['year'] = year


    return(data)

def get_ranking():
    restaurant_ranking = pd.DataFrame()
    years = get_years()
    for year in years:
        url = build_url_ranking(year)
        data = scrape_restaurant(url, year)
        restaurant_ranking = restaurant_ranking.append(data)
    return(restaurant_ranking)




if __name__ == "__main__":

     # Set directory
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    print("The path is " + path)
    os.chdir(path[:-4])
    newpath = os.getcwd()
    restaurant_ranking = get_ranking()

    restaurant_unique = numpy.unique(restaurant_ranking['cleaned_restaurant'])
    restaurant_unique = restaurant_unique.tolist()

    matches = []
    for i in range(len(restaurant_ranking['restaurant'].tolist())):
        match = difflib.get_close_matches(restaurant_ranking['cleaned_restaurant'].tolist()[i],restaurant_unique, cutoff = 0.8)
        matches.append(match)

    restaurant_ranking['matches'] = matches
    
    newpath = newpath + "/raw_data/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    restaurant_ranking.to_csv(newpath+"restaurant_ranking.csv")


