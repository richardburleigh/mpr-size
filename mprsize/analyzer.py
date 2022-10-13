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

def processMPR(args):
    # Open MPR file
    con = sqlite3.connect(args.input)
    cur = con.cursor()

    # Init variables
    count = 0
    imagedata = []
    overview = []
    headers = ['Type', 'Name', 'Size', 'Sort']

    # Loop through Unit table and extract the contents
    print("Extracting data..")
    for row in cur.execute("SELECT  * FROM main.Unit ORDER BY length(Contents);"):
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
        # Check if object contains nested images and append them to the imagedata list
        if 'Images' in extracted.keys():
            for image in extracted['Images']:
                try:
                	imagesize = get_size(image['Image'])
                	imagedata.append([itemtype, name + "/" + image['Name'].strip(), size(imagesize), imagesize])
                except:
                	pass

    print("Source data is ", count, " rows.")
    overview = sorted(overview,key=lambda sort: sort[3], reverse=True) # Sort by size
    overview = pd.DataFrame(overview, columns=headers) # Create data frame
    overview = overview.drop('Sort', axis=1) # Drop temporary sort column
    overview = overview.head(args.limit + 1) # Only export N rows of data

    imagedata = sorted(imagedata,key=lambda sort: sort[3], reverse=True)
    imagedata = pd.DataFrame(imagedata, columns=headers)
    imagedata = imagedata.drop('Sort', axis=1)
    imagedata = imagedata.drop('Type', axis=1)
    imagedata = imagedata.head(args.limit + 1)

    with pd.ExcelWriter(args.output.strip()) as writer:
    	overview.to_excel(writer, sheet_name="Overview")
    	imagedata.to_excel(writer, sheet_name="Images")
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
