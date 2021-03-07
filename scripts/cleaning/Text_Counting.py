class TextCounts(BaseEstimator, TransformerMixin):
    
    def count_regex(self, pattern, tweet):
        return len(re.findall(pattern, tweet))
    
    def fit(self, X, y=None, **fit_params):
        # fit method is used when specific operations need to be done on the train data, but not on the test data
        return self
    
    def transform(self, X, **transform_params):
        count_words = X.apply(lambda x: self.count_regex(r'\w+', str(x))) 
        count_data = X.apply(lambda x: self.count_regex(r'Data\w+', str(x)))
        count_hashtags = X.apply(lambda x: self.count_regex(r'#\w+', str(x)))
        count_capital_words = X.apply(lambda x: self.count_regex(r'\b[A-Z]{2,}\b', str(x)))
        count_excl_quest_marks = X.apply(lambda x: self.count_regex(r'!|\?', str(x)))
        count_urls = X.apply(lambda x: self.count_regex(r'http.?://[^\s]+[\s]?', str(x)))
        # We will replace the emoji symbols with a description, which makes using a regex for counting easier
        # Moreover, it will result in having more words in the tweet
        #count_emojis = X.apply(lambda x: emoji.demojize(x)).apply(lambda x: self.count_regex(r':[a-z_&]+:', x))
        
        df = pd.DataFrame({'count_words': count_words
                           , 'count_data': count_data
                           , 'count_hashtags': count_hashtags
                           , 'count_capital_words': count_capital_words
                           , 'count_excl_quest_marks': count_excl_quest_marks
                           , 'count_urls': count_urls
                          })
        
        return df

