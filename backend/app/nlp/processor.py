import spacy
import torch
class LanguageProcessor:
    def __init__(self, device=torch.device("mps" if torch.backends.mps.is_available() else "cpu")):  # Apple MPS or CPU fallback
        self.device = device
        self.nlp = {
            'en': spacy.load('en_core_web_sm'),
            'en_us': spacy.load('en_core_web_sm'),
            'en_gb': spacy.load('en_core_web_sm'),
            'en_in': spacy.load('en_core_web_sm'),
            'de': spacy.load('de_core_news_sm')
        }
        
    def extract_keywords(self, text, language = 'en'):
        nlp = self.nlp.get(language, self.nlp['en'])
        doc = nlp(text)
        return [token.text.lower() for token in doc if token.is_alpha]
    
    def process_text(self, text, language='en'):
        nlp = self.nlp.get(language, self.nlp['en'])
        doc = nlp(text)
        return {
            'tokens': [token.text for token in doc],
            'entities': [(ent.text, ent.label_) for ent in doc.ents]
        }
