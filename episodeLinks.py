from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import time

episodeLinks = ["https://southpark.fandom.com/wiki/Cartman_Gets_an_Anal_Probe/Script"]

for episode in episodeLinks:
    time.sleep(3)
    with urlopen(episode) as url:
        soup = BeautifulSoup(url, "lxml")
    headerElement = soup.find("tbody").find_all("td")

    try:
        link = "https://southpark.fandom.com" + headerElement[len(headerElement)-2].find('a').get('href')#Get the link to script of next episode if it exists
        episodeLinks.append(link)#Add to list so we can go through that in our next iteration
        with open('Episode_Links.txt', 'a') as convert_file:
            convert_file.write(json.dumps(link) + "\n")#Write to file
    except:
        print("Done")#No more episodes to get