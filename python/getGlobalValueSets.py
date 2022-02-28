#! /usr/bin/python
import os, sys, json, re, shutil
import xml.etree.ElementTree as ET

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if (('-help' in sys.argv) or ('--help' in sys.argv) or ('-h' in sys.argv) or (len(sys.argv) != 3)):
    print('\n###################################\nHELP on ' + sys.argv[0] + '\n###################################')
    print('This tool enables to fetch all global value sets on an Org via SFDX metadata API.')
    print('It requires SFDX to be already installed and connected to the target Org, the user alias to use being provided as first parameter.')
    print('It generates a single CSV file containing all values for each Global Value Set available.')
    print('###################################')
    print(sys.argv[0] + ' sfdxAlias targetCSVfileName')
    print('###################################\n')
else:
    print('* Launching operation with alias ' + sys.argv[1])

    if os.path.exists('./tmpGVSget'):
        #os.system('rm -fr ./tmpGVSget')
        shutil.rmtree('./tmpGVSget')
    #os.system('mkdir ./tmpGVSget')
    os.mkdir('./tmpGVSget')
    #os.system('mkdir ./tmpGVSget/details')
    print('* Tmp dir (re)init')

    os.system('sfdx force:mdapi:listmetadata -m GlobalValueSet -u ' + sys.argv[1] + ' > ./tmpGVSget/gvs.json')
    print('* Global Value Set list fetched ')

    gvsFile = open('./tmpGVSget/gvs.json', 'r').read()
    if (len(gvsFile) > 0) :
        print('* GVS list loaded ')
        gvsFile = re.sub('(\w+)(: )','\"\\1\"\\2',gvsFile)
        gvsFile = re.sub('\'','\"',gvsFile)
        print('* GVS list corrected ')
        gvsList = json.loads(gvsFile)
        print('* GVS list parsed with ' + str(len(gvsList)) + ' items')

        pkgFile = open('./tmpGVSget/package.xml', 'w')
        pkgFile.write('<Package xmlns="http://soap.sforce.com/2006/04/metadata">\n')
        pkgFile.write(' <types>\n')
        for gvs in gvsList:
            pkgFile.write('  <members>' + gvs['fullName'] + '</members>\n')
        pkgFile.write('  <name>GlobalValueSet</name>\n')
        pkgFile.write(' </types>\n')
        pkgFile.write(' <version>51.0</version>\n')
        pkgFile.write('</Package>')
        print('* Package file ready')
        pkgFile.close()

        print('* Launching GVS details fetch')
        os.system('sfdx force:mdapi:retrieve -k ./tmpGVSget/package.xml -r ./tmpGVSget -u ' + sys.argv[1])
        print('* Unzipping package file')
        os.system('unzip ./tmpGVSget/unpackaged.zip -d ./tmpGVSget/')

        print('* Parsing GVS description files')
        csvFile = open('./' + sys.argv[2], 'w')
        csvFile.write('GlobalValueSet,FullName,Label,Default\n')
        for gvsFile in os.listdir('./tmpGVSget/unpackaged/globalValueSets'):
            print(' - ' + gvsFile)
            tree = ET.parse('./tmpGVSget/unpackaged/globalValueSets/' + gvsFile)
            root = tree.getroot()
            #print('  root: ' + root.tag + ' / ' + json.dumps(root.attrib))
            nameSpace = root.tag[:(root.tag.index('}')+1)]
            #print('  nameSpace: ' + nameSpace)
        
            masterLabel = root.find(nameSpace + 'masterLabel').text
            #print('  ' + masterLabel)
            customValues = root.findall(nameSpace + 'customValue')
            for customValue in customValues:
                fullName = customValue.find(nameSpace + 'fullName').text
                defaultV = customValue.find(nameSpace + 'default').text
                label = customValue.find(nameSpace + 'label').text
                lineV = masterLabel + ',' + fullName + ',' + label + ',' + defaultV + '\n'
                lineV = lineV.encode('UTF-8')   
                #print(lineV)
                csvFile.write(lineV)
        csvFile.close()
        print('* CSV file ready')
    else :
        print('* GVS list empty ')