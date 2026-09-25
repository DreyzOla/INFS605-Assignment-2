# CSV read, write, update, delete functions
import csv
import sys

# Increase CSV field size limit to prevent overflow errors with large records
csv.field_size_limit(sys.maxsize)

FILE_NAME = "applications.csv"

def load_applications():
    with open(FILE_NAME, "r") as file:
        return list(csv.reader(file))

def save_application(app_name, category, department, url):
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([app_name, category, department, url])

def save_all_applications(apps):
    """Overwrites the CSV file with the complete updated list of applications."""
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(apps)

