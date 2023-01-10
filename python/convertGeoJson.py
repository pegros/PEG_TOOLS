#! /usr/bin/python3
import json
import os
import sys

if (('-help' in sys.argv) or ('--help' in sys.argv) or ('-h' in sys.argv) or (len(sys.argv) != 4)):
    print('\n###################################\nHELP on ' + sys.argv[0] + '\n###################################')
    print('This tool enables to rework a geoJson file to make it compatible with CRM Analytics.')
    print('It duplicates an IP Property of each geoJson feature in a source file as a direct ID field in a target file.')
    print('###################################')
    print(sys.argv[0] + ' idProperty sourceFile targetFile')
    print('###################################\n')
else:
    print('* Launching operation with idProperty ' + sys.argv[1])

    if not(os.path.exists(sys.argv[2])):
        print('⚠️ Processing failure --> Source file "' + sys.argv[2] + '" not found.')
        sys.exit();
    
    print('* opening source file ' + sys.argv[2])
    
    # standard geojson file
    f = open(sys.argv[2], 'r')
    json_contents = json.loads(f.read())
    features = json_contents["features"]
    for iter in features:
        iter["id"] = iter["properties"][sys.argv[1]]
    json_contents["features"] = features
    print('* #features reworked ', len(features))

    # Normalized geojson for CRM Analytics map
    out_file = open(sys.argv[3], "w")
    out_file.write(json.dumps(json_contents))
    out_file.close()
    print('* target file written ' + sys.argv[2])
