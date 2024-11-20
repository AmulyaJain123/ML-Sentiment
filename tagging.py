import pandas as pd
from textblob import TextBlob

input_file = 'cleaned_reviews.csv'
df = pd.read_csv(input_file)

def classify_comment(comment):
    analysis = TextBlob(comment)
    return 1 if analysis.sentiment.polarity > 0 else 0

df['Sentiment'] = df['Preprocessed Review'].apply(classify_comment)

output_file = 'classified_comments.csv'
df.to_csv(output_file, index=False)

print(f"Classification complete. Results saved to {output_file}")