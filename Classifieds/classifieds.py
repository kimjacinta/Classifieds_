
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 2, 2021.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
student_number = 10722831  # put your student number here as an integer
student_name = 'Kim Csoka'  # put your name here as a character string
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#


#-----Assignment Description-----------------------------------------#
#
#  Classified Ads
#
#  In this assignment you will combine your knowledge of HTMl/CSS
#  mark-up languages with your skills in Python scripting, pattern
#  matching, databases and Graphical User Interface design to produce
#  a robust, interactive application that allows its user to view
#  and save items currently for sale from multiple online sources.
#
#  See the client's requirements accompanying this file for full
#  details.
#
#--------------------------------------------------------------------#


#-----Initialisation Steps-------------------------------------------#
#

# Import standard Python 3 modules needed to complete this assignment.
# You should not need to use any modules other than those provided
# in a standard Python 3 installation for your solution.
#
# In particular, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort
from tkinter.font import BOLD

# A function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via the "download" function below.)
from urllib.request import urlopen

# Some standard Tkinter functions.  (You WILL need to use
# SOME of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: Although you can import individual widgets
# from the "tkinter.tkk" module, DON'T import ALL of them
# using a "*" wildcard because the "tkinter.tkk" module
# includes alternative versions of standard widgets
# like "Label".)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  (You do not necessarily need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  (You WILL need to use this function
# in your solution.)
from webbrowser import open as urldisplay

# All the standard SQLite functions.
from sqlite3 import *

# HTML Unescape function
from html import unescape

# Confirm that the student has declared their authorship.
# You must NOT change any of the code below.
if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()

#
#--------------------------------------------------------------------#


