import pandas as pd;

# Computing parent dictionary ------------------------------------------------------------------------
# Importing category-id.csv (q2)
df= pd.read_csv("category-id.csv")
df.columns = ["category_name","category_id"]
# print(df)
categoryname = list(df["category_name"])
categoryid = list(df["category_id"])

category = {} #Dicionary for category name vs category id mapping
for i in range(len(categoryname)):
    category[categoryname[i]] = categoryid[i]

parent = {} #Dictionary to store the parent category id of the tree.
parent['C0001'] = 'root'
# Initiallizing the parent dictionary
for i in range (1,146):
    split = categoryname[i].split(".")
    length  = len(split)
    if (length ==2 ):
        parent[categoryid[i]] = category[split[0]]
    elif (length ==3):
        n = split[0] + "." + split[1]
        parent[categoryid[i]] =category[n]
    elif (length == 4):
        n = split[0] + "." + split[1] + "." + split[2]
        parent[categoryid[i]] =category[n]

del df
# ------------------------------------------------------------------------------------------------------

# importing tsv file into dataframe df
tsv_file = open("wikispeedia_paths-and-graph/paths_unfinished.tsv")
df = pd.read_csv(tsv_file, delimiter="\t", names = ["a","b","c","path", "target","type"])
# Dropping initial introductory rows and the columns - a,b,c ,and type
df = df.loc[16:]
df.reset_index(inplace =True)
df.drop(["index","a","b","c","type"], axis =1, inplace = True)

split = df.loc[:,"path"].str.split(";", expand = True)
df["source"] = split[0]
# Dataframe df has source article name and target article name
df = df[["source","target"]]
# print(df.head)

# importing article name vs article id  from article-id.csv (q1) in dataframe articlemap
articlemap = pd.read_csv("article-id.csv")

articlemap.set_index(articlemap.columns[1], inplace = True)
# print("article vs article_id")
# print(articlemap)

#Renaming spelling mistakes---------------------------------------
df.loc[df["target"] == "Long_peper","target"] = "Long_pepper"
df.loc[df["target"] == "Adolph_Hitler","target"] = "Adolf_Hitler"
df.loc[df["target"] == 'Charlottes_web',"target"] = "Charlotte%27s_Web"
df.loc[df["target"] == "_Zebra","target"] = "Zebra"
df.loc[df["target"] == "Macedonia","target"] = "Macedon"
df.loc[df["target"] == "Podcast","target"] = "Podcasting"
df.loc[df["target"] == "Kashmir","target"] = "Kashmir_region"
df.loc[df["target"] == "Bogota","target"] = "Bogot%C3%A1"
df.loc[df["target"] == "Western_Australia","target"] = "Perth%2C_Western_Australia"



# source_dest = pd.DataFrame(columns = ["source_category","destination_category"])

#Storing source article id in source_dest dataframe
source_dest = pd.DataFrame(articlemap.loc[df["source"],"article_id"])
source_dest.reset_index(inplace = True)
source_dest.drop("article_name",axis =1, inplace = True)


#Storing destination article id in source_dest dataframe
for i in range(source_dest.shape[0]):
    if(df.loc[i,"target"] in articlemap.index):
        source_dest.loc[i,"destination_category"] = articlemap.loc[df.loc[i,"target"],"article_id"]
    else:
        source_dest.loc[i,"destination_category"] = "A0000"
source_dest.columns = ["source_articleid","destination_articleid"]

# print("For unfinished Paths-------------------------------------------")
source_dest.to_csv("1.csv", index =False)

#importing article-categories.csv (q3) in dataframe art_cat
art_cat = pd.read_csv("article-categories.csv")
art_cat.fillna("No", inplace = True)
art_cat = art_cat.append({'article_id':'A0000',"categoryid1":"C0001","categoryid2":"No","categoryid3":"No"}, ignore_index = True)
art_cat.set_index("article_id", inplace = True)
# print(art_cat)


l1 =[]
l2 = []
for i, row in source_dest.iterrows():
    s_artid = row["source_articleid"]
    d_artid = row["destination_articleid"]
    c1=[]
    #Adding categories corresponding to source_articleid to list c1
    c1.append(art_cat.loc[s_artid,"categoryid1"])

    if art_cat.loc[s_artid,"categoryid2"] !="No":
        c1.append(art_cat.loc[s_artid,"categoryid2"])
    if art_cat.loc[s_artid,"categoryid3"] !="No":
        c1.append(art_cat.loc[s_artid,"categoryid3"])

    c2=[]
    #Adding categories corresponding to destination_articleid to list c2
    c2.append(art_cat.loc[d_artid,"categoryid1"])

    if art_cat.loc[d_artid,"categoryid2"] !="No":
        c2.append(art_cat.loc[d_artid,"categoryid2"])
    if art_cat.loc[d_artid,"categoryid3"] !="No":
        c2.append(art_cat.loc[d_artid,"categoryid3"])

    k1,k2 =[],[]
    for m in c1:
        k = m
        while k!="root":
            k1.append(k)
            k = parent[k]
    for m in c2:
        k = m
        while k!="root":
            k2.append(k)
            k = parent[k]

    c1 = list(set(k1))
    c2 = list(set(k2))

    for p in c1:
        for q in c2:
            # fini_category_pair = fini_category_pair.append({"category1":p,"category2":q},ignore_index=True)
            l1.append(p)
            l2.append(q)

