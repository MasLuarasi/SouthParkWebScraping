import json

json_file_path = "Movie\Test.json"

with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

for entry in data:
    name = entry[0]
    values = entry[1]
    modified_data = [name, {
        "Lines": values[0],
        "Words": values[1],
        "Profanity Count": values[2],
        "Profanity List": values[3],
        "Profanity Frequency": values[4]
    }]
    data[data.index(entry)] = modified_data

with open(json_file_path, "w") as json_file:
    json.dump(data, json_file)