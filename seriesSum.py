import os
import json
from collections import Counter
import json
import operator


def computeSeriesSummary():#Add all the data from each episode in the season
    directory = 'Series/'
    seriesSummary = dict()
    for filename in os.listdir(directory):
        current =  json.load(open(os.path.join(directory, filename)))#Get the data of current episode
        for c in current:#For each key
            if(c in seriesSummary.keys()):#If character already has an entry in the dictionary, so if they were in one of previous episodes
                for j in range(0,3):
                    seriesSummary[c][j] += current[c][j]#Update lines, words, and profanity count
                seriesSummary[c][4] = round(seriesSummary[c][2]/seriesSummary[c][1] * 100, 2)#Update the profanity % with updated words and profanity count data
                seriesSummary[c][3] = dict(sorted((Counter(seriesSummary[c][3]) + Counter(current[c][3])).items(), key=operator.itemgetter(1), reverse=True))#Merge the profanity frequency dictionaries and sort in descending order 
            else:
                seriesSummary[c] = current[c]#Make a new entry

    seriesSummary = dict(sorted(seriesSummary.items(), key=lambda x: x[1][0], reverse=True))#Sort dictionary so character with most lines is first

    with open('Series/Summary.json', 'w') as f:
        f.write(json.dumps(seriesSummary))#Create the season summary json file with the contents in the dictionary
    f.close()

computeSeriesSummary()

# # Path to the directory containing the JSON files
# path_to_files = 'Series/'

# # Create an empty dictionary to store the merged contents
# merged_data = {}

# # Loop through each file in the directory
# for filename in os.listdir(path_to_files):
#     if filename.endswith('.json'):  # Only consider JSON files
#         # Open the file and load its contents as a dictionary
#         with open(os.path.join(path_to_files, filename)) as f:
#             file_data = json.load(f)
#         # Merge the file's contents into the main dictionary
#         merged_data.update(file_data)

# # Save the merged contents to a new JSON file
# with open('Series/Summary.json', 'w') as f:
#     json.dump(merged_data, f)
