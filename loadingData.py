import json

def firstTen(d, index):#Print first ten elements of input dictionary and the specified dictionary value
    topTen = {}
    for i, key in enumerate(d.keys()):#Iterate through dictionary via keys
        if i < 10:
            topTen[key] = d[key][index]#Assign key and specific data value in topTen dictionary
        else:
            break
    print(topTen)

def listProfanities(d):#Report profanity count and breakdown for data set. 
    totalProfanity = dict()
    for character in d:
        current = d[character][3]#Looking at the character's profanity data
        totalProfanity = {k: totalProfanity.get(k, 0) + current.get(k, 0) for k in set(totalProfanity) | set(current)}#Combine them all
    totalProfanity = dict(sorted(totalProfanity.items(), key=lambda item: item[1], reverse=True))#Sort in descending order
    print("This data set has a total profanity count of " + str(sum(totalProfanity.values())) + "\nHere are the top 10:")
    totalProfanity = {k: totalProfanity[k] for k in list(totalProfanity)[:10]}
    print(totalProfanity)

def wordInData(d, word):#Report breakdown of how many times a profanity was said. Total amount and who said it how many times
    print("\nBreakdown of " + word)
    count = 0
    characterAndCount = dict()
    for character in d:#For each character (key) in dictionary
        for profanity in d[character][3]:#For each profanity
            if(profanity == word):
                count += d[character][3][profanity]#Increment the total count of that profanity by seeing how many times the character we're on used it
                characterAndCount[character] = d[character][3][profanity]
                # print(character + " - " + str(d[character][3][profanity]))#Stan - x
    characterAndCount = dict(sorted(characterAndCount.items(), key=lambda item: item[1], reverse=True))#Sort in descending order
    print("The word " + word + " appears " + str(count) + " times in this data set")
    characterAndCount = {k: characterAndCount[k] for k in list(characterAndCount)[:10]}
    print(characterAndCount)



data = json.load(open("Seasons\\13\\12-The F Word.json"))#Series summary sorted by number of lines per character "Seasons\\26\\Summary.json" "Series\Summary.json"
print("\nTop 10 characters by number of lines")
firstTen(data, 0)#Get top 10 characters by line

dataByWords = dict(sorted(data.items(), key=lambda x: x[1][1], reverse=True))#Sort dictionary so character with most words is first
print("\nTop 10 characters by number of words")
firstTen(dataByWords, 1)#Get top 10 characters by words

dataByProfanityCount = dict(sorted(data.items(), key=lambda x: x[1][2], reverse=True))#Sort dictionary so character with most profanity count is first
print("\nTop 10 characters by profanity count")
firstTen(dataByProfanityCount, 2)#Get top 10 characters by profanity count

dataByProfanityFreq = dict(sorted(data.items(), key=lambda x: x[1][4], reverse=True))#Sort dictionary so character with highest profanity frequency is first
# print(dataByProfanityFreq['kyle'][0]*.05)
# print("------------------------------------------------------------------------")
delete = [key for key in dataByProfanityFreq if dataByProfanityFreq[key][0] < 10]#Create record of any characters that have less than 100 lines
for key in delete:
    del dataByProfanityFreq[key]#Delete those ones since it is not enough data
print("\nTop 10 characters by profanity frequency")
firstTen(dataByProfanityFreq, 4)#Get top 10 characters by profanity frequency

# name = 'craig'
# print('\n' + name + '\nLines: ' + str(data[name][0]) + '\nWords: '+ str(data[name][1]) + '\nP Count: ' + str(data[name][2]) + '\nP Freq: ' + str(data[name][4]))
# print({k: data[name][3][k] for k in list(data[name][3])[:10]})

print("\nTotal count of profanities and breakdown")
listProfanities(data)#Total profanities and breakdown of each one in this data set

wordInData(data, "fag")#How many times is a word mentinoed in this data set
