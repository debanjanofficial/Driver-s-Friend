from app.database.operations import DatabaseOperations
from app.nlp.processor import LanguageProcessor

class SearchService:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.processor = LanguageProcessor()
    
    async def search_regulations(self, query: str, language: str, category: str = None, limit: int = 10):
        """
        Search for regulations based on a text query
        
        Args:
            query: The search text from user
            language: Language code (e.g., 'en-US', 'de')
            category: Optional category filter
            limit: Maximum number of results to return
            
        Returns:
            List of matching regulations
        """
        # Extract keywords from the query
        keywords = self.processor.extract_keywords(query, language.split('-')[0])
        
        # Get results from database
        results = self.db_ops.search_regulations(keywords, language)
        
        # Filter by category if provided
        if category and results:
            results = [r for r in results if r.get("category") == category]
        
        # Limit results
        results = results[:limit]
        
        return {
            "results": results,
            "query": query,
            "matched_keywords": keywords,
            "total_results": len(results)
        }