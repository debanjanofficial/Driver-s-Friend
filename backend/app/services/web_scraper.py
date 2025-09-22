import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import time
import re
from urllib.parse import urljoin, urlparse
import logging

logger = logging.getLogger(__name__)

class RouteToGermanyScraper:
    def __init__(self):
        self.base_url = "https://routetogermany.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # URL mapping for different topics
        self.topic_urls = {
            "speed_limit": "/drivingingermany/city-driving",
            "autobahn": "/drivingingermany/autobahn",
            "parking": "/drivingingermany/parking",
            "right_of_way": "/drivingingermany/right-of-way",
            "traffic_signs": "/drivingingermany/road-signs-germany",
            "alcohol_limit": "/drivingingermany/fines-on-violations",
            "license": "/drivingingermany/driving-license",
            "safety": "/drivingingermany/city-driving",
            "accident": "/drivingingermany/accident",
            "insurance": "/drivingingermany/insurance",
            "fines": "/drivingingermany/fines-on-violations",
            "tires": "/drivingingermany/tires-regulations",
            "environmental": "/drivingingermany/environmental-zone-germany",
            "tuning": "/drivingingermany/performance-tuning"
        }
    
    def get_page_content(self, url: str) -> Optional[str]:
        """Fetch content from a specific URL with timeout protection"""
        try:
            response = self.session.get(url, timeout=5)  # Reduced timeout to 5 seconds
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            return None
    
    def extract_relevant_sections(self, html_content: str, topic_keywords: List[str]) -> List[str]:
        """Extract relevant sections based on topic keywords"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script, style, navigation elements
        for element in soup(["script", "style", "nav", "header", "footer"]):
            element.decompose()
        
        relevant_sections = []
        
        # Get all paragraphs and meaningful text blocks
        content_elements = soup.find_all(['p', 'div', 'li', 'h1', 'h2', 'h3'])
        
        for element in content_elements:
            text = element.get_text().strip()
            
            # Skip very short content or navigation-like content
            if len(text) < 30:
                continue
                
            # Skip if it's mostly navigation (lots of short words/links)
            words = text.split()
            if len(words) < 5:
                continue
                
            # Check for keyword relevance
            text_lower = text.lower()
            keyword_matches = sum(1 for keyword in topic_keywords if keyword.lower() in text_lower)
            
            # If keywords match or it's a substantial paragraph, include it
            if keyword_matches > 0 or len(text) > 100:
                # Clean up the text
                cleaned_text = self._clean_text(text)
                if cleaned_text and len(cleaned_text) > 50:
                    relevant_sections.append(cleaned_text)
        
        # If we found content, return it; otherwise get the main content
        if relevant_sections:
            return relevant_sections[:5]  # Return more sections
        else:
            # Fallback: get main paragraphs from the page
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 50:
                    cleaned = self._clean_text(text)
                    if cleaned:
                        relevant_sections.append(cleaned)
                        if len(relevant_sections) >= 3:
                            break
            return relevant_sections
    
    def _clean_text(self, text: str) -> str:
        """Clean and format extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common navigation elements that appear in content
        nav_patterns = [
            r'×\s*Home.*?German Language Level A2',
            r'Home\s+Driver\'s.*?German Language Level A2',
            r'☰\s*Driving in Germany',
            r'Learn German Language.*?lets-learn-german\.com'
        ]
        
        for pattern in nav_patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove standalone navigation words
        nav_words = ['Home', 'Driver\'s Licence', 'Traffic Laws and Regulations', '×']
        for word in nav_words:
            text = text.replace(word, ' ')
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text if len(text) > 20 else None
    
    def _is_navigation_text(self, text: str) -> bool:
        """Check if text looks like navigation"""
        nav_indicators = ['home', 'driver\'s licence', 'categories', 'buying', 'importing', 'regulations']
        text_lower = text.lower()
        nav_count = sum(1 for indicator in nav_indicators if indicator in text_lower)
        return nav_count > 2
    
    def _extract_section_with_context(self, element) -> str:
        """Extract a section with surrounding context"""
        # Try to get a meaningful section (paragraph, list item, or div)
        if element.name in ['p', 'li']:
            return element.get_text().strip()
        elif element.name in ['h1', 'h2', 'h3', 'h4']:
            # Get the header and the next few elements
            content = [element.get_text().strip()]
            next_elem = element.find_next_sibling()
            count = 0
            while next_elem and count < 3:
                if next_elem.name in ['p', 'ul', 'ol', 'div']:
                    text = next_elem.get_text().strip()
                    if text:
                        content.append(text)
                        count += 1
                elif next_elem.name in ['h1', 'h2', 'h3', 'h4']:
                    break  # Stop at next header
                next_elem = next_elem.find_next_sibling()
            return '\n'.join(content)
        else:
            return element.get_text().strip()
    
    def search_topic(self, query: str, language: str = "en") -> Optional[Dict]:
        """Search for information on a specific topic"""
        # Identify the most relevant topic URL based on keywords
        query_lower = query.lower()
        
        # Map query keywords to topic categories
        topic_mapping = {
            "speed": "speed_limit",
            "limit": "speed_limit", 
            "autobahn": "autobahn",
            "highway": "autobahn",
            "park": "parking",
            "parking": "parking",
            "right": "right_of_way",
            "way": "right_of_way",
            "priority": "right_of_way",
            "sign": "traffic_signs",
            "traffic": "traffic_signs",
            "alcohol": "alcohol_limit",
            "drink": "alcohol_limit",
            "license": "license",
            "licence": "license",
            "safety": "safety",
            "seatbelt": "safety",
            "accident": "accident",
            "insurance": "insurance",
            "fine": "fines",
            "penalty": "fines",
            "tire": "tires",
            "winter": "tires",
            "environmental": "environmental",
            "tuning": "tuning",
            "performance": "tuning", 
            "modification": "tuning"
        }
        
        # Find the best matching topic
        matched_topic = None
        for keyword, topic in topic_mapping.items():
            if keyword in query_lower:
                matched_topic = topic
                break
        
        if not matched_topic:
            matched_topic = "speed_limit"  # Default fallback
        
        # Get the URL for the topic
        topic_url = self.topic_urls.get(matched_topic, "/drivingingermany/city-driving")
        full_url = urljoin(self.base_url, topic_url)
        
        # Fetch content
        html_content = self.get_page_content(full_url)
        if not html_content:
            return None
        
        # Extract relevant sections
        query_keywords = query.split()
        relevant_sections = self.extract_relevant_sections(html_content, query_keywords)
        
        if relevant_sections:
            return {
                "source": "routetogermany.com",
                "url": full_url,
                "topic": matched_topic,
                "content": relevant_sections,
                "summary": self._create_summary(relevant_sections, query)
            }
        
        return None
    
    def _create_summary(self, sections: List[str], query: str) -> str:
        """Create a summary from extracted sections"""
        if not sections:
            return "No relevant information found."
        
        # Combine sections and clean up
        combined_text = '\n\n'.join(sections)
        
        # Basic cleanup
        combined_text = re.sub(r'\s+', ' ', combined_text)  # Remove extra whitespace
        combined_text = re.sub(r'\n+', '\n', combined_text)  # Remove extra newlines
        
        # Limit length for chat response
        if len(combined_text) > 800:
            combined_text = combined_text[:800] + "..."
        
        return combined_text.strip()

class WebSearchService:
    def __init__(self):
        self.route_scraper = RouteToGermanyScraper()
    
    def search_route_to_germany(self, query: str, language: str = "en") -> Optional[Dict]:
        """Search Route to Germany website for driving information with error protection"""
        try:
            result = self.route_scraper.search_topic(query, language)
            if result and result.get("summary") and len(result["summary"].strip()) > 50:
                return {
                    "response": result["summary"],
                    "source": "routetogermany.com",
                    "url": result["url"],
                    "topic": result["topic"],
                    "intent": "web_search",
                    "confidence": 0.85
                }
            return None
        except Exception as e:
            logger.error(f"Error searching Route to Germany: {e}")
            return None