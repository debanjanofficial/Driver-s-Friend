class IntentClassifier:
    def __init__(self):
        # In a real scenario, you might load a trained model here
        # e.g. self.model = joblib.load("path/to/model.pkl")
        pass

    def predict(self, processed_text: dict):
        """
        Predict an intent based on processed text.

        Args:
            processed_text (dict):
                - A dictionary containing tokens and entities from LanguageProcessor
                  Example: { 'tokens': [...], 'entities': [...] }

        Returns:
            An object with:
                - name: (str) the predicted intent
                - confidence: (float) confidence score
        """
        tokens = processed_text.get("tokens", [])
        tokens_lower = [t.lower() for t in tokens]

        # Naive rule-based logic:
        if any("speed" in tok for tok in tokens_lower):
            print ("Predicted intent: speed_limit (confidence: 0.9)")
            return type("Intent", (object,), {
                "name": "speed_limit",
                "confidence": 0.9
            })()
        elif any("alcohol" in tok or "drink" in tok for tok in tokens_lower):
            print("Predicted intent: alcohol_limit (confidence: 0.85)")
            return type("Intent", (object,), {
                "name": "alcohol_limit",
                "confidence": 0.85
            })()

        # Default fallback intent if no rules matched
        print("Predicted intent: unknown (confidence: 0.5)")
        return type("Intent", (object,), {
            "name": "unknown",
            "confidence": 0.5
        })()
