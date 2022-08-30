import pandas as pd
from collections import OrderedDict

# -------------------------------------------------------------------------------------------------------
# Importing edges.csv (q4)
df = pd.read_csv("edges.csv")
df.columns = ["e1","e2"]
e1 = list(df.e1)
e2 = list(df.e2)
from collections import defaultdict
graph = defaultdict(list)

for i in range(len(e1)):
    graph[e1[i]].append(e2[i])

queue = []     #Initialize a queue

# Performing BFS to create the parent dictionary parent[article] = name of parent article in graph.
def bfs( graph, node):
    global parent
    parent[node] = {}
    visited ={}
    visited[node] = True
    # visited.append(node)
    queue.append(node)
    # print(node)
    while queue:
        s = queue.pop(0)

        for neighbour in graph[s]:
          if neighbour not in visited:
              parent[node][neighbour] = s
              visited[neighbour] = True
              # print(neighbour)
              queue.append(neighbour)

parent= {}
for i in range(1,4605):
    bfs( graph, "A" + "%04d"%i)

# Function to find the shortest path between source and target article.
def findpath(source,target):
    l=[]
    l.append(target)
    m=target
    while m!=source:
        m=parent[source][m]
        l.append(m)

    return l

# -------------------------------------------------------------------------------------------------

# importing finished paths from cleaned_path.csv (generated in q6 for this question only.)
df = pd.read_csv("cleaned_path.csv")
# df.drop(df.iloc[:,1:], axis = 1, inplace = True)

# Splitting the paths by delimiter ";" and storing it in dataframe split
split  =df.loc[:,"path"].str.split(";")
# print(split)

# importing article id vs category id from article-categories.csv (q3)
art_cat = pd.read_csv("article-categories.csv")
art_cat.set_index("article_id", inplace = True)
# Replacing NaN values with 'No'
art_cat['categoryid2'].fillna('No', inplace=True)
art_cat['categoryid3'].fillna('No', inplace=True)

# print(art_cat)

# importing article name vs article id from article-id.csv (q1)
art_name = pd.read_csv("article-id.csv")
art_name.set_index("article_name", inplace = True)
# print(art_name)

short_cat_dict = {}
# Function to process shortest path to obtain the number of times
def process_shortpath(shortpathlst):
    global short_cat_dict
    for artid in shortpathlst:
        # artid = art_name.loc[article,"article_id"]
        if artid in art_cat.index:
            category = art_cat.loc[artid,"categoryid1"]
            category2 = art_cat.loc[artid,"categoryid2"]
            category3 = art_cat.loc[artid,"categoryid3"]

            if category in short_cat_dict:
                short_cat_dict[category]+=1
            else:
                short_cat_dict[category] = 1

            if(category2 != "No"):
                if category2 in short_cat_dict:
                    short_cat_dict[category2]+=1
                else:
                    short_cat_dict[category2] = 1

            if(category3!="No"):
                if category3 in short_cat_dict:
                    short_cat_dict[category3]+=1
                else:
                    short_cat_dict[category3] = 1

# Counting total number of occurence of a category in paths
cat_dict = {}

for i in range(split.shape[0]):
    length1 = len(split[i])
    source = split[i][0]
    source = art_name.loc[source,"article_id"]
    target = split[i][length1-1]
    target = art_name.loc[target,"article_id"]
    shortpathlst = []
    shortpathlst = findpath(source,target)
    process_shortpath(shortpathlst)
    l1= []
    for j in range(len(split[i])): #To obtain the backlink path in l1.
        if(split[i][j] != "<"):
            l1.append(split[i][j])
        else:
            l1.pop(len(l1)-1)
    for node in l1:
        artid = art_name.loc[node,"article_id"]
        if artid in art_cat.index:
            category = art_cat.loc[artid,"categoryid1"]
            category2 = art_cat.loc[artid,"categoryid2"]
            category3 = art_cat.loc[artid,"categoryid3"]

            if category in cat_dict:
                cat_dict[category]+=1
            else:
                cat_dict[category] = 1

            if(category2 != "No"):
                if category2 in cat_dict:
                    cat_dict[category2]+=1
                else:
                    cat_dict[category2] = 1

            if(category3!="No"):
                if category3 in cat_dict:
                    cat_dict[category3]+=1
                else:
                    cat_dict[category3] = 1


