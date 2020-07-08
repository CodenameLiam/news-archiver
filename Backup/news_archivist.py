
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N9959807
#    Student name: LIAM PERCY
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  News Archivist
#
#  In this task you will combine your knowledge of HTMl/XML mark-up
#  languages with your skills in Python scripting, pattern matching
#  and Graphical User Interface development to produce a useful
#  application for maintaining and displaying archived news or
#  current affairs stories on a topic of your own choice.  See the
#  instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements that were used in our sample
# solution.  You should be able to complete this assignment using
# these functions only.

# Import the function for opening a web document given its URL.
from urllib.request import urlopen

# Import the function for finding all occurrences of a pattern
# defined via a regular expression, as well as the "multiline"
# and "dotall" flags.
from re import findall, MULTILINE, DOTALL

# A function for opening an HTML document in your operating
# system's default web browser. We have called the function
# "webopen" so that it isn't confused with the "open" function
# for writing/reading local text files.
from webbrowser import open as webopen

# An operating system-specific function for getting the current
# working directory/folder.  Use this function to create the
# full path name to your HTML document.
from os import getcwd

# An operating system-specific function for 'normalising' a
# path to a file to the path-naming conventions used on this
# computer.  Apply this function to the full name of your
# HTML document so that your program will work on any
# operating system.
from os.path import normpath
    
# Import the standard Tkinter GUI functions.
from tkinter import *
from tkinter.ttk import Combobox

# Import the SQLite functions.
from sqlite3 import *

# Import the date and time function.
from datetime import datetime

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#
# Name of the folder containing your archived web documents.  When
# you submit your solution you must include the web archive along with
# this Python program. The archive must contain one week's worth of
# downloaded HTML/XML documents. It must NOT include any other files,
# especially image files.
internet_archive = 'InternetArchive'

#OPEN DATABASE-------------------------------------------------------#
#Create a connection to the database.
connection = connect(database = 'event_log.db')

#Get a pointer into the database.
eventLogDB = connection.cursor()

#Set up a counter for each event logged
query = "SELECT max(Event_Number) FROM Event_Log"
#Select the highest event logged thus far
eventLogDB.execute(query)
results = eventLogDB.fetchall()
#If there are currently no events logged, the event number is 0
if results[0][0] == None:
        eventNumber = 0
#Otherwise the event number is the highest even logged thus far
else:
        eventNumber = results[0][0]

def logCheck():
    #Function to check if the user has checked the log button
    checked = check.get()
    return(checked)

def database():
    global eventNumber
    #Log the switch being turned on
    if logCheck() == 1:
       #Add 1 to the eventNumber counter
       eventNumber += 1
       print(eventNumber)
       #Execute an SQLite script to insert rows.
       sql = "INSERT INTO Event_log VALUES ('" + str(eventNumber) + "', 'Event logging switched on')"
       eventLogDB.execute(sql)
       #Commit the change to the database.
       connection.commit()

    #If the user is logging events, log the switch being turned off   
    if logCheck() == 0:
       #Add 1 to the eventNumber counter
       eventNumber += 1
       #Execute an SQLite script to insert rows.
       sql = "INSERT INTO Event_log VALUES ('" + str(eventNumber) + "', 'Event logging switched off')"
       eventLogDB.execute(sql)
       #Commit the change to the database.
       connection.commit()
       
#CHECK FILE ACCESSIBILITY--------------------------------------------#
def isAccessible(path, mode='r'):
    #Check if the file or directory at `path` can be accessed by the program
        try:
            f = open(path, mode)
            f.close()
        except IOError:
            return False
        return True