#-----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  (You are not required to use this function, but it may
# save you some effort.)
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we discourage using this
#      option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url='http://www.wikipedia.org/',
             target_filename='downloaded_document',
             filename_extension='html',
             save_file=True,
             char_set='UTF-8',
             incognito=FALSE):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if incognito:
            # Pretend to be a web browser instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header(
                'User-Agent',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print(
            "Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " +
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" +
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " +
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(
                target_filename + '.' + filename_extension, 'w',
                encoding=char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" +
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#


#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.

#----------------SET UP WINDOW / FRAME SETTINGS-----------------#

# Create a window and name it
window = Tk()
window.title('Local Classifieds') # Naming window
BG = '#603E94' # Background

# Window size setting
window.geometry('500x780')
window.minsize(500, 780)

# Window color settings
window['bg'] = BG
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Creating main frame for frames
frame = Frame(window)
frame['bg'] = BG
frame.grid(row=0, column=0, sticky=NSEW)

# Even out the frames 
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Defining fonts
Title_font = ('Arial', 28, 'bold')
Label_font = ('Arial', 20, 'bold')
Widget_font = ('Arial', 15)

# Defining options to not repeat code
OPTIONS = {'font': Label_font}
MARGIN = 6  # pixels

#-------------------------DISPLAYING LOGO IN GUI-------------------#
# Importing Logo
logo = PhotoImage(file='Classified_logo.png')
# Scale Logo Picture
width = 0.5 * logo.width()
height = 0.5 * logo.height()
# Sample every pixel
scale_w = int(logo.width() / width)
scale_h = int(logo.height() / height)
# Create new subsampled image
logo_scaled = logo.subsample(x=scale_w, y=scale_h)
# Place PhotoImage inside Label
logo_label = Label(frame, image=logo_scaled, width=width, height=height, bg=BG)
logo_label.grid(row=0, column=0, columnspan=2, sticky=NSEW)

#-----------------------DISPLAYING ITEM INFORMATION IN GUI---------#

# Variable settings
website_url = ''
current_description_trans = ''
current_price_trans = 0

# Function when user selects a category
def updating_the_category(args): # This function is used as command in lines 511 - 513

    #---------EXTRACTING INFORMATION FROM CLASSIFIED SITES-------------#

    #---------------NL CLASSIFIEDS------------#
    try: # Try to execute the following
        # Downloading web document
        nl_download = download('https://www.nlclassifieds.com/Electronics/c16000?sortBy=dateDesc')
        # Source 
        nl_source = 'Source: NL Classifieds'
        nl_site_name = nl_source[8:]
        # URL
        nl_url = 'https://www.nlclassifieds.com/Electronics/c16000?sortBy=dateDesc'
        # Description
        nl_description = findall('style=\"color: #003c94;\">(.*)</a>', nl_download)
        # Price
        nl_price = findall('<div class=\"price\">\s+([\$\d+(?:\.,\d+)?]+)<', nl_download)
    # Exception handling in case of website changing, no internet or other error codes
    except: 
        print('There seems to be an issue with the NL classifieds website.') # print this in shell.
        nl_source = 'Source: None' # Display following in GUI
        nl_url = 'No URL available' # Display following in GUI
        nl_description_error = 'Currently there is no item description available. Please try at a later time.' # Display following as description in GUI
        nl_description = []
        nl_description.extend([nl_description_error for i in range(3)]) # Make list with error message above (currently,....) 3x
        nl_price_error = ['$--.--']
        nl_price = []
        nl_price.extend([nl_price_error for i in range(3)]) # Make list with ['$--.--', '$--.--', '$--.--']
    
    #-------------------EBAY-------------------#
    # Downloading web document
    try: # Try to execute the following
        ebay_download = download('https://www.ebay.com.au/b/Cars/29690/bn_1843284')
        # Source 
        ebay_source = 'Source: Ebay'
        ebay_site_name = ebay_source[8:]
        # URL
        ebay_url = 'https://www.ebay.com.au/b/Cars/29690/bn_1843284'
        # Finding description / Description
        ebay_description = findall('<h3[^\>]*s-item__title">([A-Za-z -1.0-9.0;]+)<', ebay_download)
        # Finding Price
        ebay_price = findall('s-item__price">([AU \$\d+(?:\.,\d+)?]+)', ebay_download)
    # Exception handling in case of website changing, no internet or other error codes
    except:
        print('There seems to be an issue with the Ebay website.')
        ebay_source = 'Source: None'
        ebay_url = 'No URL available'
        ebay_description_error = 'Currently there is no item description available. Please try at a later time.'
        ebay_description = []
        ebay_description.extend([ebay_description_error for i in range(3)])
        ebay_price_error = ['$--.--']
        ebay_price = []
        ebay_price.extend([ebay_price_error for i in range(3)]) 

    #-------------------GUMTREE-------------------#
    try: # Try to execute the following
        # Downloading web document
        gumtree_page = download('https://www.gumtree.com.au/s-bags/qld/c18574l3008841')
        # Source 
        gumtree_source = 'Source: Gumtree'
        gumtree_site_name = gumtree_source[8:]
        # URL
        gumtree_url = 'https://www.gumtree.com.au/s-bags/qld/c18574l3008841'
        # Finding description / Description
        gumtree_description = findall('aria-label=\"(.*).', gumtree_page)
        # Finding Price
        gumtree_price = findall('aria-label=\".*\s+Price: (.*) .', gumtree_page) 
    # Exception handling in case of website changing, no internet or other error codes
    except:
        print('There seems to be an issue with the Gumtree site.')
        gumtree_source = 'Source: None'
        gumtree_url = 'No URL available'
        gumtree_description_error = 'Currently there is no item description available. Please try at a later time.'
        gumtree_description = []
        gumtree_description.extend([gumtree_description_error for i in range(3)])
        gumtree_price_error = ['$--.--']
        gumtree_price = []
        gumtree_price.extend([gumtree_price_error for i in range(3)]) 
    
    #-------------WHEN CATEGORIES IN GUI IS SELECTED-------------------#

    # Making sure changes to variables are possible by using global 
    global current_description 
    global current_price
    global name_ad_text
    global website_title
    global website_url
    global show_details
    global current_selection_of_category # the current latest item
    
    if args == 1: # If NL Search Sell buttom is selected
        current_description = nl_description # current description becomes nl description
        current_price = nl_price # current price becomes nl item price
        website_title = nl_site_name # website_title becomes the NL site name (this is for SQL db)
        website_url = nl_url # website url becomes NL URL (this is for the show details function)
        source_name['text'] = nl_source # Source becomes nl source and is displayed in GUI
        url_text['text'] = nl_url # URL becomes NL URL and is displayed in the GUI

    if args == 2: # If Ebay button is selected
        current_description = ebay_description # If ebay Search Sell buttom is selected
        current_price = ebay_price # current description becomes ebay description
        website_title = ebay_site_name # website_title becomes the ebay site name (this is for SQL db)
        website_url = ebay_url # website url becomes ebay URL (this is for the show details function)
        source_name['text'] = ebay_source # Source becomes ebay source and is displayed in GUI
        url_text['text'] = ebay_url # URL becomes ebay URL and is displayed in the GUI
        
    if args == 3:# If Gumtree is selected 
        current_description = gumtree_description # If gumtree Search Sell buttom is selected
        current_price = gumtree_price # current description becomes gumtree description
        website_title = gumtree_site_name # website_title becomes the gumtree site name (this is for SQL db)
        website_url = gumtree_url # website url becomes gumtree URL (this is for the show details function)
        source_name['text'] = gumtree_source # Source becomes gumtree source and is displayed in GUI
        url_text['text'] = gumtree_url # URL becomes gumtree URL and is displayed in the GUI

#-------------FUNCTIONS FOR WHEN ITEM BUTTOMS IN GUI ARE SELECTED-------------------#

# Default current item
current_selection_of_category = 1
# Making sure that when latest is clicked, the correct text is displayed
def latest_selected():
    try:
        global current_selection_of_category
        global current_price_trans
        global current_description_trans
        current_selection_of_category = 1
        # When latest selected, the latest item description for selected category is displayed in GUI
        item_text['text'] = current_description[0] 
        # When latest selected, the latest item price is displayed in GUI
        price_text['text'] = current_price[0] 
        # Converting description & price from lists to string for SQL and to edit description 
        current_description_trans = ''.join(current_description[0])
        current_price_trans = ''.join(current_price[0])
        # Making sure that unicode characters in description etc. are not displayed in GUI by replace method
        current_description_trans = unescape(current_description_trans)

    except NameError:
        item_text['text'] = ('Please select a category first.')
 
# Making sure that when second latest is clicked, the correct text is displayed
def second_selected():
    try:
        global current_selection_of_category
        global current_description_trans
        global current_price_trans
        current_selection_of_category = 2
        # When second latest selected, the second latest item description for selected category is displayed
        item_text['text'] = current_description[1]
        # When second latest selected, the second latest item price is displayed
        price_text['text'] = current_price[1]
        # Converting description & price from lists to string for SQL and to edit description 
        current_description_trans = ''.join(current_description[1])
        current_price_trans = ''.join(current_price[1])
        # Making sure that unicode characters in description etc. are not displayed in GUI by replace method
        current_description_trans = unescape(current_description_trans)
    except NameError:
        item_text['text'] = ('Please select a category first.')

# Making sure that when third latest is clicked, the correct text is displayed
def third_selected():
    try:
        global current_selection_of_category
        global current_description_trans
        global current_price_trans
        current_selection_of_category = 3
        # When third latest selected, the third latest item description for selected category  is displayed
        item_text['text'] = current_description[2]
        # When third latest selected, the third latest item price is displayed
        price_text['text'] = current_price[2]
        # Converting description & price from lists to string for SQL and to edit description 
        current_description_trans = ''.join(current_description[2])
        current_price_trans = ''.join(current_price[2])
        # Making sure that unicode characters in description etc. are not displayed in GUI by replace method
        current_description_trans = unescape(current_description_trans)
    except NameError:
        item_text['text'] = ('Please select a category first.')

# When selecting 'Show Details' forward user to website
def go_to_website():
    if website_url == '': # If no category is selected, prompt user to select one
        item_text['text'] = ('Please select a category.')
    else: # If a category is selected user will be forwarded to the correct website
        urldisplay(website_url)


#-------------------SAVING SELECTION IN SQL DATABASE-------------------#

# Save selection function for saving in SQL database
def save_selection_in_db(): # used as command in line 541
    # Create a connection to the database.
    connection = connect(database = 'classifieds.db') 
    # Get a cursor on the database to allow to execute SQL queries and get the results
    classifieds_db = connection.cursor() 
    # Construct the SQLite delete statement
    try:
        delete = 'DELETE FROM current_selection' 
        classifieds_db.execute(delete)
    except DatabaseError: 
        item_text['text'] = ('Please select a category and item.') 
    connection.commit()
    query = 'insert into current_selection VALUES(?, ?, ?)'
    # Execute a query which lists the website, description & price of item in db
    try:
        classifieds_db.execute(query, [website_title, current_description_trans, current_price_trans]) 
    except NameError: 
        # If execution doesn't work, user hasn't selected category and item (this is a reminder for the user)
        item_text['text'] = ('Please select a category and item.') 
    except DatabaseError: 
        item_text['text'] = ('Please select a category and item.') 
    # Commit the changes to the database
    connection.commit()
    # Close the cursor and connection
    classifieds_db.close()
    connection.close() 

#-----------------------------CATEGORIES CONFIGURATION------------------------------#
 # Create label frame 
categories_label = LabelFrame(frame, text='Categories', **OPTIONS)
# Create three buttons 
# Variable for RadioButtons
v = IntVar() 
nl_button = Radiobutton(categories_label, text='Electronics @NL', font=Widget_font, variable=v, value=1, command=lambda:updating_the_category(1))
ebay_button = Radiobutton(categories_label, text='Cars @Ebay', font=Widget_font, variable=v, value=2, command=lambda:updating_the_category(2))
gumtree_button = Radiobutton(categories_label, text='Bags @Gumtree', font=Widget_font, variable=v, value=3, command=lambda:updating_the_category(3))
# Putting buttons into frames
nl_button.grid(padx=5, pady=5, row=1, sticky=W)
ebay_button.grid(padx=5, pady=5, row=2, sticky=W)
gumtree_button.grid(padx=5, pady=5, row=3, sticky=W)
# Use the grid geometry manager to manage frames
categories_label.grid(padx=MARGIN, pady=MARGIN, row=1, column=0, sticky=NSEW)


#------------------------------ITEMS CONFIGURATION----------------------------------#
# Create label frame 
item_label = LabelFrame(frame, text='Item', **OPTIONS)
# Create four radio button widgets 
item1 = Button(item_label, text='Latest', font=Widget_font, activebackground='#603E94', command=latest_selected)
item2 = Button(item_label, text='Second', font=Widget_font, activebackground='#603E94', command=second_selected)
item3 = Button(item_label, text='Third', font=Widget_font, activebackground='#603E94', command=third_selected)
# Putting radio buttons into frame
item1.grid(padx=5, pady=5, row=1, sticky=W)
item2.grid(padx=5, pady=5, row=2, sticky=W)
item3.grid(padx=5, pady=5, row=3, sticky=W)
# Use the grid geometry manager to manage frames
item_label.grid(padx=MARGIN, pady=MARGIN, row=1, column=1, sticky=NSEW)


#---------------------------OPTIONS CONFIGURATION----------------------------------#
 # Create label frame 
options_label = LabelFrame(frame, text='Options', **OPTIONS)
# Create Button for options labelframe
show_details = Button(options_label, text='Show details', font=Widget_font, command=go_to_website)
save_selection = Checkbutton(options_label, text='Save Selection', font=Widget_font, command=save_selection_in_db)
# Putting widget into frame
show_details.grid(padx=5, pady=5, column=0, row=1, sticky=W)
save_selection.grid(padx=20, pady=5, column=2, row=1, sticky=W)
# Use the grid geometry manager to manage frame
options_label.grid(padx=MARGIN, pady=MARGIN, row=2, column=0, columnspan=2, sticky=NSEW)


#-------------------------SELECTIONS CONFIGURATION------------------------------#
 # Create label frame 
selection_label = LabelFrame(frame, text='Selection', **OPTIONS)
# Create labels
price_text = Label(selection_label, text="$--.--", height=1, width=14, font=("Helvetica", 20, BOLD), bg='light grey')
item_text = Label(selection_label, text="No item description available\n", anchor='nw', height=8, width=27, font=("Helvetica", 15), bg='light grey', wraplength=220, justify="left")
source_name = Label(selection_label, text="Source: No Item selected", fg='black', font=("Helvetica", 10))
url_text = Label(selection_label, text="URL: No Item selected", fg='black', font=("Helvetica", 10))
# Putting labels into frame
price_text.grid(padx=5, pady=5, column=0, row=0, sticky=NW)
item_text.grid(padx=7, pady=2, column=2, row=0, columnspan=2, sticky=W)
source_name.grid(column=0, row=2, columnspan=3, sticky=W)
url_text.grid(column=0, row=3, columnspan=3, sticky=W)
# Use the grid geometry manager to manage frames
selection_label.grid(padx=MARGIN, pady=MARGIN, row=3, column=0, columnspan=2, sticky=NSEW)

#----------------MAIN LOOP-----------------#
v.set(1)
window.mainloop()