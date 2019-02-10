# Made by Parser Pals Inc.

import indicoio
from googlesearch import search
from progress.bar import ShadyBar # Get rid of if need be

indicoio.config.api_key = '60b7c73721680f219f9119ab83148b3a'

#examples, replace with a hook into spotify result tuples once in Flask
# Tuple Structure: [("<Song Name>", "<Artist Name>", "<Album Name>", <Popularity Score>)]

songDetails = [("Come Along", "Cosmo Sheldrake", "The Much Much How How and I", 18), 
               ("BOOGIE", "BROCKHAMPTON", "SATURATION III", 90), 
               ("Holland, 1945", "Neutral Milk Hotel", "In the Aeroplane Over the Sea", 19),
               ("Nocturnes, Op. 9: No. 2 in E-Flat Major. Andante", "Brigitte Engerer", "Chopin: The Essentials", 65)]



def songScore(sentiments, popularity, searchNum):
    #print(len(sentiments))
    score = (sum(sentiments)/searchNum)
    if popularity > 85:
        if score > 0.2:
            score -= 0.2
        else:
            score = 0
    if popularity < 20:
        if score < 0.75:
            score += 0.25
        else:
            score = 1
    return score

# comedy gold naming
def songcatenate(songTuple):
    if len(" ".join([songTuple[0], songTuple[1], songTuple[2]])) > 70:
        if len(" ".join([songTuple[0], songTuple[1]])) > 50:
            return songTuple[0]
        return (" ".join([songTuple[0], songTuple[1]]))
    return (" ".join([songTuple[0], songTuple[1], songTuple[2]]))

def libraryScore(songList):
    """ """
    # This holds everything
    tempUrls = []

    # SEARCH_NUM changes to fit the number of songs inputted, to avoid overwhelming Indico
    SEARCH_NUM = 10
    if len(songList) > 100:
        SEARCH_NUM = 1
    elif len(songList) > 50:
        SEARCH_NUM = 2
    elif len(songList) > 30:
        SEARCH_NUM = 3
    elif len(songList) > 20:
        SEARCH_NUM = 5



    #TODO delete bar and bar references when adding to Flask, unless it just exists in console
    bar = ShadyBar("Google Searching...", max = len(songList), suffix = '%(percent).1f%% - %(eta)ds')

    # Google API can only search for URLS in increments of 10, so SEARCH_NUM limits the amount
    for i in range(len(songList)):
        #print(songcatenate(songList[i]))
        for url in search(songcatenate(songList[i]) + ' review', num = SEARCH_NUM, stop=SEARCH_NUM):
            tempUrls += [url]
        bar.next()
    bar.finish()

    #print(tempUrls)

    # exchange sentiment_hq with sentiment if calculation takes too long
    sentiment = indicoio.sentiment(tempUrls, url=True)

    #print(sentiment)

    scores = []

    # Extracts the proper range of sentiments from the crazy big list
    for i in range(len(songList)):
        i_range = sentiment[(i*SEARCH_NUM):(i*SEARCH_NUM)+(SEARCH_NUM)]
        scores += [(songList[i], songScore(i_range, songList[i][3], SEARCH_NUM))]

    # Return Structure: [(("<Song Name>", "<Artist Name>", "<Album Name>", <Popularity Score>), <Final Song Score>)]
    return(scores)

#print(libraryScore(songDetails))