#EXTRACT NEWS--------------------------------------------------------#
def extractNews():
    #Function to extract specific pieces of information from the archive
    #based on the users date selection
    instruct['text'] = 'EXTRACTING NEWS...'
    #Informs the user that data is being extracted (probably won't see this
    #though, as the program executes too quickly

    if dayChoice() == 'TUESDAY 17th OCTOBER':
        #If the user has selected a particular day
        fileContents = open('InternetArchive/BBCTechnology_17Oct17.html', 'U').read()
        #Open a particular file
    elif dayChoice() == 'WEDNESDAY 18th OCTOBER':
        fileContents = open('InternetArchive/BBCTechnology_18Oct17.html', 'U').read()
    elif dayChoice() == 'THURSDAY 19th OCTOBER':
        fileContents = open('InternetArchive/BBCTechnology_19Oct17.html', 'U').read()
    elif dayChoice() == 'FRIDAY 20th OCTOBER':
        fileContents = open('InternetArchive/BBCTechnology_20Oct17.html', 'U').read()
    elif dayChoice() == 'SATURDAY 21st OCTOBER':
        fileContents = open('InternetArchive/BBCTechnology_21Oct17.html', 'U').read()
    elif dayChoice() == 'SUNDAY 22nd OCTOBER':
        fileContents = open('InternetArchive/BBCTechnology_22Oct17.html', 'U').read()
    elif dayChoice() == 'MONDAY 23rd OCTOBER':
        fileContents = open('InternetArchive/BBCTechnology_23Oct17.html', 'U').read()
    elif dayChoice() == 'LATEST NEWS':
        if isAccessible('InternetArchive/BBCTechnology_Latest.html') == True:
        #If the news selected is the latest news, make sure the user has first
        #extracted the latest news from the archive, and then either
            fileContents = open('InternetArchive/BBCTechnology_Latest.html', 'U').read()
            #Open it if it is available to them
        else:
            instruct['text'] = 'ERROR: NEWS FILE NOT FOUND IN ARCHIVE'
            return
            #Or present an error message and exit the function
    else:
        instruct['text'] = 'PLEASE CHOOSE A DATE...'
        return
        #If not date is selected, present an error message and exit the function
        
    #For each piece of important information about a give article (title, image,
    #description, fullstory link, publish date and image error, find the
    #necessary data from each article and add it to an array, 10 times
    title = []
    Titles = findall("<title><!\[CDATA\[[A-Za-z \',-\?!\./0-9]*",fileContents)
    for articles in range(1,11):
        title.append(Titles[articles].split("CDATA[")[1])

    image = []
    Images = findall('<media:thumbnail width="[0-9]+" height="[0-9]+" url="[A-Za-z0-9:/\._ -]*',fileContents)
    for articles in range(0,10):
        image.append(Images[articles].split('"',6)[5])

    description = []
    Descriptions = findall('<description><!\[CDATA\[[A-Za-z- .,\'0-9]*',fileContents)
    for articles in range(1,11):
        description.append(Descriptions[articles].split("CDATA[")[1])

    fullstory = []
    Fullstories = findall('<link>http://www.bbc.co.uk[/A-Za-z0-9.-]*',fileContents)
    for articles in range(2,12):
        fullstory.append(Fullstories[articles].split('<link>')[1])

    pubdate = []
    Pubdates = findall('<pubDate>[A-Za-z0-9 ,:]*',fileContents)
    for articles in range(0,10):
        pubdate.append(Pubdates[articles].split('<pubDate>')[1])

    error = []
    Errors = findall('<media:thumbnail width="[0-9]+" height="[0-9]+" url="[A-Za-z0-9:/\._ -]*',fileContents)
    for articles in range(0,10):
        error.append(Errors[articles].split('"',6)[5].split('/',5)[5])

    #Inform the user that the the news was successfully extracted
    instruct['text'] = 'NEWS EXTRACTED FROM ARCHIVE:'
    #Inform the user which date in particular was extracted
    track['text'] = dayChoice()

    #Return key information about the top 10 articles for a given day
    return title, image, description, fullstory, pubdate, error

