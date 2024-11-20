
import csv

def read_reviews_from_csv(filename):
    reviews = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            if len(row) >= 2:  
                review_text = row[0]
                label = int(row[1])
                reviews.append((review_text, label))
    return reviews

def build_vocabulary(reviews):
    vocab = set()
    for review, _ in reviews:
        for word in review.lower().split():
            vocab.add(word)
    return sorted(vocab)

def create_feature_vector(review, vocabulary):
    review_words = review.lower().split()
    feature_vector = []
    for word in vocabulary:
        if word in review_words:
            feature_vector.append(1)
        else:
            feature_vector.append(0)
    return feature_vector

def train_simple_model(reviews, vocabulary):
    positive_counts = [0] * len(vocabulary)
    negative_counts = [0] * len(vocabulary)

    for review, label in reviews:
        feature_vector = create_feature_vector(review, vocabulary)
        if label == 1:
            for i in range(len(vocabulary)):
                if feature_vector[i] == 1:
                    positive_counts[i] += 1
        else:
            for i in range(len(vocabulary)):
                if feature_vector[i] == 1:
                    negative_counts[i] += 1

    return positive_counts, negative_counts

def classify_review(review, vocabulary, positive_counts, negative_counts):
    feature_vector = create_feature_vector(review, vocabulary)
    positive_score = 0
    negative_score = 0

    for i in range(len(vocabulary)):
        if feature_vector[i] == 1:
            positive_score += positive_counts[i]
            negative_score += negative_counts[i]

    return "Positive" if positive_score > negative_score else "Negative"

def read_new_reviews(filename):
    new_reviews = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            if len(row) >= 1:  
                new_reviews.append(row[0])
    return new_reviews

def write_classifications_to_csv(filename, reviews_with_classifications):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Review', 'Classification'])
        for review, classification in reviews_with_classifications:
            writer.writerow([review, classification])


filename = 'classified_comments.csv'  
reviews = read_reviews_from_csv(filename)

vocabulary = build_vocabulary(reviews)
positive_counts, negative_counts = train_simple_model(reviews, vocabulary)


new_reviews_filename = 'cleaned_test.csv'  
new_reviews = read_new_reviews(new_reviews_filename)


results = []
for review in new_reviews:
    classification = classify_review(review, vocabulary, positive_counts, negative_counts)
    results.append((review, classification))


output_filename = 'classified_new_reviews.csv'  
write_classifications_to_csv(output_filename, results)

print(f"Classified reviews have been saved to {output_filename}")
