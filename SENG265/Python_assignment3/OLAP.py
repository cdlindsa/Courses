#!/usr/bin/env python3
#encoding=utf-8

import argparse
import os
import sys
import csv

dict_file = {}
dict_data = []
columns = []
filename = ''
gb_capped = False
gb_capped_heading = {}
gb_capped_dict = {}

def ErrorPrints(num, line, call, value):
    global filename	
    if num == 1:			
        print("Error: "+filename+": "+str(line)+": can’t compute "+call+" on non-numeric value ‘"+str(value)+"‘\n", file=sys.stderr)
    elif num == 2:
        print("Error: "+filename+": more than 100 non-numeric values found in aggregate column ‘"+call+"'\n", file=sys.stderr)
        exit(7)
    elif num == 3:
        print("Error: "+filename+": " + call + " has been capped to 20 distinct values\n", file=sys.stderr)
    elif num == 4:
        print("Error: "+filename+": no "+ call + " argument with the name " + value + " found\n", file=sys.stderr)
        exit(6)
    elif num == 5:
        print("Error: "+filename+": I/O error", file=sys.stderr)  
        exit(6)
    elif num == 6:
        print("Error: "+filename+": incorrect value (non-integer) in "+ call + " specified\n", file=sys.stderr)
        exit(6)      		

def clear_dicts():
    global dict_data, dict_file, columns
    dict_file = {}
    dict_data = []
    columns = []


def arg_min(num_field, key = ''):
    global dict_data, columns
    final = 'NaN'
    error_count = 0
    keyname = "min_" + str(num_field)
    columns.append(keyname)   
# Min no Group_by 
    if key == '':
        try:
            for value in dict_file[num_field]:
                try:
                    if value != '':
                        temp = float(value)
                        if final == 'NaN':
                            final = temp
                        else:
                            if temp < final:
                                final = temp           
                except:
            	    ErrorPrints(1,dict_file[num_field].index(value),"--min",value)            	
            	    error_count += 1
            	    if error_count>100:
            		    ErrorPrints(2,0,"--min",0)      
            if final != 'NaN':
                if dict_data == []:
                    dict_data = [{keyname:final}]
                else:
                    for dictionary in dict_data:
                        dictionary[keyname] = final
        except:
        	ErrorPrints(4,0,"--min",num_field)			
#Group_by min
    else:
        for dictionary in dict_data:
            dictionary[keyname] = 'NaN'
            try:
                for index in range(len(dict_file[key])):
                    try:
                        if dictionary[key] == dict_file[key][index]:
                            temp = float(dict_file[num_field][index])
                            if dictionary[keyname] == 'NaN':
                                dictionary[keyname] = temp
                            elif temp < dictionary[keyname]:
                                dictionary[keyname] = temp
                    except:
                        ErrorPrints(1,index,"--min",dict_file[num_field][index])
                        error_count += 1
                        if error_count>100:
                            ErrorPrints(2,0,"--min",0)
            except:
                ErrorPrints(4,0,"--min",num_field)
    return


def arg_max(num_field, key = ''):
    global dict_data, columns
    keyname = "max_" + str(num_field)
    columns.append(keyname)    
    final = 'NaN'
    error_count = 0
# Max no Group_by
    if key == '':
        try:
            for value in dict_file[num_field]:
                try:
                    if value != '':
                        temp = float(value)
                        if final == 'NaN':
                            final = temp
                        else:
                            if temp > final:
                                final = temp
                except:
                    ErrorPrints(1,dict_file[num_field].index(value),"--max",value)
                    error_count += 1
                    if error_count>100:
                        ErrorPrints(2,0,"--max",0)     
            if final != 'NaN':
                if dict_data == []:
                    dict_data = [{keyname:final}]
                else:
                    for dictionary in dict_data:
                        dictionary[keyname] = final
        except:
            ErrorPrints(4,0,"--max",num_field)