#GENERATE HTML-----------------------------------------------------------#
def generateHTML():
    #Function to generate a new HTML document based on the information gathered
    #from the extracted news page
    if dayChoice() == 'LATEST NEWS':
        if isAccessible('InternetArchive/BBCTechnology_Latest.html') == False:
            instruct['text'] = 'ERROR: NEWS FILE NOT FOUND IN ARCHIVE'
            return
        #If the latest news is selected, and the user has not first extracted
        #said latest news, produce an error message and exit the function
    if str(dayChoice()) =='':
        instruct['text'] = 'PLEASE CHOOSE A DATE...'
        return
        #If the user has not selected a date, produce an error message and
        #exit the function
    else:
        #Otherwise, generate an HTML document

        #If the user is logging events, log the news being extracted
        global eventNumber
        if logCheck() == 1:
                #Add 1 to the eventNumber counter
                eventNumber = eventNumber + 1
                #Execute an SQLite script to insert rows.
                sql = "INSERT INTO Event_log VALUES ('" + str(eventNumber) + "', 'News extracted from archive')"
                eventLogDB.execute(sql)
                #Commit the change to the database.
                connection.commit()
        
        htmlTemplate = """<!DOCTYPE html>

        <html>

        <head>
        
            <title> BBC News Technology Archive</title>

            <style>
                body	{background-color: rgb(156,10,13); color:white;font-family: "Trebuchet MS", Helvetica, sans-serif;}
                h1	{width: 80%; margin-left: auto; margin-right: auto; text-align: center;  font-size: 40px}
                h2	{width: 80%; margin-left: auto; margin-right: auto; text-align: center; font-size: 25px}
                h3	{width: 80%; margin-left: auto; margin-right: auto; text-align: center; font-size: 16px}
                p       {width: 80%; margin-left: auto; margin-right: auto; text-align: left; font-size: 14px}
                img     {max-width: 80%; height: auto; width: auto\9}
                a:link, a:visited   {color:grey}
                a:hover             {color: white}
             </style>

        </head>

        <body>
        
            <h1>BBC NEWS TECHNOLOGY ARCHIVE</h1>
        
            <h2>***DATE***</h2>

            <div align="center">
                <img src = "https://goo.gl/qqc8nY" alt=BBC Logo>
            </div>

            <p>
                <strong>News Source</strong>
                <a href = http://feeds.bbci.co.uk/news/technology/rss.xml>http://feeds.bbci.co.uk/news/technology/rss.xml</a><br>
                <strong>Archivist:</strong> Liam Percy
            </p>

            <hr width = 80%>
        """
        #This is the initial formatting for the entire page, and the initial
        #body of the page, including a title, logo, source to the RSS feed
        #and archivist name. 
        htmlCode = htmlTemplate.replace('***DATE***', dayChoice())
        #Replaces the date in the HTML document with the users selected date
        htmlFile = open('BBCNewsArchive.html', 'w')
        htmlFile.write(htmlCode)
        htmlFile.close()
        #Opens the file and writes the above code to the HTML file

        for i in range(0,10):
            #for the top 10 articles on the selected day, add the following code
            htmlCode=  """
            <h3>***NUM***: ***TITLE***</h3>
                
                <div align="center">
                    <img style = "border-style:solid" src = "***IMAGE***" alt="Sorry, image ***ERROR*** could not be posted">
                </div>
                
                <p>
                    ***DESCRIPTION***
                </p>
                
                <p>
                    <strong>Full Story: </strong>
                    <a href = ***LINK***> ***LINK***</a>
                </p>
                
                <p>
                    <strong>Date Published: </strong>
                    ***PUBDATE***
                </p>

                <hr width = 80%>
            """
            #Opens the existing code and replaces the necessary information
            #in the updated body information above 
            htmlCode = htmlCode.replace('***TITLE***', extractNews()[0][i])
            #Extract news [0][0] returns the title from the 1st news article
            #on the selected day...
            #Extract news [0][1] returns the title from the 2nd news article
            #on the selected day... etc
            htmlCode = htmlCode.replace('***IMAGE***', extractNews()[1][i])
            htmlCode = htmlCode.replace('***DESCRIPTION***', extractNews()[2][i])
            htmlCode = htmlCode.replace('***LINK***', extractNews()[3][i])
            htmlCode = htmlCode.replace('***PUBDATE***', extractNews()[4][i])
            htmlCode = htmlCode.replace('***ERROR***', extractNews()[5][i])
            htmlCode = htmlCode.replace('***NUM***', str(i+1))
            #Adds a number to each article for easier navigation
            htmlFile = open('BBCNewsArchive.html', 'a')
            htmlFile.write(htmlCode)
            htmlFile.close()
            #Opens the file and writes the above code to the HTML file
        
#DISPLAY NEWS-------------------------------------------------------#
def displayNews():
    #Function to display the currently extracted and archived news
    #on the users default browser
    if str(dayChoice()) =='':
        instruct['text'] = 'PLEASE CHOOSE A DATE...'
        return
        #If the user has not selected a date, produce an error message and
        #exit the function
    elif track['text'] == '':
        instruct['text'] = 'PLEASE EXTRACT NEWS FIRST...'
        return
        #If the user has not pressed the extract button, produce an error
        #message and exit the function
    else:
        #Otherwise, display the page
        archiveLink = 'BBCNewsArchive.html'
        new = 2
        webopen(archiveLink, new)
        instruct['text'] = 'EXTRACTED NEWS DISPLAYED IN BROWSER:'
        track['text'] = dayChoice()
        #Informs the user that they have currently displayed their selected
        #days news in their browser
        
        #If the user is logging events, log the news being displayed
        global eventNumber
        if logCheck() == 1:
                #Add 1 to the eventNumber counter
                eventNumber = eventNumber + 1
                #Execute an SQLite script to insert rows.
                sql = "INSERT INTO Event_log VALUES ('" + str(eventNumber) + "', 'Extracted news displayed in browser')"
                eventLogDB.execute(sql)
                #Commit the change to the database.
                connection.commit()

