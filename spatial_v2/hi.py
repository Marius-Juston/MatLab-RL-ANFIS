import csv
file = open("inputs100.csv")
reader = csv.reader(file)
lines= len(list(reader))

print(lines)
