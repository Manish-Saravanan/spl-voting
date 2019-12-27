import sqlite3

def GetPass(rollno):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''SELECT passcode FROM credentials WHERE RollNo = ?''', (rollno, ))
    if cur.fetchone() != None:
        return cur.fetchone()[0]
    else:
        return None

def GetCat():
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT Category FROM ContestDetails")
    Lt =  cur.fetchall()
    L = []
    for i in Lt:
        L.append(i[0])
    return L

def GetCandidateNames(category):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("SELECT a.CandidateName FROM CandidateData a, ContestDetails b WHERE b.Category = ? AND a.CandidateID = b.CandidateID", (category, ))
    Lt =  cur.fetchall()
    L = []
    for i in Lt:
        L.append(i[0])
    return  L
