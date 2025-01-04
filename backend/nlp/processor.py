import spacy

class LanguageProcessor:
    def __init__(self):
        self.nlp_models = {
            'en': spacy.load('en_core_web_sm'),
            'de': spacy.load('de_core_news_sm')
        }
    
    def process_text(self, text, language='en'):
        nlp = self.nlp_models.get(language, self.nlp_models['en'])
        doc = nlp(text)
        return {
            'tokens': [token.text for token in doc],
            'entities': [(ent.text, ent.label_) for ent in doc.ents]
        }
