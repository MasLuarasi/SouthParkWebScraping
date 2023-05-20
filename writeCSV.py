import csv
import json


with open("Seasons\\26\\1-Cupid Ye.json", "r") as f:
    data = json.load(f)

csv_data = []

for entry_name, entry_values in data.items():
    name = entry_name
    lines, words, profanityCount, profanityList, profanityFrequency = entry_values
    csv_data.append([name, lines, words, profanityCount, profanityList, profanityFrequency])

csv_file = "output.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Lines", "Words", "Profanity Count", "Profanity List", "Profanity Frequency"])
    writer.writerows(csv_data) 

# Use this for getting the name of the episode/file and assign it to the csv file
# for filename in os.listdir(directory):#For each JSON in the directory
# file_path = os.path.join(directory, filename)#Get file path for reading/writing purposes
# Looping through all the seasons
