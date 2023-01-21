import requests
from bs4 import BeautifulSoup
import os

#from pyhtml2pdf import converter

web_link_path = 'web_link.txt'
datadir_path = 'data'

# extract web information by 
# 1. convert webpage to PDF
# 2. read texts from PDF
'''
# parse text file with urls and convert them into PDF files
with open(web_link_path) as web_link:
    
    links = web_link.readlines() # list containing lines of file

    for i, link in enumerate(links):
        print(f'Converting to PDF: {link}')
        # create a file containing texts from the link        
        pdf_path = os.path.join(datadir_path, 'weblink_' + str(i) + '.pdf')
        converter.convert(link, pdf_path)
'''



# parse text file with urls and convert them into PDF files
with open(web_link_path) as web_link:
    links = web_link.readlines() # list containing lines of file

    for i, link in enumerate(links):
        print(link)
        # extract texts from web url
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        #text = soup.get_text()
        #print(text)


        results = soup.find_all("p", class_="")
        texts = []
        for result in results:
            print(result.text)
            texts.append(result.text)
        print(' '.join(texts))
        # create a file containing texts from the link        
        #page_path = os.path.join(datadir_path, 'weblink_' + str(i) + '.txt')
        #with open(page_path, 'w') as f:
        #    f.write(' '.join(texts))

