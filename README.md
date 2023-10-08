# SouthParkWebScraping
episodeLinks.py gets the link to the script for each episode by going through the site. The link for the first episode is provided, the script opens that page, looks for the link to the next episode in the 'next' tab.
This process goes on until we have the url for each episode. I manually divided the links into the respective season folders.

The main.py contains the script for the main data collection. It goes through the links for each episode in each season and analyzes the dialogue for each episode. The raw data is then organized and divided accprdingly.
Please see comments in the code for a more in depth explanation. NOTE: I did the bulk work of this project prior to learning Pandas.

loadingData.py was code I wrote that is generally irrelevant now. The main purpose is about printing more niche data. There I was experimenting because I was curious about more unique data.

keyMerging.py goes through every JSON generate (episode, season, summary). It's purpose is to combine certain keys (characters) because I believe they should not be counted as two different people. The different names
per character are laid out in the file to see. In the online script, the first use of that character is with the full name, after that they go by their more common name. Eric Cartman becomes Cartman but they are the
same character so it makes sense to combine their data. Another instance is an alias. There have been a few episodes where the boys play as superheroes and in the script they are referred to as their aliases. Butters
and Professor Chaos are the same person. Another situation is typos. I mentioned the several formatting errors on the sites end, but forgot to talk about this. Yates and Yatess for instance.

The Characters sub folder has the character profiles for a few dozen characters in csv format. The data there includes total appearances, at most 10 prominent episodes (which episodes do they have the most lines in),
and the rating for those episodes. In one of the data visualizations, I put the character name and average rating when prominent to see if a character makes episodes better or worse. The profiles also has the top 10
profoanities throughout the entire series and the count. At the bottom, I track the count for their lines, words, profanities, and profanity frequency each episode. Frequency is profanity count/words.

The Visuals folder contains the data graphics.The Character Ratings file has the data I previously mentioned with the avg rating of a characters prominent episode. The graph at the bottom displays the top and bottom 5
characters with their rating. The main character file shows who is the main character for each episode. Season number is represented in row number, season 1 starting on row 2. The episode number corresponds with the 
column, A is 1. I am mainly focussing on 7 characters. Any instance where someone else is a main character, they are categorized under 'other'. Below the series data and the graph for it, I divided the seasons into
different eras based on an in depth posting about it I came across. I do not recall the exact reasons the author used in their arguments for each era, but I agreed with their points for the most part and wanted to 
see how my data compared in the different eras. After all the era divisions, I compiled the data to track the progression of main characters against the different eras. The rating profanity file displays data in the 
same way the main character data does. The first dataset is with the ratings for each episode, and the second with the profanity count in each episode. I included overall season data (avg episode rating, and avg
profanity count per episode). The graph at the bottom compares the two against each other, and we see that generally less profanity results in better quality. The last file does a similar task, but as opposed to 
avg throughout the season, the data is with each individual episode.
