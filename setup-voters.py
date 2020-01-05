from databaseLibraries import SetupVoters
import sys
import sqlite3

cls = sys.argv[1]
try:
    SetupVoters(cls)
except sqlite3.IntegrityError:
    print("Class and section already setup")
