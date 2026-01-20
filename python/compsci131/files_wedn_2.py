# Go to Canvas > Modules and download the files.zip
# file from Week 6 Module
# Unzip the folder and save the files in the same 
# folder where you will save your script for today

import os, csv
#import csv

def get_avg_lst(filename):
    target_path = os.path.join(os.path.dirname(__file__), filename)
    with open(target_path, "r") as the_file:
        content = the_file.readlines()
    
    output = []
    for line in content:
        data = line.split()
        if data:
            total =0.0
            for num in data:
                total += float(num)
            output.append(total/len(data))
    return output


def get_avg_file(filename):
    target_path = os.path.join(os.path.dirname(__file__), filename)
    with open(target_path, "r") as the_file:
        content = the_file.readlines()
    
    out_path = os.path.join(os.path.dirname(__file__), "average.txt")
    with open(out_path, "a") as out_file:
        for line in content:
            data = line.split()
            if data:
                total =0.0
                for num in data:
                    total += float(num)
                out_file.write(f"{total/len(data)}\n")


def get_avg_file_c(filename):
    target_path = os.path.join(os.path.dirname(__file__), filename)
    with open(target_path, "r") as the_file:
        content = the_file.readlines()
    
    out_path = os.path.join(os.path.dirname(__file__), "average.txt")
    with open(out_path, "w") as out_file:
        for line in content:
            line = line.strip()
            data = line.split(',')
            if data!=[""]:
                total =0.0
                for num in data:
                    total += float(num)
                out_file.write(f"{total/len(data)}\n")


def get_quotes(filename):
    target_path = os.path.join(os.path.dirname(__file__), filename)
    with open(target_path, "r") as the_file:
        content = csv.DictReader(the_file)
    
        for row in content:
            print(f"{row['Person']} said:")
            print(f"{row['Quote']}")
            print('\n')

def get_avg_cr(filename):
    target_path = os.path.join(os.path.dirname(__file__), filename)
    out_path = os.path.join(os.path.dirname(__file__), 'complete.csv')
    with open(target_path, "r") as the_file, open(out_path, 'a') as out_file:
        content = csv.DictReader(the_file)
        out_file.write("NAME,AVERAGE\n")
        for row in content:
            if row['status'] == 'COMPLETE':
                total = float(row['num1']) + float(row['num2']) + float(row['num3'])
                out_file.write(f"{row['name']},{total/3}\n")
    

if __name__ == "__main__":
    get_avg_cr('numbers_cr.txt')