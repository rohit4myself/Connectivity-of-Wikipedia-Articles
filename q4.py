import pandas as pd
import csv

# importing the shortest path distance txt into the dataframe df
file = open('wikispeedia_paths-and-graph/shortest-path-distance-matrix.txt', 'r')
# Reading lines from the txt file into list - Lines
Lines = file.readlines()
df = pd.DataFrame(Lines)  #passed list into the dataframe df
df.columns = ["line"]
df = df.loc[17:]  #removed the introductory lines of the txt file
df.reset_index(inplace = True)
df.drop("index", axis =1,inplace =True)
df["article_id"] = ["A" + "%04d"% i for i in range(1,df.shape[0]+1)]
# Splitting the string of each line of txt file by delimiter "" and storing it
split = df["line"].str.split("")  # 2x2 dataframe

list1 = []
# opening the output file - edges.csv
with open('edges.csv', 'w+', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(("From_ArticleID","To_ArticleID"))
    for i in range(0, len(split)):
        for j in range(1, 4605):
            if(split[i][j] == "1"):
                k =i+1
                writer.writerow(("A" + "%04d"% k,"A" + "%04d"% j))

print("\n\nOutput file generated - edges.csv")
