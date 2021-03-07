DF = {}

for i in range(len(matched_tokens_total)):
    token = matched_tokens_total[i]
    for w in token:
        try:
            DF[w].add(i)
        except:
            DF[w] = {i}
            
for i in DF:
    DF[i] = len(DF[i])

# Function for Doc Frequency
def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

total_tagged_tokens = []
for i in range(len(matched_tokens_total)):
    for j in range(len(matched_tokens_total[i])):
        total_tagged_tokens.append(matched_tokens_total[i][j])

doc = 0
N = len(data)
tf_idf = {}

for i in range(N):
    
    tokens = data["tagged_tokens"][i]
    
    counter = Counter(tokens + matched_titels_total[i])
    words_count = len(tokens + matched_titels_total[i])
    print(i)
    for token in np.unique(total_tagged_tokens):
        if words_count == 0:
            tf = 0
        else:
        
            tf = counter[token]/words_count
            df = doc_freq(token)
            idf = np.log((N+1)/(df+1))
        
            tf_idf[doc, token] = tf*idf

    doc += 1

doc = 0

tf_idf_title = {}

for i in range(N):
    
    tokens = data["tagged_titels"][i]
    counter = Counter(tokens + data["tagged_tokens"][i])
    words_count = len(tokens + data["tagged_tokens"][i])
    print(i)

    for token in np.unique(total_tagged_tokens):
        if words_count == 0:
            tf = 0
        else:
            tf = counter[token]/words_count
            df = doc_freq(token)
            idf = np.log((N+1)/(df+1)) #numerator is added 1 to avoid negative values
        
            tf_idf_title[doc, token] = tf*idf

    doc += 1


for i in tf_idf:
    tf_idf[i] *= alpha

for i in tf_idf_title:
    tf_idf[i] = tf_idf_title[i]

