#!/usr/bin/env python3 
# EBI GWAS catalogParser.py

from functools import cmp_to_key
import csv
from itertools import islice
from os import error
import os

DELETE=False

# EBI GWAS parserFunction.py

from functools import cmp_to_key
import csv
from itertools import islice
from os import error


def parser(sessionID="", debug=True):
    holder = []
    SNPs = []
    errors = 0
    lineNumber = 0
    testLineNumber =0
    totalCorrect = 0
    totalIncorrect = 0

    try:
        with open(f'Genome/CHR-1{sessionID}.fa') as te:
            te.readline()
            line = te.readline()
            lineNumber = len(line.strip())

    except:
        print("Will Fail, Refrence Not Present!")

    try:
        with open(f'uploads/CHR-1{sessionID}.fa') as te:
            te.readline()
            line = te.readline()
            testLineNumber = len(line.strip())

    except:
        print("Will Fail, Test Data Not Present!")

    finally:
        te.close()

    superLargeMemory = []
    superLargeTestMemory = []
    try:
        for x in range(1, 23):

            with open("Genome/CHR-{0}{1}.fa".format(x, sessionID)) as te:
                z = te.readlines()
                superLargeMemory.append(z)
                if debug:
                    print("read refrence {}".format(x))
            te.close()
    except:
        pass

    try:
        for x in range(1, 23):

            with open("uploads/CHR-{0}{1}.fa".format(x, sessionID)) as te:
                z = te.readlines()
                superLargeTestMemory.append(z)
                if debug:
                    print("read test {}".format(x))
            te.close()
    except:
        pass

    incorrectDicts = []

    with open("EBIGWAS.tsv") as fd:
        rd = csv.DictReader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            holder.append(row)
            #Scan DNA
            try:
                z = superLargeMemory[int(row.get("CHR_ID", 0))-1][int(int(row.get("CHR_POS")) / lineNumber)][int(row.get("CHR_POS")) % lineNumber]
                y = superLargeTestMemory[int(row.get("CHR_ID", 0))-1][int(int(row.get("CHR_POS")) / lineNumber)][int(row.get("CHR_POS")) % lineNumber]

                
                if(z == y):
                    totalCorrect += 1
                else:
                    totalIncorrect += 1
                    incorrectDicts.append(row)

            except:
                errors += 1
    
    if errors > 30000:
        print("High error count, check sequence submitted!")
    if debug:
        print("Errors: {}".format(errors))
        print("Unmatched Pairs (Difference from Reference): {}".format(totalIncorrect))
    # for item in incorrectDicts:
    #     print(item)

    if DELETE:
        try:
            os.remove("uploads/CHR-1.fa")
            os.remove("uploads/CHR-2.fa")
            os.remove("uploads/CHR-3.fa")
            os.remove("uploads/CHR-4.fa")
            os.remove("uploads/CHR-5.fa")
            os.remove("uploads/CHR-6.fa")
            os.remove("uploads/CHR-7.fa")
            os.remove("uploads/CHR-8.fa")
            os.remove("uploads/CHR-9.fa")
            os.remove("uploads/CHR-10.fa")
            os.remove("uploads/CHR-11.fa")
            os.remove("uploads/CHR-12.fa")
            os.remove("uploads/CHR-13.fa")
            os.remove("uploads/CHR-14.fa")
            os.remove("uploads/CHR-15.fa")
            os.remove("uploads/CHR-16.fa")
            os.remove("uploads/CHR-17.fa")
            os.remove("uploads/CHR-18.fa")
            os.remove("uploads/CHR-19.fa")
            os.remove("uploads/CHR-20.fa")
            os.remove("uploads/CHR-21.fa")
            os.remove("uploads/CHR-22.fa")
        except:
            pass



    return [errors, incorrectDicts]

if __name__ == "__main__":
    x, y = parser(debug=True, sessionID="")
    print(x, y)