short_cat_dict2 = {}
# Function to obtain shortest_path count for number of paths
def process_shortpath_categorypath(shortpathlst):
    global short_cat_dict2
    duplicate_check = []
    for artid in shortpathlst:
        if artid in art_cat.index:
            category = art_cat.loc[artid,"categoryid1"]
            category2 = art_cat.loc[artid,"categoryid2"]
            category3 = art_cat.loc[artid,"categoryid3"]

            if category not in duplicate_check:
                duplicate_check.append(category)
                if category in short_cat_dict2:
                    short_cat_dict2[category]+=1
                else:
                    short_cat_dict2[category] = 1

            if(category2 != "No"):
                if category2 not in duplicate_check:
                    duplicate_check.append(category2)
                    if category2 in short_cat_dict2:
                        short_cat_dict2[category2]+=1
                    else:
                        short_cat_dict2[category2] = 1

            if(category3!="No"):
                if category3 not in duplicate_check:
                    duplicate_check.append(category3)
                    if category3 in short_cat_dict2:
                        short_cat_dict2[category3]+=1
                    else:
                        short_cat_dict2[category3] = 1



# Caculating number of paths in which a category has occured
cat_dict2 = {}
for i in range(split.shape[0]):
    length2 = len(split[i])
    source = split[i][0]
    source = art_name.loc[source,"article_id"]
    target = split[i][length2-1]
    target = art_name.loc[target,"article_id"]
    shortpathlst = []
    shortpathlst = findpath(source,target)
    process_shortpath_categorypath(shortpathlst)
    l1= []
    for j in range(len(split[i])):#To obtain the backlink path in l1.
        if(split[i][j] != "<"):
            l1.append(split[i][j])
        else:
            l1.pop(len(l1)-1)
    l1 = set(l1) # removed duplicates
    l1 = list(l1)
    duplicate_check=[]
    for node in l1:
        artid = art_name.loc[node,"article_id"]
        if artid in art_cat.index:
            category = art_cat.loc[artid,"categoryid1"]
            category2 = art_cat.loc[artid,"categoryid2"]
            category3 = art_cat.loc[artid,"categoryid3"]

            if category not in duplicate_check:
                duplicate_check.append(category)
                if category in cat_dict2:
                    cat_dict2[category]+=1
                else:
                    cat_dict2[category] = 1

            if(category2 != "No"):
                if category2 not in duplicate_check:
                    duplicate_check.append(category2)
                    if category2 in cat_dict2:
                        cat_dict2[category2]+=1
                    else:
                        cat_dict2[category2] = 1

            if(category3!="No"):
                if category3 not in duplicate_check:
                    duplicate_check.append(category3)
                    if category3 in cat_dict2:
                        cat_dict2[category3]+=1
                    else:
                        cat_dict2[category3] = 1


# Storing the results in cat_df dataframe
# k = zip(list(cat_dict.keys()),list(cat_dict.values()),list(cat_dict2.values()),list(short_cat_dict.values()),list(short_cat_dict2.values()))

p1,p2,p3,p4,p5 = [],[],[],[],[]
for i in range(1,147):
    m = "C" + "%04d"%i
    if m not in cat_dict:
        cat_dict[m] = 0
    if m not in cat_dict2:
        cat_dict2[m] = 0
    if m not in short_cat_dict:
        short_cat_dict[m] = 0
    if m not in short_cat_dict2:
        short_cat_dict2[m] = 0
    p1.append(m)
    p2.append(cat_dict[m])
    p3.append(cat_dict2[m])
    p4.append(short_cat_dict[m])
    p5.append(short_cat_dict2[m])

k = zip(p1,p2,p3,p4,p5)


cat_df = pd.DataFrame(list(k), columns = ["category_id","number of times this category is traversed","number of paths","shortest number of times","shortest number of paths"])
#Sorting on the basis of category id
cat_df.sort_values(by=["category_id"], inplace = True)

cat_df = cat_df[["category_id","number of paths","number of times this category is traversed","shortest number of paths","shortest number of times"]]
cat_df.columns = ["Category_ID","Number_of_human_paths_traversed","Number_of_human_times_traversed","Number_of_shortest_paths_traversed","Number_of_shortest_times_traversed"]

# Exporting to category-paths.csv file
cat_df.to_csv("category-paths.csv", index = False)
print("Output file generated - category-paths.csv")
# print(cat_df)



# print(df)
