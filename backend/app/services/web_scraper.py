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
            "environmental": "/drivingingermany/environmental-zone-germany"
        }
    
    def get_page_content(self, url: str) -> Optional[str]:
        """Fetch content from a specific URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_relevant_sections(self, html_content: str, topic_keywords: List[str]) -> List[str]:
        """Extract relevant sections based on topic keywords"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script, style, navigation, header, footer elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()
        
        # Remove common navigation classes and IDs
        nav_selectors = [
            ".nav", ".navigation", ".menu", "#nav", "#navigation", "#menu",
            ".sidebar", ".header", ".footer", "[class*='nav']", "[id*='nav']"
        ]
        for selector in nav_selectors:
            for element in soup.select(selector):
                element.decompose()
        
        relevant_sections = []
        
        # Look for main content areas first
        main_content = soup.find(['main', 'article']) or soup.find('div', class_=re.compile(r'content|main|article'))
        if main_content:
            soup = main_content
        
        # Find sections containing the keywords in meaningful content
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'div'], string=True):
            text = element.get_text().lower()
            
            # Skip very short text or navigation-like text
            if len(text.strip()) < 20:
                continue
                
            # Skip if it looks like navigation (contains lots of links)
            links_count = len(element.find_all('a'))
            text_length = len(text)
            if links_count > 3 and text_length < 200:  # Likely navigation
                continue
            
            # Check if any keyword matches
            if any(keyword.lower() in text for keyword in topic_keywords):
                # Get the parent section for context
                section_text = self._extract_section_with_context(element)
                if section_text and len(section_text.strip()) > 100:  # Increase minimum content length
                    # Clean up the text
                    cleaned_text = self._clean_text(section_text)
                    if cleaned_text:
                        relevant_sections.append(cleaned_text)
        
        # If no specific matches, try to get the first few meaningful paragraphs
        if not relevant_sections:
            paragraphs = soup.find_all('p')
            for p in paragraphs[:5]:  # First 5 paragraphs
                text = p.get_text().strip()
                if len(text) > 50 and not self._is_navigation_text(text):
                    cleaned_text = self._clean_text(text)
                    if cleaned_text:
                        relevant_sections.append(cleaned_text)
        
        return relevant_sections[:3]  # Limit to top 3 most relevant sections
    
    def _clean_text(self, text: str) -> str:
        """Clean and format extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove common navigation phrases
        nav_phrases = [
            '× Home', 'Driver\'s Licence', 'Traffic Laws and Regulations',
            'Driving on Autobahn', 'Important Road Signs', 'Learn German Language'
        ]
        for phrase in nav_phrases:
            text = text.replace(phrase, '')
        
        # Remove sequences of navigation links
        text = re.sub(r'(Home|Driver\'s|License|Categories|Buying|Importing|Cars){3,}', '', text)
        
        # Clean up and return
        text = text.strip()
        return text if len(text) > 30 else None
    
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
            "environmental": "environmental"
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
        """Search Route to Germany website for driving information"""
        try:
            result = self.route_scraper.search_topic(query, language)
            if result:
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