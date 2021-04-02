import pandas as pd
from bs4 import BeautifulSoup
import glob
import os
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
max_subpages = 10
with open('keywords_search_all_languages.txt') as f:
    contents = re.sub('\s+', '', f.read())
    covid_words = re.findall(r'"([^"]*)"', contents)
    print(covid_words)


def wayback_machine_scraper(url):
    for month in range(1, 10):
        os.system("/Users/parnianshahkar/Downloads/miniconda3/bin/wayback-machine-scraper -f 20200" + str(month) +  "01 -t 20200" + str(month) + "01 " + url + " -c " + str(max_subpages))
    for month in range(10, 13):
        os.system("/Users/parnianshahkar/Downloads/miniconda3/bin/wayback-machine-scraper -f 2020" + str(month) +  "01 -t 2020" + str(month) + "01 " + url + " -c " + str(max_subpages))
    os.system("/Users/parnianshahkar/Downloads/miniconda3/bin/wayback-machine-scraper -f 20210101 -t 20210101 " + url + " -c " + str(max_subpages))
    os.system("/Users/parnianshahkar/Downloads/miniconda3/bin/wayback-machine-scraper -f 20210201 -t 20210201 " + url + " -c " + str(max_subpages))
    os.system("/Users/parnianshahkar/Downloads/miniconda3/bin/wayback-machine-scraper -f 20210301 -t 20210301 " + url + " -c " + str(max_subpages))


def link_finder(soup, date, url):
    links = []
    merged_list = soup.findAll('a') + soup.findAll('link')  # all hyperlinks in the body and head parts.
    combined_list = list(set(merged_list))
    # print(combined_list)
    for link in combined_list:
        if link.get('href') != None:
            if 'www.' in url:
                if '/web/' + str(date) + '/https://' + url in link.get('href') or '/web/' + str(
                        date) + '/http://' + url in link.get('href'):  # only website links
                    if any(word in link.get('href') for word in ['css', 'png', '.js', 'ico', 'digest']) == False:
                        pre_link = link.get('href').split('/web/', 1)[1]
                        if 'https://' in pre_link:
                            links.append(pre_link.split('https://', 1)[1]) 
                        if 'http://' in pre_link:
                            links.append(pre_link.split('http://', 1)[1])  

            else:
                if '/web/' + str(date) + '/https://www.' + url in link.get('href') or '/web/' + str(date) + '/http://www.' + url in link.get('href'):  # only website links
                    if any(word in link.get('href') for word in ['css', 'png', '.js', 'ico', 'digest']) == False:
                        pre_link = link.get('href').split('/web/', 1)[1]
                        if 'https://' in pre_link:
                            links.append(pre_link.split('https://', 1)[1]) 
                        if 'http://' in pre_link:
                            links.append(pre_link.split('http://', 1)[1]) 

    links = list(set(links)) ## remove duplicates 
    return links


def subpage_scraper(links):
    print(links)
    i = 0
    subpage_minilinks = ""
    links_copy = links
    # Priority is with subpages containing an information about coronavirus
    for link in links:
        if any(word in link for word in covid_words):
            i = i +1
            subpage_minilinks = subpage_minilinks + link + " "
            links_copy.remove(link)

    max_index = min(len(links_copy), max_subpages - i)
    for link in links_copy[:max_index]:
        subpage_minilinks = subpage_minilinks + link + " "
    wayback_machine_scraper(subpage_minilinks)


# Find snapshots of each url in desired dates: first of each month from Jan 2020 till now
df = pd.read_csv("jakob_companies.csv", delimiter = ';')
df = df.dropna()
company_urls = list(df.websiteaddress)
urls = ""
for url in company_urls:
    urls = urls + url + " "
wayback_machine_scraper(urls)


# Finding the subpages
files_and_directories = os.listdir(dir_path + "/website")
print(files_and_directories)
for url in files_and_directories:
    if url !='.DS_Store':
        print(url)
        snapshots = glob.glob(dir_path + "/website/" + url + "/*.snapshot")
        links = []
        for snapshot in snapshots:
            with open(snapshot, "rb") as fname:
                bytes_ = fname.read()
            date = int(snapshot[-23:-9])
            # print(url, date)
            soup = BeautifulSoup(bytes_)
            links = links + link_finder(soup, date, url)

        links = list(set(links))
        subpage_scraper(links)



##### Check if everything works properly
# os.system("/Users/parnianshahkar/Downloads/miniconda3/bin/wayback-machine-scraper -f " + str(date) +  " -t " + str(date) + " www.roche.com/partnering.htm")
# os.system("/Users/parnianshahkar/Downloads/miniconda3/bin/wayback-machine-scraper -f " + str(date) +  " -t " + str(date) + " www.roche.com/about.htm")
# os.system("/Users/parnianshahkar/Downloads/miniconda3/bin/wayback-machine-scraper -f " + str(date) +  " -t " + str(date) + " www.roche.com/research_and_development.htm")


