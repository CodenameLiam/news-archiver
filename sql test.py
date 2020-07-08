# Import the SQLite functions.
from sqlite3 import *

# Import the date and time function.
from datetime import datetime

#Create a connection to the database.
connection = connect(database = 'event_log.db')

#Get a pointer into the database.
eventLogDB = connection.cursor()

eventNumber = 0
eventNumber = eventNumber + 1
query = "SELECT max(Event_Number) FROM Event_Log"

eventLogDB.execute(query)

results = eventLogDB.fetchall()

print(results[0][0])

connection.commit()
eventLogDB.close()
connection.close()
    
