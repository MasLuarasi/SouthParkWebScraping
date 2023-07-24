import os
import glob
import json
import csv

profanityHeatmap = [[f"" for j in range(1, 21)] for i in range(1, 27)]#Make the csv with dimensions for alloted seasons and episodes
with open("Profanity Heatmap.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(profanityHeatmap)

for index in range(1, 27):
    filePath = os.path.join('Seasons', str(index))#'Seasons\1...
    if os.path.exists(filePath):
        epFiles = glob.glob(os.path.join(filePath, '*.json'))#Gather all the json files
        epFiles = [f for f in epFiles if not f.endswith('Summary.json')]#Ignore the Summary.json at the end
        for ep in epFiles:#For each episode in this season
            profanitySum = 0
            epNum = int(ep[ep.rfind('\\')+1 : ep.find('-')])#Episode number is between last '\' and the only '-'
            with open(ep, 'r') as file:
                data = json.load(file)#Load dictionary into data
                for k in data:#For each character
                    profanitySum += data[k][2]#Increment profanitySum by the number of profanities current character has in episode

                with open("Profanity Heatmap.csv", "r", newline="") as file:
                    reader = csv.reader(file)
                    rows = list(reader)  # Read all rows from the CSV file

                rows[index-1][epNum-1] = profanitySum  # Update the specified cell

                with open("Profanity Heatmap.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)  # Write all rows back to the CSV file




#     first_key = next(iter(data))
#     first_value = data[first_key]
