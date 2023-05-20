import os
import json

#MAYBE WE DONT NEED THIS

def modifyJSON():#Add all the data from each season summary into a series summary
    directory = "Seasons\\26"#Navigate to folder
    for filename in os.listdir(directory):#For each JSON in the directory
        file_path = os.path.join(directory, filename)#Get file path for reading/writing purposes
        if(filename.endswith(".json")):#If JSON file
            with open(file_path, "r") as f:
                data = json.load(f)
            modified_data = {}#Dictionary for modified data
            for key, values in data.items():#For k,v in dictionary
                modified_entry = {#Add identifiers
                    "Lines": values[0],
                    "Words": values[1],
                    "Profanity Count": values[2],
                    "Profanity List": values[3],
                    "Profanity Frequency": values[4]
                }
                modified_data[key] = modified_entry#Add the key value pair with modified value entry to the output dictionary
            with open(file_path, "w") as f:
                json.dump(modified_data, f)#Rewrite with modifications

modifyJSON()