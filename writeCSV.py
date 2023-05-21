import csv
import json
import os

for index in range(1,27):#Seasons 1-26
    directory = "Seasons\\" + str(index) + "\\"#Navigate to folder
    for filename in os.listdir(directory):#For each JSON in the directory
        file_path = os.path.join(directory, filename)#Get file path for reading/writing purposes
        if(filename.endswith(".json")):#If JSON file
            with open(directory + filename, "r") as f:
                data = json.load(f)#Load data of json file for this episode
            csv_data = []
            for entry_name, entry_values in data.items():#Organizing to csv
                name = entry_name
                lines, words, profanityCount, profanityList, profanityFrequency = entry_values
                csv_data.append([name, lines, words, profanityCount, profanityList, profanityFrequency])

            csv_file = filename[:-5] + ".csv"
            with open(directory + csv_file, "w", newline="") as file:#Writing to csv
                writer = csv.writer(file)
                writer.writerow(["Name", "Lines", "Words", "Profanity Count", "Profanity List", "Profanity Frequency"])
                writer.writerows(csv_data) 

# Use this for getting the name of the episode/file and assign it to the csv file
# for filename in os.listdir(directory):#For each JSON in the directory
# file_path = os.path.join(directory, filename)#Get file path for reading/writing purposes
# Looping through all the seasons



# with open("Seasons\\26\\1-Cupid Ye.json", "r") as f:
#     data = json.load(f)

# csv_data = []

# for entry_name, entry_values in data.items():
#     name = entry_name
#     lines, words, profanityCount, profanityList, profanityFrequency = entry_values
#     csv_data.append([name, lines, words, profanityCount, profanityList, profanityFrequency])

# csv_file = "output.csv"
# with open(csv_file, "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Name", "Lines", "Words", "Profanity Count", "Profanity List", "Profanity Frequency"])
#     writer.writerows(csv_data) 
