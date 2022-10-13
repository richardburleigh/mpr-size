import sqlite3
import bson
from hurry.filesize import size # Converts bytes to a Human-Readable format
import sys
import pandas as pd
import argparse

# Get size total size of an object, thanks to: https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python
def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

def processResults(results, limit):
    results = sorted(results,key=lambda sort: sort[3], reverse=True) # Sort by size
    results = pd.DataFrame(results, columns=['Type', 'Name', 'Size', 'Sort']) # Create data frame
    results = results.drop('Sort', axis=1) # Drop temporary sort column
    results = results.head(limit + 1) # Only export N rows of data
    return results

# Find nested keys in a dict, thanks to: https://stackoverflow.com/questions/9807634/find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists/19871956#19871956
def findkeys(node, kv):
    size = 0
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            size = get_size(node)
            yield node[kv], size
        for j in node.values():
            for x in findkeys(j, kv):
                yield x

def processMPR(args):
    # Open MPR file
    con = sqlite3.connect(args.input)
    cur = con.cursor()

    # Init variables
    count = 0
    imagedata = []
    overview = []
    unknown = []
    entities = []

    # Loop through Unit table and extract the contents
    print("Extracting data..")
    for row in cur.execute("SELECT  * FROM main.Unit;"):
        count = count + 1
        extracted = bson.BSON(row[6]).decode() # Extract BSON data from Contents
        try:
        	name = extracted['Name']
        except:
        	name = "N/A"
        totalsize = size(get_size(extracted))
        totalsize_sort = get_size(extracted)
        itemtype =  extracted['$Type']
        overview.append([itemtype, name, totalsize, totalsize_sort])
        # Extracted nested objects
        if 'Images' in extracted.keys():
            for image in extracted['Images']:
                try:
                	imagesize = get_size(image['Image'])
                	imagedata.append([itemtype, name + "/" + image['Name'].strip(), size(imagesize), imagesize])
                except:
                	pass

        elif 'Entities' in extracted.keys():
            ent = list(findkeys(extracted['Entities'],"Name"))
            for i in ent:
                if isinstance(i, tuple):
                    ename = list(i)[0]
                    esize = list(i)[1] 
                    while isinstance(ename, tuple):
                        ename = ename[0]
                    entities.append([itemtype, str(ename), size(esize), esize])

        else:
            for key in extracted.keys():
                if isinstance(extracted[key], dict):
                    for i in extracted[key].keys():
                        unknown.append([itemtype, name + "/" + key + "/" + i, size(get_size(extracted[key][i])), get_size(extracted[key][i])])
                else:
                    unknown.append([itemtype, name + "/" + key, size(get_size(extracted[key])), get_size(extracted[key])])

    print("Source data is ", count, " rows.")
    # Process results
    overview = processResults(overview, args.limit)
    imagedata = processResults(imagedata, args.limit)
    unknown = processResults(unknown, args.limit)
    entities = processResults(entities, args.limit)

    with pd.ExcelWriter(args.output.strip()) as writer:
        overview.to_excel(writer, sheet_name="Overview")
        imagedata.to_excel(writer, sheet_name="Images")
        entities.to_excel(writer, sheet_name="Entities")
        unknown.to_excel(writer, sheet_name="Uncategorized")
    print("Successfully exported to ", args.output)

def cli():
    parser = argparse.ArgumentParser("mpranalyzer")
    parser.add_argument("-i", "--input", help="MPR file to analyze", type=str, required=True)
    parser.add_argument("-o", "--output", help="Excel file to write to", type=str, required=True)
    parser.add_argument("-l", "--limit", help="Limit final report to N rows per sheet", type=int, default=100)
    args = parser.parse_args()
    processMPR(args)

if __name__ == '__main__':
    cli()
