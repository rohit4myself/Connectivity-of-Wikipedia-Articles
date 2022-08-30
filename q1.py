import pandas as pd;

# importing tsv file into dataframe df
tsv_file = open("wikispeedia_paths-and-graph/articles.tsv")
df = pd.read_csv(tsv_file, delimiter="\t", names = ["article_name", "article_id"])
# Dropping initial introductory rows 
df = df.loc[11:]
df.reset_index(inplace =True)
df.drop("index", axis =1, inplace = True)
# Assigning Ids to article
df["article_id"] = ["A" + "%04d"% i for i in range(1,df.shape[0]+1)]    
df = df[["article_id", "article_name"]]
# Exporting results to article-id.csv
df.to_csv("article-id.csv" , index = False)
print("Output file generated: article-id.csv")
# print(df)
