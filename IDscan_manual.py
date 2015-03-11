import requests
import os
import datetime
import csv
import xml.etree.ElementTree as etree
from colorama import init, Fore

if os.name == 'nt':
    import msvcrt


def getMemberData():
    URL = '...'
    response = requests.get(URL)
    root = etree.fromstring(response.content)

    # populate members list
    members = []
    for child in root:
        temp = []
        temp.append(child.find('FirstName').text)
        temp.append(child.find('LastName').text)
        if (child.find('UniqueID').text is None):
            temp.append('UniqueID not supplied')
        else:
            temp.append(child.find('UniqueID').text)
        # check for members without email address
        if (child.find('EmailAddress').text is None):
            temp.append('EmailAddress not supplied')
        else:
            temp.append(child.find('EmailAddress').text)
        members.append(temp)

    print 'Membership Data Parsed.'
    return members


def parseCSVdata():
    attendees = []
    with open('data.csv', 'rbU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', dialect=csv.excel_tab)
        for row in reader:
            attendee = []
            attendee.append(row[0])
            attendee.append(row[1])
            attendee.append(row[2])
            # LName, FName, ID Number
            attendees.append(attendee)
    return attendees


def matchID(members, IDnumber):
    for member in members:
        if member[2] == IDnumber:
            if mode.lower() == "api":
                print Fore.GREEN, member[0].title(), member[1].title(), \
                    member[2].title(), Fore.RESET, len(attendees)+1
            elif mode.lower() == "csv":
                print Fore.GREEN, member[1].title(), member[0].title(), \
                    member[2], Fore.RESET, len(attendees)+1

            scanTime = datetime.datetime.now().strftime('%H:%M')
            member.append(scanTime)
            member.append('\n')
            return member

    else:
        if mode.lower() == "api":
            print Fore.RED, IDnumber + ' is not a member', Fore.RESET
        elif mode.lower() == "csv":
            print Fore.RED, IDnumber + ' is not an attendee', Fore.RESET
        return 1


# colorama init
init()
attendees = []
fileName = datetime.datetime.now().strftime('%Y-%m-%d#%H-%M-%S.txt')
d = open(fileName, 'a')
print "MANUAL ID INPUT ONLY"
print "Hi there EngSoc minion!"
print "To refresh the member database, press 'r' anytime"
print "To input an ID number manually, press '1' anytime"
print "EngSoc is Love, EngSoc is Life. \n"

mode = raw_input("API or CSV? ")
if mode.lower() == "api":
    membersList = getMemberData()
    print "Tell Michael we have", len(membersList), "members"
elif mode.lower() == "csv":
    membersList = parseCSVdata()
    print "Tell Michael we have", len(membersList), "attendees"
else:
    exit()


try:
    while (True):
        if msvcrt.kbhit():
            huminput = msvcrt.getch()
            if huminput == "r":
                    membersList = getMemberData()
            elif huminput == "n":
                num = len(attendees)
                if num == 1:
                    print "1 person"
                else:
                    print num, "people"
            elif huminput == "1":
                manualID = raw_input("Enter ID number: ")
                attendee = matchID(membersList, manualID)
                if attendee != 1:
                        attendees.append(attendee)
                        d.write(', '.join(attendee))
finally:
    d.close()
