import pandas as pd

# importing the shortest path distance txt into the dataframe shortest
file = open('wikispeedia_paths-and-graph/shortest-path-distance-matrix.txt', 'r')
# Reading lines from the txt file into list - Lines
Lines = file.readlines()
shortest = pd.DataFrame(Lines)  #passed list into the dataframe df
shortest.columns = ["line"]
shortest = shortest.loc[17:]  #removed the introductory lines of the txt file
shortest.reset_index(inplace = True)
shortest.drop("index", axis =1,inplace =True)
# Splitting the string of each line of txt file by delimiter "" and storing it in shortmatrix 2d list
shortmatrix = shortest["line"].str.split("")  # 2x2 dataframe

# importing article-id.csv
# artdf = pd.read_csv("article-id.csv", names = ["article_id","article_name"])
artdf = pd.read_csv("article-id.csv")
artdf.set_index("article_name", inplace= True) #seting index to article name.

# importing paths_finished.tsv in dataframe df
tsv_file = open("wikispeedia_paths-and-graph/paths_finished.tsv")
df = pd.read_csv(tsv_file, delimiter="\t", names = ["ip","timestamp","duration", "path","rating","path_length"])
# df.drop(2411,inplace = True)
df = df.loc[15:] #dropping initial introductory lines from the ts
df.reset_index(inplace = True)
df.drop(["index","ip","timestamp","duration","rating"], axis =1, inplace = True)

split = df["path"].str.split(";")

# Finding path length - backs are allowed
list1= []
for i, row in df.iterrows():
    list1.append( len(split[i]))

df["path_length"] = list1

# Finding shortest path and the path length where back links are not counted.
shortlist = []
lengthlist = []
for i in range(0,len(split)):
    source = artdf.loc[split[i][0],"article_id"]
    target  = artdf.loc[split[i][len(split[i])-1],"article_id"]
    source = int(source[1:])-1
    target = int(target[1:])
    shortlist.append(shortmatrix[source][target])
    length = len(split[i])
    for j in range(0, length):
        if(split[i][j] == "<"):
            length-=2;
    lengthlist.append(length)
# print(shortlist)

# Assigning shortest path to df
df["shortest_path"] = shortlist

# Assigning path_length if backs are not allowed
backs_not_df = df.copy()
backs_not_df.drop("path_length", axis =1, inplace = True)
backs_not_df["path_length"] = lengthlist
backs_not_df = backs_not_df[["path","path_length","shortest_path"]]

# Removing the case where wrong path is given in the file
df = df[df["shortest_path"]!="_"]
backs_not_df = backs_not_df[backs_not_df["shortest_path"]!="_"]

# Calculating ratios for both the cases
df['shortest_path'] = df['shortest_path'].astype('int') #converting into int data type
backs_not_df['shortest_path'] = backs_not_df['shortest_path'].astype('int')
# df['shortest_path'] -=1
df['path_length'] -=1
backs_not_df['path_length'] -=1
# backs_not_df['shortest_path'] -=1
df["ratio"] = df["path_length"] / df["shortest_path"]
backs_not_df["ratio"] = backs_not_df["path_length"] / backs_not_df["shortest_path"]

# Removing the cases where rotio is infinite.
df = df[df["path_length"]!=0]
backs_not_df = backs_not_df[backs_not_df["path_length"]!=0]

# Dropping the path column
path_df = df["path"]
df.drop("path", axis =1, inplace = True)
backs_not_df.drop("path", axis =1, inplace = True)

# Renaming the column names
df.columns = [["Human_Path_Length","Shortest_Path_Length","Ratio"]]
backs_not_df.columns = [["Human_Path_Length","Shortest_Path_Length","Ratio"]]

# Exporting results to finished-paths-back.csv and finished-paths-no-back
df.to_csv("finished-paths-back.csv", index = False)
backs_not_df.to_csv("finished-paths-no-back.csv", index = False)
print("\nOutput file generated - finished-paths-back.csv and finished-paths-no-back.csv\n")


path_df.to_csv("cleaned_path.csv", index =False)
# print(df)
