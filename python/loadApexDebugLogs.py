#! /usr/bin/python3
import os, sys

if (('-help' in sys.argv) or ('--help' in sys.argv) or ('-h' in sys.argv) or (len(sys.argv) != 3)):
    print('\n###################################\nHELP on ' + sys.argv[0] + '\n###################################')
    print('This tool enables to fetch all debug logs of a connected SFDX user from an Org')
    print('###################################')
    print(sys.argv[0] + ' sfdxAlias targetDir')
    print('###################################\n')
else:
    print('* Launching debug log files fetch with alias ' + sys.argv[1])
    
    os.system('sfdx force:data:soql:query -u ' +  sys.argv[1] + ' -q \'select Id from ApexLog order by StartTime desc limit 2000\' > ' + sys.argv[2] + '/tmp.csv')
    f = open(sys.argv[2] + '/tmp.csv', 'r')
    all_lines = f.readlines()
    lines = [] if len(all_lines) <= 3 else all_lines[2:-1]
    lineCount = 1
    for line in lines:
        stripped_line = line.rstrip()
        print('   Fetching log #' + lineCount + ' with ID ' + stripped_line)
        os.system('sfdx force:apex:log:get -u ' +  sys.argv[1] + ' -d ' + sys.argv[2] + ' -i ' + stripped_line)
        lineCount += 1                                       
    print('* Operation completed with #files fetched ' +  (lineCount - 1))
    f.closed