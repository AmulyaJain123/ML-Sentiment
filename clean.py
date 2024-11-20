import csv

def preprocess_text(review):
    review = review.lower()
    
    cleaned_review = ""
    for char in review:
        if char.isalnum() or char.isspace():
            cleaned_review += char
    
    cleaned_review = ' '.join(cleaned_review.split())

    tokens = []
    word = ""
    for char in cleaned_review:
        if char.isspace():
            if word:
                tokens.append(word)
                word = ""
        else:
            word += char
    if word:  
        tokens.append(word)

    stop_words = [
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", 
    "you", "your", "yours", "yourself", "yourselves", 
    "he", "him", "his", "himself", 
    "she", "her", "hers", "herself", 
    "it", "its", "itself", 
    "they", "them", "their", "theirs", "themselves", 
    "what", "which", "who", "whom", 
    "this", "that", "these", "those",
    "am", "is", "are", "was", "were",
    "be", "been", "being",
    "have", "has", "had", 
    "having",
    "do", "does", "did",
    "doing",
    "a", "an", "the",
    "and", "but", "if",
    "or", "because",
    "as", 
    "until", 
    "while",
    "of","at","by","for","with","about","against","between","into","through","during","before","after","above","below",
    "to","from","up","down","in","out","on","off","over","under",
    "again","further",
    ]
    
    filtered_tokens = []
    for token in tokens:
        if token not in stop_words:
            filtered_tokens.append(token)

    def stem_word(word):
        suffixes = [
            "ing", "ly", "ed", "es", "s", "er", "ment", "ness", "ation", "tion", "able", "ible", 
            "ous", "ive", "ful", "less", "est", "ant", "ent", "al", "ic", "ical", "ity", "ies", "ize", "ise"
        ]
        
        exceptions = {
            "am": "be", 
            "are": "be", 
            "is": "be", 
            "was": "be", 
            "were": "be", 
            "been": "be", 
            "being": "be", 
            "have": "have", 
            "has": "have", 
            "had": "have", 
            "do": "do", 
            "does": "do", 
            "did": "do", 
            "doing": "do", 
            "go": "go", 
            "went": "go", 
            "gone": "go", 
            "saw": "see", 
            "seen": "see", 
            "say": "say", 
            "said": "say", 
            "make": "make", 
            "made": "make", 
            "know": "know", 
            "knew": "know", 
            "known": "know", 
            "think": "think", 
            "thought": "think", 
            "come": "come", 
            "came": "come",
            'men': 'man',
            'women': 'woman',
            'teeth': 'tooth',
            'feet': 'foot',
            'better': 'good',
            'best': 'good',
            'worse': 'bad',
            'worst': 'bad',
            'further': 'far',
            'farther': 'far',
            'more': 'many',
            'most': 'many',
            'less': 'little',
            'least': 'little',
            'gotten': 'get',
            'forgotten': 'forget',
        }
        
        if word in exceptions:
            return word
        
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix):
                word = word[:-len(suffix)]
                break  
        
        if len(word) > 3 and word[-1] == word[-2]:
            word = word[:-1]  
        
        return word


        suffixes = ["ing", "ly", "ed", "es", "s", "er"]
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix):
                return word[:-len(suffix)]
        return word

    stemmed_tokens = [stem_word(token) for token in filtered_tokens]

    preprocessed_review = ' '.join(stemmed_tokens)
    return preprocessed_review

def preprocess_csv(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  
        reviews = [row for row in reader]  

    preprocessed_reviews = []
    for row in reviews:
        review_text = row[1]  
        preprocessed_review = preprocess_text(review_text)
        preprocessed_reviews.append([preprocessed_review])

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Preprocessed Review"])  
        writer.writerows(preprocessed_reviews)

input_csv = 'steam_reviews_555570.csv'  
output_csv = 'cleaned_reviews.csv'  
preprocess_csv(input_csv, output_csv)


