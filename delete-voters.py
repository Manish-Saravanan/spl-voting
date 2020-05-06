from databaseLibraries import DeleteVoters
import sys
import sqlite3

cls = sys.argv[1]
try:
    DeleteVoters(cls)
except:
    print("An error occured. Please try again")