#Group by(max)
    else:
        keyname = "max_" + str(num_field)
        for dictionary in dict_data:
            dictionary[keyname] = 'NaN'
            try:
                for index in range(len(dict_file[key])):
                    try:
                        if dictionary[key] == dict_file[key][index]:
                            temp = float(dict_file[num_field][index])
                            if dictionary[keyname] == 'NaN':
                                dictionary[keyname] = temp
                            elif temp > dictionary[keyname]:
                                dictionary[keyname] = temp
                    except:
                        ErrorPrints(1,index,"--max",dict_file[num_field][index])
                        error_count += 1
                        if error_count>100:
                            ErrorPrints(2,0,"--max",0)
            except:
                ErrorPrints(4,0,"--max",num_field)
    return


def arg_mean(num_field, key = ''):
    global dict_data, columns
    final = 'NaN'
    error_count = 0
    count = 0
    keyname = "mean_" + str(num_field)
    columns.append(keyname)
# Mean no Group_by
    if key == '':
        try:               
            for value in dict_file[num_field]:
                try:
                    if value != '':
                        temp = float(value)
                        if final == 'NaN':
                            final = temp
                        else:
                            final+= temp
                        count += 1
                except:
                    ErrorPrints(1,dict_file[num_field].index(value),"--mean",value)
                    error_count += 1
                    if error_count>100:
                        ErrorPrints(2,0,"--mean",0)	     
            if final != 'NaN':
                final = final/count
                if dict_data == []:
                    dict_data = [{keyname:final}]
                else:
                    for dictionary in dict_data:
                        dictionary[keyname] = final
        except:
            ErrorPrints(4,0,"--mean",num_field)  			                 
#Group_by mean    
    else:
        for dictionary in dict_data:
            dictionary[keyname] = 'NaN'
            try:
                for index in range(len(dict_file[key])):
                    try:
                        if dictionary[key] == dict_file[key][index]:
                            temp = float(dict_file[num_field][index])
                            count+=1
                            if dictionary[keyname] == 'NaN':
                                dictionary[keyname] = temp
                            else:
                                dictionary[keyname] += temp
                    except:
                        ErrorPrints(1,index,"--mean",dict_file[num_field][index])
                        error_count += 1
                        if error_count>100:
                            ErrorPrints(2,0,"--mean",0)
            except:
                ErrorPrints(4,0,"--mean",num_field)
            if count!= 0:
                dictionary[keyname] = dictionary[keyname]/count
    return


def arg_sum(num_field, key =''):
    global dict_data
    final = 'NaN'
    error_count = 0
    keyname = "sum_" + str(num_field)
    columns.append(keyname)
# Sum no Group_by
    if key == '':
        try:           
            for value in dict_file[num_field]:
                try:
                    if value != '':
                        temp = float(value)
                        if final == 'NaN':
                            final = temp
                        else:
                            final+= temp
                except:
                    ErrorPrints(1,dict_file[num_field].index(value),"--sum",value)
                    error_count += 1
                    if error_count>100:
                        ErrorPrints(2,0,"--sum",0)
            if final != 'NaN':
                if dict_data == []:
                    dict_data = [{keyname:final}]
                else:
                    for dictionary in dict_data:
                        dictionary[keyname] = final
        except:
        	ErrorPrints(4,0,"--sum",num_field)
#Group_by sum    
    else:
        keyname = "sum_" + str(num_field)
        for dictionary in dict_data:
            dictionary[keyname] = 'NaN'
            try:
                for index in range(len(dict_file[key])):
                    try:
                        if dictionary[key] == dict_file[key][index]:
                            temp = float(dict_file[num_field][index])
                            if dictionary[keyname] == 'NaN':
                                dictionary[keyname] = temp
                            else:
                                dictionary[keyname] += temp
                    except:
                        ErrorPrints(1,index,"--sum",dict_file[key][index])
                        error_count += 1
                        if error_count>100:
                            ErrorPrints(2,0,"--sum",0)
            except:
        	    ErrorPrints(4,0,"--sum",num_field)
    return