#ARCHIVE LATEST NEWS------------------------------------------------#
def archiveLatestNews():
    #Function to extract and archive the latest news from the RSS feed
    url = 'http://feeds.bbci.co.uk/news/technology/rss.xml'
    # Open the web document for reading
    web_page = urlopen(url)

    # Read its contents as a Unicode string
    web_page_contents = web_page.read().decode('UTF-8')

    # Write the contents to a text file (overwriting the file if it
    # already exists!)
    html_file = open('InternetArchive/BBCTechnology_Latest.html', 'w', encoding = 'UTF-8')
    html_file.write(web_page_contents)
    html_file.close()
    #Writes the information extracted from the feed to a new HTML document
    #located in the archive

    #Informs the user that the latest news has been archived successfully
    instruct['text'] = 'LATEST NEWS ARCHIVED SUCCESSFULLY'
    track['text'] = ''

    #If the user is logging events, log the news being displayed
    global eventNumber
    if logCheck() == 1:
            #Add 1 to the eventNumber counter
            eventNumber = eventNumber + 1
            #Execute an SQLite script to insert rows.
            sql = "INSERT INTO Event_log VALUES ('" + str(eventNumber) + "', 'Latest news downloaded and stored in archive')"
            eventLogDB.execute(sql)
            #Commit the change to the database.
            connection.commit()             

#GUI----------------------------------------------------------------#
#A segment of code the handles the creation of a GUI for the program
days = \
     ['TUESDAY 17th OCTOBER',
      'WEDNESDAY 18th OCTOBER',
      'THURSDAY 19th OCTOBER',
      'FRIDAY 20th OCTOBER',
      'SATURDAY 21st OCTOBER',
      'SUNDAY 22nd OCTOBER',
      'MONDAY 23rd OCTOBER',
      'LATEST NEWS']
#The days that the user can chose from

def dayChoice():
    #Function to check which day the user has chosen from the combobox
    choice = options.get()
    return(choice)

# Create a window
GUI = Tk()

# Gives the window a title
GUI.title('BBC News Technology Archive')
#Changes the windows background colour to white
GUI['bg'] = 'white'
#Defines the BBC red colour for GUI consistency
BBCRed = '#%02x%02x%02x' % (156,11,13)

#Loads the BBC logo into the GUI and places it at the top of the GUI
BBCImage = PhotoImage(file = 'BBCNews.gif')
BBCLogo = Label(GUI, image = BBCImage)
BBCLogo.grid(row = 0, column = 0, columnspan = 3)
#Removes the logo border
BBCLogo['bd'] = 0

#Creates a label displaying TECHNOLOGY, indicating that this program
#purely archives information from the BBC technology feed
#Places label below logo
tech = Label(GUI, text = 'TECHNOLOGY', font = ('Petra',60),
             fg = BBCRed, bg = 'white')
tech.grid(row = 1, column = 0, columnspan = 3, pady = 10)

#A label for providing instructions or information to the user
instruct = Label(GUI, text = 'CHOOSE WHICH NEWS TO EXTRACT...', font = ('Petra',16),
                 fg = BBCRed, bg = 'white')
instruct.grid(row = 2, column = 0, columnspan = 3)

#A label providing further information to the user about their selected dates
track = Label(GUI, text = '', font = ('Petra',12),
                 fg = BBCRed, bg = 'white')
track.grid(row = 3, column = 0, columnspan = 3)

#A combo box widget to display the choices of element name
options = Combobox(GUI, values = days, justify = CENTER, font = ('Petra',20),
                   width = 30, state = 'readonly')
options.grid(row = 4, column = 0, columnspan = 3, pady=10)


#A button to push when the user is happy with their choice
extract = Button(GUI, text = 'EXTRACT NEWS', command = generateHTML,
                        font = ('Petra',15), bg = 'white',
                        activebackground = BBCRed, bd = 1,
                        activeforeground = 'white', width = 22)
extract.grid(row = 5, column = 0)

#A button to push so the user can display their selected webpage
display = Button(GUI, text = 'DISPLAY NEWS', command = displayNews,
                 font = ('Petra',15), 
                 bg = 'white', activebackground = BBCRed, bd = 1,
                 activeforeground = 'white', width = 22)
display.grid(row = 5, column = 1, pady = 10)

#A button to archive the latest edition of the BBC technology news
archive = Button(GUI, text = 'ARCHIVE LATEST NEWS', command = archiveLatestNews,
                 font = ('Petra',15), bg = 'white', activebackground = BBCRed,
                 activeforeground = 'white', width = 22, bd = 1,)
archive.grid(row = 5, column = 2, pady = 10)

#A checkbox to allow the user to log events performed on the GUI
check = IntVar()
log = Checkbutton(GUI, text = 'LOG EVENTS', variable = check, command = database,
                  font = ('Petra',15), bg = 'white')
log.grid(row = 6, column = 1, pady = 10)
    
#Start the event loop to react to user inputs
GUI.mainloop()

#Close the cursor and release the server connection
eventLogDB.close()
connection.close()
