import pandas as pd

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

#importing cleaned_path.csv (generated in q6 storing the paths that are valid.)
df = pd.read_csv("cleaned_path.csv")
#Splitting the path on delimiter ";" and storing it in 2D array split
split = df["path"].str.split(";")
# print(split)

#importing finished-paths-no-back.csv (q6)
fini = pd.read_csv("finished-paths-no-back.csv")
fini.columns = [["a","b","ratio"]]
# Storing source article name in l1 and target article name in l2
# and storing them in DataFrame fini_source_dest
l1=[]
l2 = []
lratio =[]
for i in range(fini.shape[0]):
    length = len(split[i])
    l1.append(split[i][0])
    l2.append(split[i][length-1])
    lratio.append(fini.loc[i,"ratio"])

fini_source_dest = pd.DataFrame()
fini_source_dest["source_articlename"] = l1
fini_source_dest["destination_articlename"] = l2
fini_source_dest["ratio"] = lratio

# Getting article id from article names and storing them in the lists l3 and l4
# and then adding them in fini_source_dest
# importing article name vs article id  from article-id.csv (q1) in dataframe articlemap
articlemap = pd.read_csv("article-id.csv")
articlemap.set_index(articlemap.columns[1], inplace = True) #setted article name as index
# print(articlemap)
l3= list(articlemap.loc[fini_source_dest["source_articlename"],"article_id"])
l4= list(articlemap.loc[fini_source_dest["destination_articlename"],"article_id"])
fini_source_dest["source_articleid"] = l3
fini_source_dest["destination_articleid"] = l4
#Dropping source and destination article names.
fini_source_dest.drop(["source_articlename","destination_articlename"], axis = 1, inplace = True)
# print(fini_source_dest)

#importing article-categories.csv (q3) in dataframe art_cat
art_cat = pd.read_csv("article-categories.csv")
art_cat.fillna("No", inplace = True)
art_cat.set_index("article_id", inplace = True)

#Getting Category Id pair from these article id pairs and also storing ratio
l1 =[]
l2 = []
lratio = []
for i, row in fini_source_dest.iterrows():
    s_artid = row["source_articleid"]
    d_artid = row["destination_articleid"]
    ratio = row["ratio"]
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
            lratio.append(ratio)

# DataFrame unf_category_pair will store the category pairs for unfinish paths
f_category_pair = pd.DataFrame(columns = ["category1","category2","ratio"])
f_category_pair["category1"] = l1;
f_category_pair["category2"] =l2;
f_category_pair["ratio"] =lratio;
# print(f_category_pair)

# Finding the count of each category pair using group by and storing it in DataFrame count_category
count_category = f_category_pair.groupby(["category1","category2"]).size().reset_index(name = 'count')
# print(count_category)

# Finding the sum of ratio of each category pair using group by.
f_category_pair = f_category_pair.groupby(["category1","category2"]).sum()["ratio"].reset_index(name = 'sum of ratio')
f_category_pair["count"] = count_category["count"]
# Finding average ratio
f_category_pair["average ratio"] = f_category_pair["sum of ratio"] / f_category_pair["count"]
# print(f_category_pair)

output_df = f_category_pair[["category1","category2","average ratio"]].copy()
output_df.sort_values(by=["category1","category2"], inplace = True)
output_df.columns = [["From_Category","To_Category","Ratio_of_human_to_shortest"]]
output_df.to_csv("category-ratios.csv", index = False)
print("Output file generated - category-ratios.csv")
