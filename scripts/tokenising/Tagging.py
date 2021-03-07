import nltk
import random
#nltk.download('averaged_perceptron_tagger')
corp = nltk.corpus.ConllCorpusReader('.', 'tiger_release_aug07.corrected.16012013.conll09',
                                     ['ignore', 'words', 'ignore', 'ignore', 'pos'],
                                     encoding='utf-8')



tagged_sents = list(corp.tagged_sents())
random.shuffle(tagged_sents)

# set a split size: use 90% for training, 10% for testing
split_perc = 0.1
split_size = int(len(tagged_sents) * split_perc)
train_sents, test_sents = tagged_sents[split_size:], tagged_sents[:split_size]                                  


# Test tokenisieren
tokens_uncleaned = []

for i in range(len(data)):
    if type(data["Text"][i]) == float:
        tokens_uncleaned.append(["no"])
    else:
        tokens_uncleaned.append(word_tokenize(str(data["Text"][i])))


white_list_tags = ["NN","NNP","NE","ADJA"]
matched_tokens_total = []

for i in range(len(data["tokens_uncleaned"])):
    tagged_tokens = tagger.tag(data["tokens_uncleaned"][i])
    matched_tokens = []
    for i in range(len(tagged_tokens)):
        if tagged_tokens[i][1] in white_list_tags:
            matched_tokens.append(tagged_tokens[i][0])
        else:
            pass
    
    matched_tokens_total.append(matched_tokens)
    
