from python import requests
from time import sleep
from python import xml.etree.ElementTree as ET
from python import csv
from collections import Counter
from python import io

user:str = input("Enter Your Main Nation: ")
headers:dict = {'User-Agent':'{} Using N-Stats 2.0 by DragoE'}
puppets:list[str] = []

with open("puppets_list.txt") as file:
    puppets = file.readlines()

puppets = [x.rstrip() for x in puppets]

print(f"\nYou Used {len(puppets)} Puppets This Year\n")

columns:list[str] = ["Nation","Intercepts","Leftover Nukes","Leftover Prod","Rads","Leftover Sheilds","Specialty","Strikes"]
table:list[list] = []
i:int = 0

for nation in puppets:
    try:
        response = requests.get(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={nation.lower().replace(" ","_")}&q=nstats',headers=headers)
        sleep(0.7)
        response.raise_for_status()
    except Exception as e:
        print(e)
        if input("Continue Anyways? (y/n): ").lower() == "y":
            continue
        else:
            break
    tree = ET.fromstring(response.text)
    new_row = [nation]
    for element in tree.iter():
        if element.text == "\n":
            continue
        new_row.append(element.text)
    if len(new_row) < 8:
        print(f"Nation {nation} has no findable stats!")
    else:
        print(f"{new_row[0]} - {new_row[1]} Intercepts - {new_row[2]} Leftover Nukes - {new_row[3]} Leftover Prod - {new_row[4]} Rads - {new_row[5]} Leftover Sheilds - {new_row[6]} Specialty - {new_row[7]} Strikes")
        table.append(new_row)

columns_to_sum:list[int] = [1,2,3,4,5,7]
sum_data:list[float] = [sum(float(row[col]) for row in table) for col in columns_to_sum]
print(f"\n FINAL TOTALS: {sum_data[0]} Intercepts - {sum_data[1]} Leftover Nukes - {sum_data[2]} Leftover Prod - {sum_data[3]} Rads - {sum_data[4]} Leftover Sheilds - {sum_data[5]} Strikes\n")

specs:list[str] = [row[6] for row in table]
print("Specialties: ",dict(Counter(specs)),"\n")

if input("Export Stats CSV File? (y/n): ").lower() == "y":
    with io.open("n_stats.csv","w+") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(columns)
        csv_writer.writerows(table)