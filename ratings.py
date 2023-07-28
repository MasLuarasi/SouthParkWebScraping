from bs4 import BeautifulSoup
import requests

# url = 'https://www.imdb.com/title/tt0394893/?ref_=tt_ep_pr'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# print(soup)
# element = soup.find('div', class_='sc-e226b0e3-3 jJsEuz')
# print(element)

# while True:
#     time.sleep(3)
#     with urlopen(starterLink) as url:
#         soup = BeautifulSoup(url, "lxml")
#     element = soup.find(_class="sc-bde20123-1 iZlgcd")

#     try:
#         link = "https://southpark.fandom.com" + headerElement[len(headerElement)-2].find('a').get('href')#Get the link to script of next episode if it exists
#         episodeLinks.append(link)#Add to list so we can go through that in our next iteration
#         with open('Episode_Links.txt', 'a') as convert_file:
#             convert_file.write(json.dumps(link) + "\n")#Write to file
#     except:
#         print("Done")#No more episodes to get

