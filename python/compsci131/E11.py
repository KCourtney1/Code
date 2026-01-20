import os, csv

def final_grades(filename):
    target_path = os.path.join(os.path.dirname(__file__), filename)
    out_path = os.path.join(os.path.dirname(__file__), "finalGrades.csv")
    with open(target_path,"r") as the_file, open(out_path,"w") as out_file:
        contents = csv.DictReader(the_file)
        out_file.write("student,ID,SIS User ID,FINAL GRADE\n")
        for row in contents:
            final_grade = ((float(row["HW1"]) + float(row["HW2"]) + float(row["HW3"]) + float(row["HW4"]))/4)*.35 + ((float(row["QUIZ1"]) + float(row["QUIZ2"]) + float(row["QUIZ3"]))/3)*.4 + float(row["Final"])*.25
            out_file.write(f"{row['Student']},{row['ID']},{row['SIS User ID']},{final_grade}\n")

final_grades("grades.csv")