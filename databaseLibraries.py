import sqlite3
import base64
import os
from random import randint

def GetPass(rollno):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''SELECT passcode FROM credentials WHERE RollNo = ?''', (rollno, ))
    c = cur.fetchone()
    if (c != None):
        return base64.b64decode(c[0])
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
    imagepath = GetPath(candidateID)
    imagepath = "static/images/" + imagepath
    if os.path.exists(imagepath):
        os.remove(imagepath)
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

def GetResults(cat):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("SELECT a.CandidateName, b.NoOfVotes FROM CandidateData a, ContestDetails b WHERE a.CandidateID = b.CandidateID AND b.Category = ? ORDER BY b.NoOfVotes desc", (cat, ))
    L =  cur.fetchall()
    return  L

def ResetElection():
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    for file in os.listdir("static/images/"):
        if (file.lower().endswith(".png") or file.lower().endswith(".jpg") or file.lower().endswith(".jpeg")):
            os.remove("static/images/" + file) 
    cur.execute("DELETE FROM CandidateData")
    cur.execute("DELETE FROM ContestDetails")
    cur.execute("SELECT RollNo FROM Credentials")
    for candidate in cur.fetchall():
        cur.execute("UPDATE credentials SET passcode = ?, Voted = 0 WHERE RollNo = ?", (base64.b64encode(str(randint(100000, 999999))), candidate[0]))
    conn.commit()

def GetVoterDetails(cls):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("SELECT RollNo, passcode FROM credentials WHERE RollNo LIKE ?", (cls + "%", ))
    voters =  cur.fetchall()
    ret_voters = []
    for voter in voters:
        attrs = list(voter)
        attrs[1] = base64.b64decode(attrs[1])
        ret_voters.append(attrs)
    return ret_voters

def GetClassSection():
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT SUBSTR(rollno, 1, 3) FROM credentials")
    classes = cur.fetchall()
    return classes

def ChangePasswd(newpsswd):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("UPDATE adminCredentials SET passcode = ?", (base64.b64encode(newpsswd), ))
    conn.commit()

def SetupVoters(cls):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM credentials WHERE rollno LIKE ?", (cls + "%", ))
    for i in range(1, 37):
        rollNo = cls + "%02d"%i
        password = base64.b64encode(str(randint(100000, 999999)))
        cur.execute("INSERT INTO credentials(rollno, passcode, voted) VALUES(?, ?, '0')", (rollNo, password))
    conn.commit()

