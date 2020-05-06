# spl-voting
Tool for the school to conduct election for school pupil leaders.

## Voting software Capabilities:

* At least 10 people can vote simultaneously.
* The consolidated results will be available in a single page.
* Only the authorized people can perform activities related to managing elections.
* Voters’ privacy will be maintained.  

## Installation:
1.	Download the zip file containing the software and extract it.
2.	Install Python 3.7 and pip 3. (refer: https://docs.python.org/3/using/index.html) 
3.	Run the following command to create entries for voters of each class and section
```
python setup-voters.py <class>

  where class is the class and section the voters are from. It should be in the format 06A. Here 06 refers to the class and A refers to the section.

  Example:
  python setup-voters.py 07B (for class 7 and section B)

  This command creates 40 voters’ entry for the given class and section. This command should be repeated for each class and section eligible for voting.
```

4.	The following command can be run in a similar manner to delete voters in that class.
```
python delete-voters <class>
```

5.	Run the following command every time you want to start using the application.
```
python StartElection.py
```

## Usage:
There are three phases in the application. 
* The first is the pre-election phase when candidates can be added/deleted.    
* The second phase is when the election happens.    
* The third is the post-election phase when results can be viewed. 
You can go only in one direction; you cannot go backwards.   
### Admin:
1.	In http://\<HostIP\>/login page, click on login as Admin.
2.	Use the admin credentials to login.   
*	View voter credentials   
        Click on the ‘View voter credentials’ tab to view the Login ID and password of the voters.   
* Change password   
        In the ‘Change password’ tab, enter your old password, new password and confirm your new password.   
#### Phase 1   
* Adding candidates:   
1.	In the ‘Edit candidates’ tab, fill in all the data and click on Add.   
2.	If you want to delete a candidate click on the delete icon corresponding to the candidate.   
* Move to next phase   
        Click on ‘Open voting’ tab and enter admin password to move to second phase.   
#### Phase 2   
The total number of voters who have voted so far is displayed on the top.   
* View candidates   
        Click on the ‘View candidates’ tab. (The candidates can only be viewed and not edited.)   
* Move to next phase   
        Click on ‘Close voting’ tab and enter admin password to move to post-election phase.   
#### Phase 3   
* View results   
        Click on ‘View results’ tab to view results.   
* Move to next phase   
        Click on ‘Reset’ tab and enter admin password to move to pre-election phase. This will set the data back to defaults for the next year's election  
