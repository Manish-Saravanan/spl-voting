import sqlite3
import base64

def GetPass(rollno):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''SELECT passcode FROM credentials WHERE RollNo = ?''', (rollno, ))
    c = cur.fetchone()
    if (c != None):
        return c[0]
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
    cur.execute("SELECT a.CandidateID, a.CandidateName FROM CandidateData a, ContestDetails b WHERE b.Category = ? AND a.CandidateID = b.CandidateID", (category, ))
    L =  cur.fetchall()
    return  L

def CastVote(Votes, categories, rollno):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    for i in categories:
        cur.execute("UPDATE ContestDetails SET NoOfVotes = NoOfVotes + 1 WHERE CandidateID = ?", (Votes[i], ))
    cur.execute("UPDATE credentials SET Voted = 1 WHERE RollNo = ?", (rollno, ))
    conn.commit()

def GetPath(candidateID):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''SELECT imageFilename FROM CandidateData WHERE CandidateID = ?''', (candidateID, ))
    c = cur.fetchone()
    if c!= None:    
        return c[0]
    else:
        return None

def hasVoted(rollno):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''SELECT Voted FROM credentials WHERE RollNo = ?''', (rollno, ))
    c = cur.fetchone()
    if (c != None):
        return bool(int(c[0]))
    else:
        return False
def addCandidate(candidateName, filename, category):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO CandidateData(CandidateName, ImageFilename) VALUES (?,?)", (candidateName, filename))
    cur.execute("INSERT INTO ContestDetails(CandidateID, Category, NoOfVotes) VALUES (LAST_INSERT_ROWID(), ?, 0)", (category, ))
    conn.commit()

def GetCandidateData():
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("SELECT a.CandidateID, a.CandidateName, b.Category FROM CandidateData a, ContestDetails b WHERE a.CandidateID = b.CandidateID")
    L =  cur.fetchall()
    return  L

def GetAdminPass():
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''SELECT passcode FROM adminCredentials''')
    c = cur.fetchone()
    if (c != None):
        return base64.b64decode(c[0])
    else:
        return None

def delCandidate(candidateID):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM CandidateData WHERE CandidateID = ?", (candidateID, ))
    cur.execute("DELETE FROM ContestDetails WHERE CandidateID = ?", (candidateID, ))
    conn.commit()

def isElectionOpen():
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''SELECT isOpen FROM ElectionOpen''')
    c = cur.fetchone()
    return bool(int(c[0]))

def ElectionClose():
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''UPDATE ElectionOpen SET isOpen = 0''')
    conn.commit()


def ElectionOpen():
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''UPDATE ElectionOpen SET isOpen = 1''')
    conn.commit()
