import os
import glob
import json
import csv
from natsort import natsorted
from operator import itemgetter

with open("Heatmaps\Rating Heatmap.csv", "r", newline="") as file:
    reader = csv.reader(file)
    rows = list(reader)  # Read all rows from the CSV file

characters = {
            'cartman' : [5, 'Eric Cartman'], 'kenny' : [5, 'Kenny McCormick'], 'kyle' : [5, 'Kyle Broflovski'], 'stan' : [5, 'Stan Marsh'],
            'butters' : [5, 'Butters Stotch'], 'wendy' : [1, 'Wendy Testaburger'], 'jimmy' : [1, 'Jimmy Valmer'], 'timmy' : [1, 'Timmy'],
            'craig' : [1, 'Craig Tucker'], 'tweek' : [1, 'Tweek Tweak'], 'tolkien' : [1, 'Tolkein Black'], 'clyde' : [1, 'Clyde Donovan'],
            'ike' : [1, 'Ike Broflovski'], 'heidi' : [1, 'Heidi Turner'], 'scott' : [1, 'Scott Malkinson'], 'shelly' : [1, 'Shelly Marsh'],
            'randy' : [5, 'Randy Marsh'], 'sharon' : [1, 'Sharon Marsh'], 'gerald' : [1, 'Gerald Broflovski'], 'sheila' : [1, 'Sheila Broflovski'],
            'carol' : [1, 'Carol McCormick'], 'stuart' : [1, 'Stuart McCormick'], 'stephen' : [1, 'Stephen Stotch'], 'liane' : [1, 'Liane Cartman'],
            'mr garrison' : [1, 'Mr Garrison'], 'chef' : [1, 'Chef'], 'mr mackey' : [1, 'Mr Mackey'],  
            'principal victoria' : [1, 'Principal Victoria'], 'pc principal' : [1, 'PC Principal'], 'jesus' : [1, 'Jesus Christ'], 'satan' : [1, 'Satan'],
            'santa' : [1, 'Santa'], 'mr hankey' : [1, 'Mr Hankey'], 'mayor mcdaniels' : [1, 'Mayor McDaniels'], 'officer barbrady' : [1, 'Officer Barbrady'],
            'yates' : [1, 'Detective Yates'], 'priest maxi' : [1, 'Father Maxi'], 'jimbo' : [1, 'Jimbo'], 'mr slave' : [1, 'Mr Slave'],
            'towelie' : [1, 'Towelie'], 'doctor' : [1, 'Doctor']
            }

for c in characters:
    characterAppearances = 0
    characterTopEpisodes = {}
    characterProfanity = {}
    characterSeasonProgression = {}
    for index in range(1, 27):
        filePath = os.path.join('Seasons', str(index))#'Seasons\1...
        if os.path.exists(filePath):
            epFiles = natsorted(glob.glob(os.path.join(filePath, '*.json')))#Gather all the json files
            # epFiles = [f for f in epFiles if not f.endswith('Summary.json')]#Ignore the Summary.json at the end
            for ep in epFiles:#For each episode in this season
                profanitySum = 0
                if not ep.endswith('Summary.json'):#If it's an episode
                    epNum = int(ep[ep.rfind('\\')+1 : ep.find('-')])#Episode number is between last '\' and the only '-'
                    with open(ep, 'r') as file:
                        epData = json.load(file)#Load data
                        epName = file.name[file.name.find('-') + 1: -5]#Extract the episode name
                        try:
                            characterData = epData[c]#If our character appears in this episode, assign the values, then we can do more
                            if(characterData[0] > characters[c][0]):#If they have more than n lines. (Baseline for an appearance. Can change depending on character)
                                characterAppearances += 1
                            characterTopEpisodes[epName] = characterData[0], rows[index][epNum-1]#Add episode and # of lines to dictionary and episode rating                
                        except:
                            continue
                else:#If it's the season summary
                    with open(ep, 'r') as file:
                        seasonData = json.load(file)#Load data
                        try:
                            characterData = seasonData[c]#If our character appears in this season
                            characterSeasonProgression[index] = characterData[0], characterData[2], characterData[4]#Add lines, profanityCount, and profanity% to dictionary                
                        except:
                            characterSeasonProgression[index] = 0,0,0#They do not appear in this season, enter 0s into data to fill

    with open('Series\Summary.json', 'r') as file:
        seriesData = json.load(file)
    characterData = seriesData[c]#Get our character from the series data
    characterProfanity = characterData[3]#Get the profanity list for that character
    characterProfanity = list(characterProfanity.items())[:10]#Take the first five

    characterTopEpisodes = dict(sorted(characterTopEpisodes.items(), key=itemgetter(1), reverse=True))#Sort episodes in descending order by lines
    characterTopEpisodes = list(characterTopEpisodes.items())[:10]#Take the first five

    with open('Characters\\' + characters[c][1] + '.csv', 'w') as file:#Writing all the data to the corresponding csv file
        file.write(characters[c][1])
        file.write('\n'*2)
        file.write('Appearanes,')
        file.write(str(characterAppearances))
        file.write('\n'*2)
        file.write('Top Episodes')
        file.write('\n')
        file.write('Episode,')
        file.write('Lines,')
        file.write('Rating')
        file.write('\n')
        for e in characterTopEpisodes:
            file.write(e[0] + ',')
            file.write(str(e[1][0]) + ',')
            file.write((e[1][1]))
            file.write('\n')
        file.write('Average')
        file.write('\n'*2)
        file.write('Top Profanities')
        file.write('\n')
        file.write('Profanity,')
        file.write('Count')
        file.write('\n')
        for p in characterProfanity:
            file.write(p[0] + ',')
            file.write(str(p[1]))
            file.write('\n')
        file.write('\n')
        file.write('Season Progression')
        file.write('\n')
        file.write('Season,')
        file.write('Lines,')
        file.write('Profanity Count,')
        file.write('Profanity Frequency')
        file.write('\n')
        for s in characterSeasonProgression:
            file.write(str(s) + ',')
            file.write(str(characterSeasonProgression[s][0]) + ',')
            file.write(str(characterSeasonProgression[s][1]) + ',')
            file.write(str(characterSeasonProgression[s][2]) + ',')
            file.write('\n')