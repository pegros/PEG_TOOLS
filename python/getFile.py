#! /usr/bin/python3
import os, sys, re, requests

if (('-help' in sys.argv) or ('--help' in sys.argv) or ('-h' in sys.argv) or (len(sys.argv) != 3)):
    print('\n###################################\nHELP on ' + sys.argv[0] + '\n###################################')
    print('This tool enables to fetch a file given its ContentVersionId')
    print('###################################')
    print(sys.argv[0] + ' fileId fileName')
    print('###################################\n')
    sys.exit(0)

print('****** START **************************')
print('* Launching operation with fileId ' + sys.argv[1])
print('* and file name ' + sys.argv[2])

print('***************************************')
print('* fetching current org / user infos from SF CLI')
orgUserData = os.popen('sf org display user').read()
print('***************************************')
token = re.search("Access Token (.*) ",orgUserData).group(1)
print('* current token extracted: ' + token)
instance = re.search("Instance Url (.*) ",orgUserData).group(1)
print('* current instance extracted: ' + instance)

#token = os.system('sf org display user | grep "Access Token"')
#tokenLine = os.popen('sf org display user | grep "Access Token"').read()
#print('* current token infos fetched: ' + tokenLine)
#token = tokenLine.split(' ')[3]
#print('* current token extracted: ' + token)

#instanceLine = os.popen('sf org display user | grep "Instance Url"').read()
#print('* current instance infos fetched: ' + instanceLine)
#instance = instanceLine.split(' ')[3]
#print('* current instance extracted: ' + instance)
fileUrl = instance.replace('my.salesforce.com','file.force.com/sfc/servlet.shepherd/version/download/')
print('* file donwload Url init: ' + fileUrl)
print('***************************************')

print('* fetching file content')
filerequest = requests.get(fileUrl + sys.argv[1], headers={'Authorization': 'Bearer ' + token})
print('* file content fetched')
with open(sys.argv[2], 'wb') as fd:
    fd.write(filerequest.content)
fd.close()
print('****** END ****************************')