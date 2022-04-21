#! /usr/bin/python3
import os, sys, json, re, shutil

#############################
# UTILITIES
#############################

# Utility Method to fetch files with a certain extension in a directory, returning a dictionary of them
def getFiles(dirName,extension):
    print('** getting ' + extension + ' files in directory ' + dirName)
    fileDictionary = {}
    for iterFile in os.listdir(dirName):
        if ((os.path.isfile(dirName + '/' + iterFile)) and (iterFile.endswith(extension))):
            print(' + ' + iterFile)
            fileDictionary[os.path.splitext(iterFile)[0]] = dirName + '/' + iterFile
        else:
            print(' - ' + iterFile)
    print('** returning ')
    print(fileDictionary)
    return fileDictionary

# Utility Method to fetch and stringify the content of a set of files returning a new dictionary of them
def getRefData(dictionary):
    print('** getting reference content')
    dataDictionary = {}
    for iter in dictionary:
        print('*** processing file ' + iter)
        file = open(dictionary[iter],mode='r')
        fileContent = file.read()
        file.close()
        dataDictionary[iter] = fileContent
    print('** returning ')
    print(dataDictionary)
    return dataDictionary

# Utility Method to merge a file
def mergeData(sourceFile,targetFile,refData):
    print('** merging data in ' + targetFile)
    file = open(sourceFile,mode='r')
    fileContent = file.read()
    file.close()
    print('   content loaded')
    
    tokens = set(tokenRE.findall(fileContent))
    print('   tokens found')
    print(tokens)
    
    for tokenIter in tokens:
        print('*** replacing token ' + tokenIter)
        if tokenIter in refData:
            print('*** token data found')
            fileContent = fileContent.replace('<%%%>' + tokenIter + '</%%%>', refData[tokenIter])
        else:
            print('*** token ' + tokenIter + ' not found in reference data')
            raise Exception('No reference data for token ' + tokenIter + ' found in file ' + sourceFile)
    print('*** all tokens processed ')
        
    file = open(targetFile,mode='w')
    file.write(fileContent)
    file.close()
    print('*** target file generated ' + targetFile)
    return


#############################
# MAIN EXEC LOGIC
#############################

tokenRE = re.compile('<%%%>(.+?)</%%%>')

if (('-help' in sys.argv) or ('--help' in sys.argv) or ('-h' in sys.argv) or (len(sys.argv) != 3)):
    print('\n###################################\nHELP on ' + sys.argv[0] + '\n###################################')
    print('This tool enables to parse dataflow file templates and replace the merge tokens found by the content of reference files, saving the result in a target directory.')
    print('Template and reference files are assumed to be located in a "source" directory with "templates" and "references" sub-directories.')
    print('"Source" and "Target" directories need to be existing.')
    print('###################################')
    print(sys.argv[0] + ' sourceDir targetDir')
    print('###################################\n')
elif not os.path.exists(sys.argv[1]):
    print('### Source directory not found (' + sys.argv[1] + ')! ###')
    sys.exit()
elif not os.path.exists(sys.argv[1] + '/templates'):
    print('### Templates sub-directory not present in Source directory (' + sys.argv[1] + '/templates)! ###')
    sys.exit()
elif not os.path.exists(sys.argv[1] + '/references'):
    print('### References sub-directory not present in Source directory (' + sys.argv[1] + '/references)! ###')
    sys.exit() 
elif  not os.path.exists(sys.argv[2]):
    print('### Target directory not found (' + sys.argv[2] + ')! ###')
    sys.exit() 
else:
    print('***********************************************************************')
    print('* Launching operation merging files in ' + sys.argv[1] + ' into ' + sys.argv[2])
    print('***********************************************************************')
        
    print('* Template files')
    templatesDic = getFiles(sys.argv[1] + '/templates', '.xml')
    #print(templatesDic)
          
    print('* Reference files')
    referencesDic = getFiles(sys.argv[1] + '/references', '.xml')
    #print(referencesDic)
    print('* Reference data')
    refdataDic = getRefData(referencesDic)
    #print(refdataDic)
    
    print('* Existing Target files')
    targetDic = getFiles(sys.argv[2], '.xml')
    #print(targetDic)
    
    print('***********************************************************************')
    print('* Initialisation done')
    print('***********************************************************************')

    for iter in templatesDic:
        print('* Merging template ' + iter)
        targetFile = sys.argv[2] + '/' + iter + '.xml'
        if iter in targetDic:
            print('  replacing ' + targetFile)
        else:
            print('  initialising ' + targetFile)
        mergeData(templatesDic[iter], targetFile, refdataDic)
        print('\n')
        
    print('***********************************************************************')
    print('* Operation complete')
    print('***********************************************************************')