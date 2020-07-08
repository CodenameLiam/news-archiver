#-----------------------------------------------------------
#
# Web Document Downloader
#
# This simple program is a stand-alone tool to download
# and save the source code of a given web document. For a
# particular URL, it downloads the corresponding web
# document as a Unicode character string and saves it to
# a file.  NB: This script assumes the source file is
# encoded as UTF-8.
#
# Q: Why not just access the web page's source code via
# favourite web browser (Firefox, Google Chrome, etc)?
#
# A: Because when a Python script requests a web document
# from an online server it may not receive the same file
# you see in your browser!  Many web servers generate
# different HTML/XML code for different clients.
#
# Worse, some web servers may refuse to send documents to
# programs other than standard web browsers.  If a Python
# script requests a web document they may instead respond
# with an "access denied" document!  In this case you'll
# just have to try another web page.
#

# Put your web page address here
url = 'http://feeds.bbci.co.uk/news/technology/rss.xml' # this web site is nice and doesn't block access
# url = 'http://www.wayofcats.com/blog/' # this web site is nasty and blocks access by Python scripts

# Import the function for opening online documents
from urllib.request import urlopen

# Open the web document for reading
web_page = urlopen(url)

# Read its contents as a Unicode string
web_page_contents = web_page.read().decode('UTF-8')

# Write the contents to a text file (overwriting the file if it
# already exists!)
html_file = open('download.html', 'w', encoding = 'UTF-8')
html_file.write(web_page_contents)
html_file.close()



