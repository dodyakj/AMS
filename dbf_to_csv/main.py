import os, sys
import csv
from dbfpy3 import dbf
from dbfread import DBF
import zipfile

def deldbf(filename):
    dbf_fn = './extract/' + filename[:-4]+ ".DBF"
    pft_fn = './extract/' + filename[:-4]+ ".FPT"
    try:
        os.remove(dbf_fn)
        print("File Removed!"+ filename[:-4] + ".DBF")
        if os.path.isfile(pft_fn):
            os.remove(pft_fn)
            print("File Removed!"+ filename[:-4] + ".FPT")
    except Exception as te:
        print (te)

with_extract = input('Press Y to Extract All on This Folder and for Convert DBF to CSV: ')
if with_extract == 'Y' or with_extract == 'y':
    for item in os.listdir('.'):
        if item.endswith('.zip'):
            with zipfile.ZipFile(item, 'r') as zip_ref:
                zip_ref.extractall('./extract')

    for dirpath, dirnames, filenames in os.walk('./extract'):
        for filename in filenames:
            if filename.endswith('.DBF'):
                print ("Converting %s to csv" % filename)
                csv_fn = './extract/' + filename[:-4]+ ".csv"
                csv_fn_hst = './extract/' + filename[:-4]+ "_hst.csv"
                with open(csv_fn, 'w', newline = '', encoding="utf8", errors='ignore') as f:
                    if os.path.exists('./extract/' + filename):
                        try :
                            out_csv = csv.writer(f, delimiter=",")
                            in_db = DBF('./extract/' + filename)
                            writer = csv.writer(f)
                            writer.writerow(in_db.field_names)
                            for record in in_db:
                                writer.writerow(list(record.values()))
                            try :
                                if in_db != False:
                                    for rec in in_db:
                                        if rec.deleted == False:
                                            out_csv.writerow(rec.fieldData)
                            except Exception as te:
                                print(te)
                        except Exception as te:
                            print(te)
                deldbf(filename)
                with open(csv_fn_hst, 'w', newline = '', encoding="utf8", errors='ignore') as f:
                    if os.path.exists('./extract/' + filename):
                        try :
                            out_csv = csv.writer(f, delimiter=",")
                            in_db = DBF('./extract/' + filename)
                            writer = csv.writer(f)
                            writer.writerow(in_db.field_names)
                            for record in in_db:
                                writer.writerow(list(record.values()))
                            try :
                                if in_db != False:
                                    for rec in in_db:
                                        if rec.deleted == False:
                                            out_csv.writerow(rec.fieldData)
                            except Exception as te:
                                print(te)
                        except Exception as te:
                            print(te)


