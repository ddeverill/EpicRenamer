from jira import JIRA
import getpass

def connect_jira(jira_server, jira_user, jira_password):
    print "Connecting to Jira!"
    try:
        jira_options = {'server' : jira_server}
        jira = JIRA(options=jira_options, basic_auth=(jira_user, jira_password))
        return jira
    except Exception,e:
        print "Failed to connect to jira"
        print e
        return None

def determine_status(listOfEpics):
    if bool(listOfEpics) is False:
        return "Empty"
    for i in listOfEpics:
        #print 'Starting the determination with %s' % (i)
        #Removing the backlog option, since it's the default for all new things
        #if isItOpen(listOfEpics) == True: return "Backlog"
        #print 'Checking to see if its closed'
        if isItClosed(listOfEpics) == True:
            return "Closed"
        #print 'Checking to see if its in QA'
        if isItInQA(listOfEpics) == True:
            return "InQA"
        #print 'Checking to see if its in progress'
        if isItInProgress(listOfEpics) == True:
            return "In Progress"
    return "No Status Found"

def isItOpen(listOfEpics):
    #Check to see if they're all open
    tempStatus = True
    for i in listOfEpics:
        #It's actually backlog
        if (str(i.fields.status) != 'Open' and tempStatus == True): 
            return False
    return tempStatus

def isItClosed(listOfEpics):
    #Check to see if they're all closed
    tempStatus = True
    for i in listOfEpics:
        if (str(i.fields.status) == 'Closed' and tempStatus != False): tempStatus = True
        else:
            return False
    return tempStatus

def isItInQA(listOfEpics):
    #Check to see if it's In QA
    tempStatus = True
    for i in listOfEpics:
        if (str(i.fields.status) == "Resolved" or str(i.fields.status) == "Closed" and tempStatus != False): tempStatus = True
        else:
            return False
    return tempStatus

def isItInProgress(listOfEpics):
    #Check to see if it's In Progress
    tempStatus = True
    for i in listOfEpics:
        if (str(i.fields.status) == "Open" or str(i.fields.status) == "In Progress" or str(i.fields.status) == "Blocked" or str(i.fields.status) == "Code Review" or str(i.fields.status) == "Resolved" or str(i.fields.status) == "Closed" and tempStatus != False): tempStatus = True
        else:
            return False
    return tempStatus

username = input('Enter your Jira username (in quotes): ')
password = getpass.getpass('Password: ')

jira_connection = connect_jira("https://jira.hulu.com", username, password)

print "Connected to Jira!"

projects = jira_connection.projects()

epics_in_HUTV = jira_connection.search_issues('assignee = lynda.gusick and project = HUTV and Status != closed')

for v in epics_in_HUTV:
    #Get the current status of the Epic
    print v
    tempStatus = v.fields.status
    tempString = str(v)
    #Get a collection of all the stories attached to the epic
    stories_in_epic = jira_connection.search_issues('"Epic Link" = %s' % (tempString))
    print determine_status(stories_in_epic) 