def arg_count(key = ''):
    global dict_data, columns, gb_capped
    keyname = "count"
    columns.append(keyname)
# Count no Group_by    
    if key == '':
        keylist = list(dict_file.keys())
        if dict_data == []:
        	dict_data = [{keyname:len(dict_file[keylist[0]])-1}]
        else:
        	for dictionary in dict_data:
        		dictionary[keyname] = len(dict_file[keylist[0]])-1        
# Group_by count    
    else:
        try: 
            for dictionary in dict_data:
                count = 0
                for index in range(len(dict_file[key])):
                    if dictionary[key] == dict_file[key][index]:
                        count+=1
                dictionary[keyname] = count
        except:
            ErrorPrints(4,0,"--count",key)
    return


def arg_top(number, cat_field, key = ''):
    global dict_data,columns
    temp = {}
    string = ''
    if int(number)==20:
        keyname = "top_" + str(cat_field) + "_capped"
    else:
        keyname = "top_" + str(cat_field)
    columns.append(keyname)
# Top k no Group_by    
    if key == '':
        try:
            for index in range(len(dict_file[cat_field])):
                if dict_file[cat_field][index] in temp:
                    temp[dict_file[cat_field][index]] += 1                		
                elif dict_file[cat_field][index] != '':
                    temp[dict_file[cat_field][index]] = 1                						
            temp_outlist = []
        except:
            ErrorPrints(4,0,"--top",cat_field)
        for k,v in temp.items():
        	temp_outlist.append(v)             
        temp_outlist = sorted(temp_outlist, reverse=True)
        temp_keylist = list(temp.keys())
        temp_vallist = list(temp.values())            
        count = 0
        for item in temp_outlist:
        	if item in temp_vallist and count < int(number):
        		if count < int(number)-1:          	
        			string += temp_keylist[temp_vallist.index(item)]+": "+str(item)+","
        		else:
        			string += temp_keylist[temp_vallist.index(item)]+": "+str(item)
        		count +=1                    
        if dict_data == []:
        	dict_data = [{keyname:string}]
        else:
        	for dictionary in dict_data:
        		dictionary[keyname] = string
#Group_by Top K
    else:
        try:       
            for dictionary in dict_data:
                for index in range(len(dict_file[key])):
                    if dictionary[key] == dict_file[key][index]:
                        if dict_file[cat_field][index] in temp:
                            temp[dict_file[cat_field][index]] += 1                		
                        else:
                            temp[dict_file[cat_field][index]] = 1                						
                temp_outlist = []
                for k,v in temp.items():
                    temp_outlist.append(v)             
                temp_outlist = sorted(temp_outlist, reverse=True)
                temp_keylist = list(temp.keys())
                temp_vallist = list(temp.values())            
                count = 0
                for item in temp_outlist:
                    if item in temp_vallist and count < int(number):
                        if count < int(number)-1:          	
                            string += temp_keylist[temp_vallist.index(item)]+": "+str(item)+","
                        else:
                            string += temp_keylist[temp_vallist.index(item)]+": "+str(item)
                    count +=1              
                dictionary[keyname] = string            
                temp = {}
                string = ''
        except:
            ErrorPrints(4,0,"--top",key)
    return


def arg_group_by(cat_field, args):
    global dict_data, columns, gb_capped, gb_capped_dict, gb_capped_heading
    columns = [str(cat_field)]
    dict_data = [{cat_field: ''}]
    try:
        for x in dict_file[cat_field]:
                if {cat_field: x} not in dict_data and x != '':
                    if dict_data == [{cat_field: ''}]:
                        dict_data = [{cat_field : x}]
                    elif len(dict_data)<1000:
                        dict_data.append({cat_field : x})
    except:
    	ErrorPrints(4,0,"--group-by",cat_field)
    if len(dict_data)>20:
        ErrorPrints(3,0,"--group-by",0)
        gb_capped = True 
      
    for x in range(len(sys.argv)):

        if sys.argv[x].lower() == "--min":
            arg_min(sys.argv[x+1], cat_field)
        if sys.argv[x].lower() == "--max":
            arg_max(sys.argv[x+1], cat_field)
        if sys.argv[x].lower() == "--mean":
            arg_mean(sys.argv[x+1], cat_field)
        if sys.argv[x].lower() == "--sum":
            arg_sum(sys.argv[x+1], cat_field)
        if sys.argv[x].lower() == "--count":
            arg_count(cat_field)
        if sys.argv[x].lower() == "--top":
        	try:
                if int(args.top[0])>20:
                    ErrorPrints(3, 0,"--top", 0)
        			arg_top(20, sys.argv[x+2], cat_field)
        		else:
        			arg_top(sys.argv[x+1], sys.argv[x+2], cat_field)
            except:
                ErrorPrints(6,0,"--top",0)
    dict_data = sorted(dict_data, key= lambda i: i[cat_field])
