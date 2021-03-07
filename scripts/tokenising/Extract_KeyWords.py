values_total = []
token_total = []
docs_total = []

for i in range(len(data["cleaned_text"])):
    values=[]
    document=[]
    token = []
    for key in tf_idf:
        if key[0] == i:
            document.append(key[0])
            values.append(key[1])
            token.append(tf_idf[key])
        else:
            pass
        
    print(i)      
    df = pd.DataFrame()
    df["values"] = values
    df["token"] = token
    df["doc"] = document
    df = df.sort_values(by='token', ascending=False)
    df = df.head()
    values_total.append(df["values"].to_list())
    token_total.append(df["token"].to_list())
    docs_total.append(df["doc"].to_list())

docs_ = []
values_1 = []
values_2 = []
values_3 = []
values_4 = []
values_5 = []

for i in range(len(values_total)):
    if len(values_total[i]) == 5:
        values_1.append(values_total[i][0])
        values_2.append(values_total[i][1])
        values_3.append(values_total[i][2])
        values_4.append(values_total[i][3])
        values_5.append(values_total[i][4])
    else:
        values_1.append("")
        values_2.append("")
        values_3.append("")
        values_4.append("")
        values_5.append("")