# DataFrame unf_category_pair will store the category pairs for unfinish paths
unf_category_pair = pd.DataFrame(columns = ["category1","category2"])
unf_category_pair["category1"] = l1;
unf_category_pair["category2"] =l2;

# Finding the count of each category pair using group by
unf_category_pair = unf_category_pair.groupby(["category1","category2"]).size().reset_index(name = 'count')
# print(unf_category_pair)


'''
#Those destination articles that do not map
# print(source_dest[source_dest["destination_category"].isna()==True])
# print(df.loc[source_dest[source_dest["destination_category"].isna()==True].index,"target"])
'''

# ---------------------------------------------------------------------------------------------
# Finished Paths

#importing cleaned_path.csv (generated in q6 storing the paths that are valid.)
fini = pd.read_csv("cleaned_path.csv")

split = fini["path"].str.split(";")
# print(split)

# Storing source article name in l1 and target article name in l2 and
# storing them in DataFrame fini_source_dest
l1=[]
l2 = []
for i in range(fini.shape[0]):
    length = len(split[i])
    l1.append(split[i][0])
    l2.append(split[i][length-1])

fini_source_dest = pd.DataFrame()
fini_source_dest["source_articlename"] = l1
fini_source_dest["destination_articlename"] = l2

# Getting article id from article names and storing them in the lists l3 and l4
# and then adding them in fini_source_dest
l3= list(articlemap.loc[fini_source_dest["source_articlename"],"article_id"])
l4= list(articlemap.loc[fini_source_dest["destination_articlename"],"article_id"])
fini_source_dest["source_articleid"] = l3
fini_source_dest["destination_articleid"] = l4

fini_source_dest.drop(["source_articlename","destination_articlename"], axis = 1, inplace = True)

# print("For finished Paths------------------------------------------------")
# print(fini_source_dest)

#Getting Category Id pair from these article id pairs.
l1 =[]
l2 = []
for i, row in fini_source_dest.iterrows():
    s_artid = row["source_articleid"]
    d_artid = row["destination_articleid"]
    c1=[]
    #Adding categories corresponding to source_articleid to list c1
    if s_artid in art_cat.index:
        c1.append(art_cat.loc[s_artid,"categoryid1"])

        if art_cat.loc[s_artid,"categoryid2"] !="No":
            c1.append(art_cat.loc[s_artid,"categoryid2"])
        if art_cat.loc[s_artid,"categoryid3"] !="No":
            c1.append(art_cat.loc[s_artid,"categoryid3"])

    c2=[]
    #Adding categories corresponding to destination_articleid to list c2
    if d_artid in art_cat.index:
        c2.append(art_cat.loc[d_artid,"categoryid1"])

        if art_cat.loc[d_artid,"categoryid2"] !="No":
            c2.append(art_cat.loc[d_artid,"categoryid2"])
        if art_cat.loc[d_artid,"categoryid3"] !="No":
            c2.append(art_cat.loc[d_artid,"categoryid3"])

    k1,k2 =[],[]
    for m in c1:
        k = m
        while k!="root":
            k1.append(k)
            k = parent[k]
    for m in c2:
        k = m
        while k!="root":
            k2.append(k)
            k = parent[k]

    c1 = list(set(k1))
    c2 = list(set(k2))
    for p in c1:
        for q in c2:
            # fini_category_pair = fini_category_pair.append({"category1":p,"category2":q},ignore_index=True)
            l1.append(p)
            l2.append(q)

# DataFrame unf_category_pair will store the category pairs for unfinish paths
f_category_pair = pd.DataFrame(columns = ["category1","category2"])
f_category_pair["category1"] = l1;
f_category_pair["category2"] =l2;

# Finding the count of each category pair using group by
f_category_pair = f_category_pair.groupby(["category1","category2"]).size().reset_index(name = 'count')
# print(f_category_pair)


# Finding percentage for both the finished and unfinished paths -----------------------------------------------

unf_category_pair.set_index(["category1","category2"], inplace = True)
# print(unf_category_pair)
unf_index = list(unf_category_pair.index)
# print(unf_index[0][0])
cl1 = list(f_category_pair["category1"])
cl2 = list(f_category_pair["category2"])

f_category_pair.set_index(["category1","category2"], inplace = True)
# print(f_category_pair)

lst1 = []
lst2 = []
for index, row in f_category_pair.iterrows():
    finished = row["count"]
    if index in unf_category_pair.index:
        unfinished = unf_category_pair.loc[index,"count"]
        total = finished + unfinished
        lst1.append((finished/total)*100)
        lst2.append((unfinished/total)*100)
    else:
        lst2.append(0)
        total = finished
        lst1.append((finished/total)*100)



for i in unf_index:
    if i not in f_category_pair.index:
        cl1.append(i[0])
        cl2.append(i[1])
        lst1.append(0)
        lst2.append(100)


output_df = pd.DataFrame(columns = ["category1","category2","percentage of finished paths","percentage of unfinished paths"])
f_category_pair.reset_index(inplace = True)
output_df["category1"] = cl1
output_df["category2"] = cl2
output_df["percentage of finished paths"] = lst1
output_df["percentage of unfinished paths"] = lst2

# print(output_df)
# Renaming column names
output_df.columns = [["From_Category","To_Category","Percentage_of_finished_paths","Percentage_of_unfinished_paths"]]
#Exporting results to category-pairs.csv.
output_df.to_csv("category-pairs.csv", index = False)
print("Output file generated - category-pairs.csv")
