import sqlite3

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
    cur.execute("SELECT a.CandidateName FROM CandidateData a, ContestDetails b WHERE b.Category = ? AND a.CandidateID = b.CandidateID", (category, ))
    Lt =  cur.fetchall()
    L = []
    for i in Lt:
        L.append(i[0])
    return  L

def CastVote(Votes, categories, rollno):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    for i in categories:
        candidateName = Votes[i]
        cur.execute('''SELECT CandidateID FROM CandidateData WHERE CandidateName = ?''', (candidateName, ))
        c = cur.fetchone()
        candidateID = c[0]
        cur.execute("UPDATE ContestDetails SET NoOfVotes = NoOfVotes + 1 WHERE CandidateID = ?", (candidateID, ))
    cur.execute("UPDATE credentials SET Voted = 1 WHERE RollNo = ?", (rollno, ))
    conn.commit()

def GetPath(candidateName):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''SELECT imageFilename FROM CandidateData WHERE CandidateName = ?''', (candidateName, ))
    c = cur.fetchone()
    return c[0]

def hasVoted(rollno):
    conn = sqlite3.connect('election.db')
    cur = conn.cursor()
    cur.execute('''SELECT Voted FROM credentials WHERE RollNo = ?''', (rollno, ))
    c = cur.fetchone()
    if (c != None):
        return bool(int(c[0]))
    else:
        return False
