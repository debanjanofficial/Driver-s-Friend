class LanguageProcessor:
    def __init__(self):
        self.nlp_en = spacy.load('en_core_web_sm')
        self.nlp_de = spacy.load('de_core_news_sm')
        
    def process_query(self, text, language='en'):
        nlp = self.nlp_en if language.startswith('en') else self.nlp_de
        return nlp(text)