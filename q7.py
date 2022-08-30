import pandas as pd
import csv

def percentage(inputname, outputname):
    df = pd.read_csv(inputname)
    total_rows = df.shape[0]

    samelength = df[df["Human_Path_Length"] == df["Shortest_Path_Length"]].shape[0]
    percentage_samelength = (samelength/total_rows) *100

    list1 = []
    for i in range(1,11):
         number  = df[df["Human_Path_Length"] - df["Shortest_Path_Length"] == i].shape[0]
         list1.append((number / total_rows) * 100)


    greater_than_11 = df[df["Human_Path_Length"] - df["Shortest_Path_Length"] >= 11].shape[0]
    percentage_greater_than_11 = (greater_than_11/total_rows) *100

    with open(outputname, 'w+', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(("Equal_Length", "Larger_by_1", "Larger_by_2", "Larger_by_3", "Larger_by_4", "Larger_by_5", "Larger_by_6", "Larger_by_7", "Larger_by_8", "Larger_by_9", "Larger_by_10", "Larger_by_more_than_10"))
        writer.writerow((percentage_samelength, list1[0], list1[1], list1[2], list1[3], list1[4], list1[5], list1[6], list1[7], list1[8], list1[9],percentage_greater_than_11))


percentage("finished-paths-back.csv",'percentage-paths-back.csv')
percentage("finished-paths-no-back.csv",'percentage-paths-no-back.csv')
print("\nOutput file generated - percentage-paths-back.csv and percentage-paths-no-back.csv\n")
