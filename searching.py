import os
import glob
import json


for sNum in range(26, 27):
    filePath = os.path.join('Seasons', str(sNum))
    if os.path.exists(filePath):
        epFiles = glob.glob(os.path.join(filePath, '*.json'))
        epFiles = [f for f in epFiles if not f.endswith('Summary.json')]
        for ep in epFiles:
            profanitySum = 0
            epNum = ep[ep.index('-')-1]
            with open(ep, 'r') as file:
                data = json.load(file)
                for k in data:                    
                    profanitySum += data[k][2]
                print(str(epNum) + ' - ' + str(profanitySum))





#     first_key = next(iter(data))
#     first_value = data[first_key]
