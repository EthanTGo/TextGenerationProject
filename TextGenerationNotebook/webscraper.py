import numpy as np
import pandas as pd
import requests 
from bs4 import BeautifulSoup, NavigableString, Tag
import matplotlib.pyplot as plt



'''
Input:

This is the function that will be called in order to extract the data from the website. 
For now, it will only get data for the grade 3, Kagero cards and use those data to create our training dataset
'''
def get_data_gr3():
    grade = 'Grade 3'
    file_output_path = 'grade3_kagero.txt
    URL = "https://cardfight.fandom.com/wiki/Kagero_(V_Series)"
    r = requests.get(URL) 

    # Creates the Beautiful Soup Object
    soup = BeautifulSoup(r.content, 'html5lib') 

    # Finding a h3 with the content of grade
    grade = soup.find_all("h3", string=grade)

    # We are going to store information here regarding cards links
    # The most important element is card_links[0] or the first element, we will further deprocess it
    card_links = []
    for header in grade:
        nextNode = header
        while True:
            nextNode = nextNode.nextSibling
            if nextNode is None:
                break
            if isinstance(nextNode, Tag):
                if nextNode.name == "h3":
                    break
                card_links.append(nextNode)

    #This will put each table row into an element
    cards = []
    for row in card_links[0].findAll('tr'):
        if type(row) != None:
            cards.append(row.find('td'))

    # retrieve the a tag link which can be used to access each individual card pages
    cards_a_attr = []
    for link in cards:
        if link != None:
            cards_a_attr.append(link.find('a', href=True)['href'])

    base_url = 'https://cardfight.fandom.com'

    # In order to access each page, we need to append it with the base url
    full_link = []
    for i in cards_a_attr:  
        full_link.append(base_url + i)
    
    # Th document we will write
    document_grade = ''
    for link in full_link:
        r = requests.get(link)
        soup = BeautifulSoup(r.content,'html5lib')
        # An error handling to make sure the process keeps running even if no attributes are found
        try:
            soup.find('table', attrs = {'class':'effect'}).findAll('td')
            items = soup.find('table', attrs = {'class':'effect'}).findAll('td')
            for item in items:
                document_grade = document_grade + item.text
        except:
            print('A none appeared')
    
    text_file = open(file_output_path, "wt")
    n = text_file.write(document)
    text_file.close()

get_data_gr3()