#Group_by capped is true, create field and list
    if gb_capped == True:
        string = ''
        heading = str(cat_field)+"_OTHER"
        gb_capped_heading = {str(cat_field):heading}
        for i in dict_data[20:]:
            for k,v in i.items():
                if i != len(dict_data):
                    string += v + ", "
                else: 
                    string += v
        gb_capped_dict = {str(cat_field):string}

    return
 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help = "Filename input", required = True)
    parser.add_argument("--group-by", type = str, help = "Output CSV file with one row of output per distinct value in that categorical field")
    parser.add_argument("--top", type=str, nargs = 2, help = "Compute the top k most common values of categorical-field-name")
    parser.add_argument("--count", action="store_true", help = "Count the number of records")
    parser.add_argument("--min", type = str, help = "Compute the minimum value of numeric-field-name")
    parser.add_argument("--max", type = str, help = "Compute the maximum value of numeric-field-name")
    parser.add_argument("--mean", type = str, help = "Compute the mean (average) of numeric-field-name")
    parser.add_argument("--sum", type = str, help = "Compute the sum of numeric-field-name")
    args = parser.parse_args()
    try:
        with open(args.input, 'r') as csv_file:
            keys = csv_file.readline().strip().encode("utf-8").decode("utf-8-sig").split(",")
            for value in keys:
                dict_file[value] = [""]

        with open(args.input, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                for (key, value) in row.items():
                    temp = key.encode("utf-8").decode("utf-8-sig")
                    if temp in dict_file:
                        dict_file[temp].append(value)
    except:
        ErrorPrints(5,0,0,0)

    global filename, gb_capped, gb_capped_dict, gb_capped_heading
    filename = args.input

    if args.group_by:
        arg_group_by(args.group_by, args)
    elif len(sys.argv)==3:
        arg_count()
    else:
        for x in range(len(sys.argv)):
            if sys.argv[x].lower() == "--min":
                arg_min(sys.argv[x+1])
            if sys.argv[x].lower() == "--max":
                arg_max(sys.argv[x+1])
            if sys.argv[x].lower() == "--mean":
                arg_mean(sys.argv[x+1])
            if sys.argv[x].lower() == "--sum":
                arg_sum(sys.argv[x+1])
            if sys.argv[x].lower() == "--count":
                arg_count()
            if sys.argv[x].lower() == "--top":
            	if int(sys.argv[x+1])>20:
            		ErrorPrints(3, 0,"--top", 0)
            		arg_top(20, sys.argv[x+2])
            	else:
            		arg_top(sys.argv[x+1], sys.argv[x+2])

    csv_out = "output.csv"
    try:
        with open(csv_out, 'w') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=columns)
            csv_writer.writeheader()
            if gb_capped == False:
                for data in dict_data:
                    csv_writer.writerow(data)
            else:
                count = 0
                for data in dict_data:
                    if count < 20:
                        csv_writer.writerow(data)
                    count += 1
                csv_writer.writerow(gb_capped_heading)
                csv_writer.writerow(gb_capped_dict)
    except:
        ErrorPrints(5,0,0,0) 
    clear_dicts()

if __name__ == '__main__':
    main()
