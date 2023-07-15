import tkinter
import math
import ssl
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
import json

# for this file to work you need to have the modulesForOauth
# folder in your working directory. A zip file containing the
# modulesForOauth is here:
# http://www.cs.uiowa.edu/~cremer/courses/cs1210/hw/hw11/modulesForOauth.zip

import sys
sys.path.insert(0,'./modulesForOauth')
import requests
from requests_oauthlib import OAuth1
import json
from urllib.parse import quote_plus
import webbrowser

# 
# The code in this file won't work until you set up your Twitter "app"
# at https://dev.twitter.com/apps
# After you set up the app, copy the four long messy strings and put them here.
#

API_KEY = "c3pbJ5YkSzaXqVCPZn31iNCGb"
API_SECRET = "VJDI72KQ9pcHio9OSF2C1OSuCautNAhqxIpSd9suYZ1oFj5k5t"
ACCESS_TOKEN = "1336049491472998402-NiRQViuJcTyUlTVGCgYzElV1v9QOgX"
ACCESS_TOKEN_SECRET = "JG38InOwjkfR3T1ShYTvPi51ArZQGqtmdSa8Osh3OD0ql"
 
# Call this function after starting Python.  It creates a Twitter client object (in variable client)
# that is authorized (based on your account credentials and the keys above) to talk
# to the Twitter API. You won't be able to use the other functions in this file until you've
# called authTwitter()
#
def authTwitter():
    global client
    client = OAuth1(API_KEY, API_SECRET,
                    ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Study the documentation at 
# https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
# to learn about construction Twitter queries and at
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
# the understand the structure of the JSON results returned for search queries
#

# Try:
#      tweets = searchTwitter("finals")
#
# Iowa City's lat/lng is [41.6611277, -91.5301683] so also try:
#      tweets = searchTwitter("finals", latlngcenter=[41.6611277, -91.5301683])
#
# To find tweets with location, it's often helpful to search in big cities.
#      E.g. lat/long for Times Square in NYC is (40.758895, -73.985131)
#      tweets = searchTwitter("party", latlngcenter=(40.758895, -73.985131))
#      usually yields several tweets with location detail
#
def searchTwitter(searchString, count = 20, radius = 2, latlngcenter = None):    
    query = "https://api.twitter.com/1.1/search/tweets.json?q=" + quote_plus(searchString) + "&count=" + str(count)

    # if you want JSON results that provide full text of tweets longer than 140
    # characters, add "&tweet_mode=extended" to your query string.  The
    # JSON structure will be different, so you'll have to check Twitter docs
    # to extract the relevant text and entities.
    #query = query + "&tweet_mode=extended" 
    if latlngcenter != None:
        query = query + "&geocode=" + str(latlngcenter[0]) + "," + str(latlngcenter[1]) + "," + str(radius) + "km"
    global response
    response = requests.get(query, auth=client)
    resultDict = json.loads(response.text)
    # The most important information in resultDict is the value associated with key 'statuses'
    tweets = resultDict['statuses']
    tweetsWithGeoCount = 0 
    for tweetIndex in range(len(tweets)):
        tweet = tweets[tweetIndex]
        if tweet['coordinates'] != None:
            tweetsWithGeoCount += 1
            print("Tweet {} has geo coordinates.".format(tweetIndex))           
    return tweets
    

# sometimes tweets contain emoji or other characters that can't be
# printed in Python shell, yielding runtime errors when you attempt
# to print.  This function can help prevent that, replacing such charcters
# with '?'s.  E.g. for a tweet, you can do print(printable(tweet['text']))
#
def printable(s):
    result = ''
    for c in s:
        result = result + (c if c <= '\uffff' else '?')
    return result

#####

# You don't need the following functions for HW 9. They are just additional
# examples of Twitter API use.
#
def whoIsFollowedBy(screenName):
    global response
    global resultDict
    
    query = "https://api.twitter.com/1.1/friends/list.json?&count=50"
    query = query + "&screen_name={}".format(screenName)
    response = requests.get(query, auth=client)
    resultDict = json.loads(response.text)
    for person in resultDict['users']:
        print(person['screen_name'])
    
def getMyRecentTweets():
    global response
    global data
    global statusList 
    query = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    response = requests.get(query,auth=client)
    statusList = json.loads(response.text)
    for tweet in statusList:
        print(printable(tweet['text']))
        print()

#
# In HW10 and 11, you will use two Google services, Google Static Maps API
# and Google Geocoding API.  Both require use of an API key.
# 
# When you have the API key, put it between the quotes in the string below
GOOGLEAPIKEY = "AIzaSyAvaSR9dhWXrKuaX2Y9cI_mk-X3hcweidM"

# To run the HW10 program, call the last function in this file: HW10().

# The Globals class demonstrates a better style of managing "global variables"
# than simply scattering the globals around the code and using "global x" within
# functions to identify a variable as global.
#
# We make all of the variables that we wish to access from various places in the
# program properties of this Globals class.  They get initial values here
# and then can be referenced and set anywhere in the program via code like
# e.g. Globals.zoomLevel = Globals.zoomLevel + 1
#
class Globals:
   
   rootWindow = None
   mapLabel = None

   entryBox = None
   entryBoxLabel = None
   twitterEntryBox = None
   twitterEntryBoxLabel = None
   zoomUp = None
   zoomDown = None
   mapType = None
   standardRadioButton = None
   satelliteRadioButton = None
   terrainRadioButton = None
   hybridRadioButton = None

   selectedButtonText = None
   
   defaultLocation = "Mauna Kea, Hawaii"
   mapLocation = defaultLocation
   mapFileName = 'googlemap.gif'
   mapSize = 400
   zoomLevel = 9

   mapCenter = None

   tweetInfo = None
   currentTweetIndex = None
   currentTweetURLIndex = None

   numberOfTweetsRetrievedLabel = None
   currentTweetText = None
   currentTweetTextLabel = None
   nextTweetButton = None
   previousTweetButton = None
   nextURLButton = None
   previousURLButton = None
   URLIndexLabel = None

   tweetLatLonList = []

   markerArg = None

def nextTweet():
    Globals.currentTweetIndex+=1
    Globals.currentTweetTextLabel.configure(text="Current Tweet (index {}/{}) is:".format(Globals.currentTweetIndex, len(Globals.tweetInfo)-1))
    displayTweet()
    displayMap()
def previousTweet():
    Globals.currentTweetIndex-=1
    Globals.currentTweetTextLabel.configure(text="Current Tweet (index {}/{}) is:".format(Globals.currentTweetIndex, len(Globals.tweetInfo)-1))
    displayTweet()
    displayMap()
def nextURL():
    if Globals.tweetInfo[Globals.currentTweetIndex]['entities']['urls'] != None:
        if Globals.currentTweetURLIndex==None or Globals.currentTweetURLIndex==len(Globals.tweetInfo[Globals.currentTweetIndex]['entities']['urls'])-1:
            Globals.currentTweetURLIndex = 0
        else:
            Globals.currentTweetURLIndex+=1
        beforefix = str(Globals.tweetInfo[Globals.currentTweetIndex]['entities']['urls'][Globals.currentTweetURLIndex])
        firstindex = None
        lastindex = None
        afterfix = None
        for i in range(len(beforefix)):
            if beforefix[i:i+5]=="', 'e":
                afterfix = beforefix[9:i]
                i ==len(beforefix)
        webbrowser.open(afterfix)
def previousURL():
    if Globals.tweetInfo[Globals.currentTweetIndex]['entities']['urls'] != None:
        if Globals.currentTweetURLIndex==None or Globals.currentTweetURLIndex ==0:
            Globals.currentTweetURLIndex = len(Globals.tweetInfo[Globals.currentTweetIndex]['entities']['urls'])-1
        else:
            Globals.currentTweetURLIndex-=1
        beforefix = str(Globals.tweetInfo[Globals.currentTweetIndex]['entities']['urls'][Globals.currentTweetURLIndex])
        firstindex = None
        lastindex = None
        afterfix = None
        for i in range(len(beforefix)):
            if beforefix[i:i+5]=="', 'e":
                afterfix = beforefix[9:i]
                i ==len(beforefix)
        webbrowser.open(afterfix)
def generateMarkerString(tweetIndex, tweetLatLonList, mapCenterLatLon):
    latlonlist = []
    for i in range(len(tweetLatLonList)):
        if tweetLatLonList[i]==None:
                latlonlist.append(mapCenterLatLon)
        else:
                latlonlist.append(tweetLatLonList[i])
    answer = "&markers=color:red|{}&markers=color:green|size:small".format(latlonlist[tweetIndex])
    for i in range(len(latlonlist)):
        if not i == tweetIndex:
            answer += "|{}".format(latlonlist[i])
    #getting rid of [] brackets and spaces from answer
    nextone = True
    i = 0
    while nextone == True:
        if i < len(answer):
            if answer[i] == "[" or answer[i]=="]" or answer[i]==" " or answer[i]=="(" or answer[i]==")":
                answer = answer[:i] + answer[i+1:]
                i = i-1
            i = i+1
        else:
            nextone=False
    return answer


def radioButtonChosen():
    if choiceVar.get() == 1:
        Globals.selectedButtonText = "roadmap"
    elif choiceVar.get() ==2:
        Globals.selectedButtonText = "satellite"
    elif choiceVar.get() == 3:
        Globals.selectedButtonText = "terrain"
    elif choiceVar.get() == 4:
        Globals.selectedButtonText = "hybrid"
    Globals.mapType = Globals.selectedButtonText
    readEntryAndDisplayMap()

def upZoom():
    Globals.zoomLevel = Globals.zoomLevel+1
    Globals.zoomLevelLabel.configure(text = "Zoom Level is {}".format(Globals.zoomLevel))
    readEntryAndDisplayMap()
def downZoom():
    Globals.zoomLevel = Globals.zoomLevel-1
    Globals.zoomLevelLabel.configure(text = "Zoom Level is {}".format(Globals.zoomLevel))
    readEntryAndDisplayMap()
   
# Given a string representing a location, return 2-element tuple
# (latitude, longitude) for that location 
#
# See https://developers.google.com/maps/documentation/geocoding/
# for details about Google's geocoding API.
#
#
def geocodeAddress(addressString):
   urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
   geoURL = urlbase + quote_plus(addressString)
   geoURL = geoURL + "&key=" + GOOGLEAPIKEY

   # required (non-secure) security stuff for use of urlopen
   ctx = ssl.create_default_context()
   ctx.check_hostname = False
   ctx.verify_mode = ssl.CERT_NONE
   
   stringResultFromGoogle = urlopen(geoURL, context=ctx).read().decode('utf8')
   jsonResult = json.loads(stringResultFromGoogle)
   if (jsonResult['status'] != "OK"):
      print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
      result = (0.0, 0.0) # this prevents crash in retrieveMapFromGoogle - yields maps with lat/lon center at 0.0, 0.0
   else:
      loc = jsonResult['results'][0]['geometry']['location']
      result = (float(loc['lat']),float(loc['lng']))
   return result

# Contruct a Google Static Maps API URL that specifies a map that is:
# - is centered at provided latitude lat and longitude long
# - is "zoomed" to the Google Maps zoom level in Globals.zoomLevel
# - Globals.mapSize-by-Globals.mapsize in size (in pixels), 
# - will be provided as a gif image
#
# See https://developers.google.com/maps/documentation/static-maps/
#
# YOU WILL NEED TO MODIFY THIS TO BE ABLE TO
# 1) DISPLAY A PIN ON THE MAP
# 2) SPECIFY MAP TYPE - terrain vs road vs ...
#
def getMapUrl():
   lat, lng = geocodeAddress(Globals.mapLocation)
   urlbase = "http://maps.google.com/maps/api/staticmap?"
   args = "center={},{}&zoom={}&size={}x{}&format=gif&maptype={}{}".format(lat,lng,Globals.zoomLevel,Globals.mapSize,Globals.mapSize,Globals.mapType, Globals.markerArg)
   args = args + "&key=" + GOOGLEAPIKEY
   mapURL = urlbase + args
   return mapURL

# Retrieve a map image via Google Static Maps API, storing the 
# returned image in file name specified by Globals' mapFileName
#
def retrieveMapFromGoogle():
   url = getMapUrl()
   urlretrieve(url, Globals.mapFileName)

########## 
#  basic GUI code

def displayTweet():
    if Globals.tweetInfo != None:
       if len(Globals.tweetInfo)!=0:
           
            Globals.currentTweetText.configure(state=tkinter.NORMAL)
            Globals.currentTweetText.delete(1.0,tkinter.END)
            Globals.currentTweetText.insert(1.0,"tweet text is: {}, \naccount screen name is: {}, \naccount name is: {}".format(printable(Globals.tweetInfo[Globals.currentTweetIndex]["text"]), printable(Globals.tweetInfo[Globals.currentTweetIndex]["user"]["screen_name"]), printable(Globals.tweetInfo[Globals.currentTweetIndex]["user"]["name"])))
            Globals.currentTweetText.configure(state=tkinter.DISABLED)
            Globals.URLIndexLabel.configure(text = "There are {} URL's in tweet".format(len(Globals.tweetInfo[Globals.currentTweetIndex]['entities']['urls'])))
            Globals.currentTweetTextLabel.configure(text="Current Tweet (index {}/{}) is:".format(Globals.currentTweetIndex, len(Globals.tweetInfo)-1))
            Globals.currentTweetURLIndex = 0
    
    
def displayMap():
   Globals.markerArg = ""
   if Globals.tweetInfo != None:
       if len(Globals.tweetInfo)!=0:  
           Globals.markerArg = generateMarkerString(Globals.currentTweetIndex, Globals.tweetLatLonList, Globals.mapCenter)
   retrieveMapFromGoogle()    
   mapImage = tkinter.PhotoImage(file=Globals.mapFileName)
   Globals.mapLabel.configure(image=mapImage)
   # next line necessary to "prevent (image) from being garbage collected" - http://effbot.org/tkinterbook/label.htm
   Globals.mapLabel.mapImage = mapImage
   
def readEntryAndDisplayMap():
   #### you should change this function to read from the location from an Entry widget
   #### instead of using the default location\
   Globals.mapLocation = Globals.entryBox.get()
   Globals.mapCenter = geocodeAddress(Globals.mapLocation)
   Globals.tweetInfo = searchTwitter(Globals.twitterEntryBox.get(), latlngcenter = Globals.mapCenter)
   Globals.numberOfTweetsRetrievedLabel.configure(text = "Number of Tweets Retrieved is {}".format(len(Globals.tweetInfo)))
   Globals.currentTweetIndex = 0
   Globals.URLIndexLabel.configure(text="There are 0 URL's in current tweet")
   Globals.currentTweetTextLabel.configure(text="Current Tweet is:")
   Globals.currentTweetText.configure(state=tkinter.NORMAL)
   Globals.currentTweetText.delete(1.0,tkinter.END)
   Globals.currentTweetText.configure(state=tkinter.DISABLED)
   for i in range(len(Globals.tweetInfo)):
       if Globals.tweetInfo[i]['coordinates']==None:
           Globals.tweetLatLonList.append(None)
       else:
           beforefix = str(Globals.tweetInfo[i]['coordinates'])
           firstindex = None
           lastindex = None
           for i in range(len(beforefix)):
               if beforefix[i] == "[":
                   firstindex = i
               if beforefix[i] == "]":
                   lastindex = i
           afterfix = beforefix[firstindex+1:lastindex]
           for i in range(len(afterfix)):
               if afterfix[i]==",":
                   commaindex = i
           afterfix = afterfix[commaindex+2:] + ", " + afterfix[:commaindex]
           Globals.tweetLatLonList.append(afterfix)
   displayMap()
   displayTweet()
     
def initializeGUIetc():

   Globals.rootWindow = tkinter.Tk()
   Globals.rootWindow.title("HW11")

   mainFrame = tkinter.Frame(Globals.rootWindow) 
   mainFrame.pack(side=tkinter.LEFT)

   # until you add code, pressing this button won't change the map (except
   # once, to the Beijing location "hardcoded" into readEntryAndDisplayMap)
   # you need to add an Entry widget that allows you to type in an address
   # The click function should extract the location string from the Entry widget
   # and create the appropriate map.
   readEntryAndDisplayMapButton = tkinter.Button(mainFrame, text="Show me the map!", command=readEntryAndDisplayMap)
   readEntryAndDisplayMapButton.pack()

   # we use a tkinter Label to display the map image
   Globals.mapLabel = tkinter.Label(mainFrame, width=Globals.mapSize, bd=2, relief=tkinter.FLAT)
   Globals.mapLabel.pack()

   Globals.entryBoxLabel=tkinter.Label(mainFrame, text="Enter the location:")
   Globals.entryBoxLabel.pack()
   
   Globals.entryBox = tkinter.Entry(mainFrame)
   Globals.entryBox.insert(0,Globals.mapLocation)
   Globals.entryBox.pack()

   Globals.zoomLevelLabel = tkinter.Label(mainFrame, text="Zoom Level is {}".format(Globals.zoomLevel))
   Globals.zoomLevelLabel.pack()
   Globals.zoomUp = tkinter.Button(mainFrame, text = "+", command=upZoom)
   Globals.zoomUp.pack()
   Globals.zoomDown = tkinter.Button(mainFrame, text = "-", command=downZoom)
   Globals.zoomDown.pack()

   leftFrame = tkinter.Frame(Globals.rootWindow)
   leftFrame.pack(side=tkinter.RIGHT)
   Globals.twitterEntryBoxLabel = tkinter.Label(leftFrame, text="enter search term:")
   Globals.twitterEntryBoxLabel.pack(side=tkinter.TOP)
   Globals.twitterEntryBox = tkinter.Entry(leftFrame)
   Globals.twitterEntryBox.pack(side=tkinter.TOP)
   Globals.numberOfTweetsRetrievedLabel = tkinter.Label(leftFrame)
   Globals.numberOfTweetsRetrievedLabel.pack(side=tkinter.TOP)
   Globals.currentTweetTextLabel = tkinter.Label(leftFrame, text = "Current Tweet is:")
   Globals.currentTweetTextLabel.pack(side=tkinter.TOP)
   Globals.currentTweetText = tkinter.Text(leftFrame, height = 10, width = 40)
   Globals.currentTweetText.pack(side=tkinter.TOP)
   Globals.currentTweetText.configure(state=tkinter.DISABLED)
   Globals.nextTweetButton = tkinter.Button(leftFrame, text = "show next tweet", command = nextTweet)
   Globals.nextTweetButton.pack(side=tkinter.TOP)
   Globals.previousTweetButton = tkinter.Button(leftFrame, text = "show previous tweet", command = previousTweet)
   Globals.previousTweetButton.pack(side=tkinter.TOP)
   Globals.URLIndexLabel = tkinter.Label(leftFrame, text = "There are 0 URL's in current tweet")
   Globals.URLIndexLabel.pack(side = tkinter.TOP)
   Globals.nextURLButton = tkinter.Button(leftFrame, text = "go to next URL", command = nextURL)
   Globals.nextURLButton.pack(side=tkinter.TOP)
   Globals.previousURLButton = tkinter.Button(leftFrame, text = "go to previous URL", command = previousURL)
   Globals.previousURLButton.pack(side=tkinter.TOP)
   
   global choiceVar
   choiceVar = tkinter.IntVar()
   choiceVar.set(1)

   Globals.standardRadioButton = tkinter.Radiobutton(mainFrame, text = "roadmap view", variable = choiceVar, value = 1, command = radioButtonChosen)
   Globals.standardRadioButton.pack()
   Globals.satteliteRadioButton = tkinter.Radiobutton(mainFrame, text = "sattelite view", variable = choiceVar, value = 2, command = radioButtonChosen)
   Globals.satteliteRadioButton.pack()
   Globals.terrainRadioButton = tkinter.Radiobutton(mainFrame, text = "terrain view", variable = choiceVar, value = 3, command = radioButtonChosen)
   Globals.terrainRadioButton.pack()
   Globals.hybridRadioButton = tkinter.Radiobutton(mainFrame, text = "hybrid view", variable = choiceVar, value = 4, command = radioButtonChosen)
   Globals.hybridRadioButton.pack()
   


def HW11():
    authTwitter()
    initializeGUIetc()
    displayMap()
    Globals.rootWindow.mainloop()
