# CSV read, write, update, delete functions
import csv

FILE_NAME = "applications.csv"

def load_applications():
    with open(FILE_NAME, "r") as file:
        return list(csv.reader(file))

def save_application(app_name, category, department, url):
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([app_name, category, department, url])

