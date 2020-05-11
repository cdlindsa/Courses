#!/usr/bin/env python3
#encoding=utf-8

import os
import csv
import re
import sys

columns = []
columns_final = []
dictfile = []
f = ''

def errors(n,param = ''):
    if n ==1:
        print("Error: No input file/incorrect filepath specified", file = sys.stderr)
        exit(1)
    elif n==2:
        print("Error: Output file", param, "is currently in use", file = sys.stderr)
        exit(1)
    elif n==3:
        print("Error: No output file specified. Defaulted output to 'output.csv'", file = sys.stderr)


def searches(csv_out):
    #--------------------------------------------------------------
    #Takes data from individual lines and puts them into a list,
    #then performs a search on the html commands of interest
    #--------------------------------------------------------------
    global f, columns, columns_final, dictfile
    tag = ''
    row,index = 0,0
    line_num, table_count = 1,1
    for line in f:
        #--------------------------------------------------------------
        #Data put into a list, splits based on "<>" and filters out None
        #--------------------------------------------------------------
        #print("LINE NUM: ", line_num)
        line = line.strip()
        temp =  re.split('(<[^>]*>)', line)
        temp.insert(0,tag)
        temp = list(filter(None, temp))
        csv_writer = csv.DictWriter(csv_out, fieldnames=columns_final)
        writer = csv.writer(csv_out)
        #print("BEFORE: ", temp)
        i = 0
        while i<len(temp):
            #--------------------------------------------------------------
            #List data is modified and non relevant elements are removed
            #--------------------------------------------------------------
            temp[i] = temp[i].strip()
            temp[i] = re.sub(' +', ' ', temp[i])
            #print("TEMP PROCESS, i: ", temp, i)
            if re.search(r'<(.*)>', temp[i],  re.DOTALL|re.IGNORECASE):
                #print("element contains <>: ", temp[i])
                if '<table' in temp[i] or '<tr' in temp[i] or '<td' in temp[i] or \
                    '<th' in temp[i] or '</table' in temp[i] or '</tr' in temp[i] or\
                    '</td' in temp[i] or '</th' in temp[i]:
                    #print("element being kept: ", temp[i])
                    i+=1
                else:
                    #print("element to be removed: ", temp[i])
                    temp.remove(temp[i])
            else:
                i += 1
        tag = ''
        # print("AFTER: ", temp, file = sys.stderr)
        for i in range(len(temp)):
            #--------------------------------------------------------------
            #Searching for html commands in the list,
            #Sent to row_builder to be put into dicts or printed to output
            #--------------------------------------------------------------
            if re.search(r'<table>', temp[i],  re.DOTALL|re.IGNORECASE):
                string = "TABLE %d: " %table_count
                # writer = csv.writer(csv_out)
                writer.writerow([string])
                table_count += 1
            elif re.search(r'</table>', temp[i],  re.DOTALL|re.IGNORECASE):
                #print("______END TABLE")
                row, index = 0,0
                for dictionary in dictfile:
                    # csv_writer = csv.DictWriter(csv_out, fieldnames=columns_final)
                    csv_writer.writerow(dictionary)
                writer = csv.writer(csv_out)
                writer.writerow([])
                #print(dictfile)
                dictfile = []
                columns = []
                columns_final = []
            elif re.search(r'<th>', temp[i],  re.DOTALL|re.IGNORECASE):
                #print("TH")
                try:
                    if not re.search(r'</th>', temp[i+1],  re.DOTALL|re.IGNORECASE):
                        #print(temp[i+1])
                        row_builder(temp[i+1],row,index)
                    else:
                        row_builder('',row,index)
                    index += 1
                except:
                    pass
            elif re.search(r'<td.*>', temp[i],  re.DOTALL|re.IGNORECASE):
                #print("TD")
                try:
                    if not re.search(r'</td>', temp[i+1],  re.DOTALL|re.IGNORECASE):
                        #print(temp[i+1])
                        row_builder(temp[i+1],row,index)
                    else:
                        row_builder('',row,index)
                    index += 1
                except:
                    pass
            elif re.search(r'<tr.*>', temp[i],  re.DOTALL|re.IGNORECASE):
                #print("TR______")
                row += 1
                index =0 
            elif re.search(r'</tr.*>', temp[i],  re.DOTALL|re.IGNORECASE):
                #print("______END TR")
                if row == 1: 
                    for key in columns_final:
                        dictfile   
                    csv_writer = csv.DictWriter(csv_out, fieldnames=columns_final)
                    csv_writer.writeheader()
            else:
                tag = temp[i]
        line_num += 1


def row_builder(line, row, index):
    #--------------------------------------------------------------
    #builds dictionaries based on values given from search function
    #--------------------------------------------------------------
    #print(line, row, index)
    global columns, columns_final, dictfile
    if row == 1:
        columns.append(line)
        if line != '':
            columns_final.append(line)
    else:
        if index == 0:
            dictfile.append({columns[index]:line})
        else:
            dictfile[row-2][columns[index]] = line

def main():
    global columns, columns_final, dictfile, f
    #--------------------------------------------------------------   
    #Test for stdin/stdout piping, if not looks at argv
    #--------------------------------------------------------------
    try: 
        if sys.stdin.isatty():
            f = open(sys.argv[1], 'r', encoding='utf-8-sig')
        else:
            f = sys.stdin
    except:
        errors(1)
    try:
        if sys.stdout.isatty() and sys.stdin.isatty():
            csv_out = str(sys.argv[2])
            with open(csv_out, 'w', encoding='utf-8-sig') as csvfile:
                searches(csvfile)
            csvfile.close()   
        elif sys.stdout.isatty():
            csv_out = str(sys.argv[1])
            with open(csv_out, 'w', encoding='utf-8-sig') as csvfile:
                searches(csvfile)
            csvfile.close() 
        else:
            csv_out = sys.stdout
            searches(csv_out)
            csv_out.close
    except IOError:
        errors(2,csv_out)
    except:
        #--------------------------------------------------------------
        #If no output file has been specified, default to 'output.csv'
        #--------------------------------------------------------------
        csv_out = "output.csv"
        try:
            with open(csv_out, 'w', encoding='utf-8-sig') as csvfile:
                searches(csvfile)
                errors(3)
        except IOError:
            errors(2,csv_out)
        csvfile.close()

    f.close()


if __name__ == "__main__":
    main()
