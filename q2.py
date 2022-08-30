import pandas as pd;

# importing tsv file into dataframe df
tsv_file = open("wikispeedia_paths-and-graph/categories.tsv")
df = pd.read_csv(tsv_file, delimiter="\t", names = ["article_name", "category_name"])
# Dropping initial introductory rows and the column - article_name
df = df.loc[12:]
df.reset_index(inplace =True)
df.drop(["index","article_name"], axis =1, inplace = True)

# Removing duplicate category names and storing them in category_df
myset = set(df["category_name"])
category_df = pd.DataFrame();
category_df["category_name"] = list(myset);

# print(category_df)

# Splitting the category into sub-categories by delimiter "." and storing these 
# sub-categories in different columns c1, c2, and c3
split = category_df["category_name"].str.split(".",expand = True)
# print(split)

category_df["c0"]= split[0]
category_df["c1"]= split[0] + "." + split[1]
category_df["c2"]= split[0] + "." + split[1]+ "." + split[2]
category_df["c3"]= split[0] + "." + split[1]+ "." + split[2] + "." + split[3]
category_df.sort_values(by=["c0","c1","c2","c3"], inplace = True)
category_df.drop("category_name",axis = 1,inplace = True)
category_df.fillna("No", inplace = True)
# print(category_df)

output_df= pd.DataFrame(columns=["category_name","category_id"])



# Function for giving id in bread first order
def tree(name,count,output_df):
    set1 = list(category_df[name])
    lst = []
    [lst.append(x) for x in set1 if x not in lst and x!="No"] 
    c = pd.DataFrame(lst, columns=["category_name"])
    # c.sort_values(by = ["category_name"], inplace = True)
    # c.reset_index(inplace = True)
    # c.drop("index", axis =1 , inplace = True)
    # c.dropna(inplace = True)
    for i in range(0, c.shape[0]):
        k = count +i
        c.loc[i,"category_id"] = "C" + "%04d"% k
    count = k +1
    output_df = pd.concat([output_df,c])
    # print(c)
    return count, output_df

count = 1;
#Calls to the function tree 
count, output_df = tree("c0",count, output_df)
count, output_df = tree("c1",count, output_df)
count, output_df = tree("c2",count, output_df)
count, output_df = tree("c3",count, output_df)

# print(output_df)

# Exporting results in category-id.csv
output_df.to_csv("category-id.csv" , index = False)
print("Output file generated: category-id.csv")