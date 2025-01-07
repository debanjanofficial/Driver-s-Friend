from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class IntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        
    def train(self, training_data, language):
        X = []
        y = []
        for intent_data in training_data[language]:
            intent = intent_data['intent']
            for example in intent_data['examples']:
                X.append(example)
                y.append(intent)
                
        X_vectorized = self.vectorizer.fit_transform(X)
        self.classifier.fit(X_vectorized, y)

