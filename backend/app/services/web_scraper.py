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
            "seatbelt": "/drivingingermany/city-driving",
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
        
        # Remove common navigation and unwanted elements
        unwanted_patterns = [
            r'×\s*Home.*?German Language Level A2',
            r'Home\s+Driver\'s.*?German Language Level A2',
            r'☰\s*Driving in Germany',
            r'Learn German Language.*?lets-learn-german\.com',
            r'This page contains the following topics:',
            r'To see the important.*?please visit.*',
            r'Learn German on Your Own.*?beginners',
            r'A self-study guide for beginners'
        ]
        
        for pattern in unwanted_patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove standalone navigation words
        nav_words = ['Home', 'Driver\'s Licence', 'Traffic Laws and Regulations', '×']
        for word in nav_words:
            text = text.replace(word, ' ')
        
        # Clean up extra spaces and format
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'\.([A-Z])', r'. \1', text)  # Add space after periods
        
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
            "seatbelt": "seatbelt",
            "seat belt": "seatbelt",
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
        """Create a summary from extracted sections with direct answer first"""
        if not sections:
            return "No relevant information found."
        
        # Extract the most relevant direct answer for the query
        direct_answer = self._extract_direct_answer(sections, query)
        
        # Clean and structure the additional details
        cleaned_sections = []
        for section in sections:
            # Apply additional cleaning to each section
            cleaned_section = self._clean_detailed_content(section)
            if cleaned_section and len(cleaned_section.strip()) > 30:
                cleaned_sections.append(cleaned_section)
        
        # Combine cleaned sections for additional details
        combined_text = '\n\n'.join(cleaned_sections)
        
        # Final cleanup
        combined_text = re.sub(r'\s+', ' ', combined_text)  # Remove extra whitespace
        combined_text = re.sub(r'\n+', '\n', combined_text)  # Remove extra newlines
        
        # Remove any remaining unwanted phrases
        unwanted_phrases = [
            "This page contains the following topics:",
            "To see the important",
            "please visit",
            "Learn German on Your Own",
            "A self-study guide for beginners"
        ]
        
        for phrase in unwanted_phrases:
            combined_text = re.sub(phrase, '', combined_text, flags=re.IGNORECASE)
        
        # Limit length for chat response
        if len(combined_text) > 2000:
            combined_text = combined_text[:2000] + "..."
        
        # Format: Direct answer first, then additional details
        if direct_answer and direct_answer != combined_text.strip():
            return f"{direct_answer}\n\nFor more details:\n\n{combined_text.strip()}"
        else:
            return combined_text.strip()
    
    def _clean_detailed_content(self, text: str) -> str:
        """Additional cleaning for detailed content sections"""
        # Remove unwanted patterns
        patterns_to_remove = [
            r'This page contains the following topics:.*?(\n|$)',
            r'To see the important.*?please visit.*?(\n|$)',
            r'Learn German on Your Own.*?beginners.*?(\n|$)',
            r'A self-study guide for beginners.*?(\n|$)',
            r'×\s*Home.*?German Language Level A2.*?(\n|$)',
            r'Home\s+Driver\'s.*?German Language Level A2.*?(\n|$)',
            r'☰\s*Driving in Germany.*?(\n|$)'
        ]
        
        for pattern in patterns_to_remove:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Clean up formatting
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'\.([A-Z])', r'. \1', text)  # Add space after periods
        
        # Remove standalone navigation words
        nav_words = ['Home', 'Driver\'s Licence', 'Traffic Laws and Regulations', '×']
        for word in nav_words:
            text = text.replace(word, ' ')
        
        # Final cleanup
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text if len(text) > 30 else ""
    
    def _extract_direct_answer(self, sections: List[str], query: str) -> str:
        """Extract the most direct answer to the query from sections"""
        query_lower = query.lower()
        query_words = query_lower.split()
        
        # Check what type of question this is
        is_speed_question = any(keyword in query_lower for keyword in ["speed", "limit", "velocity", "kmh", "mph", "fast", "slow", "geschwindigkeit", "limit", "schnell"])
        is_parking_question = any(keyword in query_lower for keyword in ["park", "parking", "parken", "parkplatz", "einparken"])
        is_alcohol_question = any(keyword in query_lower for keyword in ["alcohol", "drink", "bac", "promille", "alkohol", "trinken"])
        
        best_answer = ""
        best_score = 0
        
        for section in sections:
            section_lower = section.lower()
            
            # Skip sections that contain unwanted content
            if any(unwanted in section_lower for unwanted in ["this page contains", "to see the important", "learn german"]):
                continue
            
            # Extract all sentences from the section
            sentences = re.split(r'[.!?]+', section)
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) < 15:  # Skip very short sentences
                    continue
                
                sentence_lower = sentence.lower()
                score = 0
                
                # Score based on keyword matches
                for word in query_words:
                    if word in sentence_lower:
                        score += len(word) * 2  # Higher weight for direct matches
                
                # Bonus for specific patterns based on question type
                if is_speed_question:
                    if any(pattern in sentence_lower for pattern in ["km/h", "kmh", "mph", "50 km", "30 km", "100 km", "130 km"]):
                        score += 15
                    if "speed limit" in sentence_lower:
                        score += 12
                    if "normal speed limit" in sentence_lower:
                        score += 10
                        
                elif is_parking_question:
                    if any(pattern in sentence_lower for pattern in ["park", "parking", "parken"]):
                        score += 10
                    if "regulation" in sentence_lower:
                        score += 8
                        
                elif is_alcohol_question:
                    if any(pattern in sentence_lower for pattern in ["0.5", "0.05", "promille", "bac", "alcohol"]):
                        score += 15
                    if "limit" in sentence_lower:
                        score += 10
                
                # Look for sentences with specific numbers (often contain direct answers)
                if re.search(r'\b\d+\s*(km/h|mph|promille|%|euros?|€)\b', sentence_lower):
                    score += 8
                
                # Penalty for sentences that look like navigation or metadata
                if any(nav in sentence_lower for nav in ["page contains", "topics", "visit", "learn german"]):
                    score -= 20
                
                # Update best answer if this sentence scores higher
                if score > best_score and score > 5:  # Minimum threshold increased
                    best_score = score
                    best_answer = sentence
        
        # If no good sentence found, try to find the best paragraph
        if not best_answer:
            for section in sections:
                section_lower = section.lower()
                if any(unwanted in section_lower for unwanted in ["this page contains", "to see the important", "learn german"]):
                    continue
                
                score = 0
                for word in query_words:
                    if word in section_lower:
                        score += len(word)
                
                if is_speed_question and "speed limit" in section_lower:
                    score += 10
                elif is_alcohol_question and "alcohol" in section_lower:
                    score += 10
                elif is_parking_question and "parking" in section_lower:
                    score += 10
                
                if score > best_score and score > 3:
                    best_score = score
                    # Take first 200 characters of the best section
                    best_answer = section[:200] + ("..." if len(section) > 200 else "")
        
        return best_answer.strip()

class GettingAroundGermanyScraper:
    def __init__(self):
        self.base_url = "https://www.gettingaroundgermany.info"
        self.main_page_url = f"{self.base_url}/regeln.shtml"
        
        # Topic mapping for keywords to sections
        self.topic_mapping = {
            "license": "licensing",
            "licence": "licensing", 
            "driving license": "licensing",
            "speed": "speed limits",
            "autobahn": "autobahn traffic regulations",
            "parking": "parking regulations",
            "right": "right-of-way",
            "priority": "right-of-way",
            "alcohol": "drinking and driving",
            "drink": "drinking and driving",
            "accident": "accidents",
            "insurance": "general laws and enforcement",
            "seatbelt": "general laws and enforcement",
            "safety": "general laws and enforcement",
            "enforcement": "general laws and enforcement",
            "fine": "general laws and enforcement",
            "penalty": "general laws and enforcement",
            "bicycle": "bicycle lanes, streets, and zones",
            "bike": "bicycle lanes, streets, and zones",
            "urban": "urban traffic regulations",
            "city": "urban traffic regulations",
            "traffic": "traffic calming zones",
            "calm": "traffic calming zones",
            "pass": "passing/overtaking",
            "overtake": "passing/overtaking",
            "phone": "additional prohibitions",
            "mobile": "additional prohibitions"
        }
    
    def get_page_content(self, url: str) -> Optional[str]:
        """Fetch content from a specific URL with timeout protection"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_section_content(self, html_content: str, section_title: str) -> Optional[str]:
        """Extract content for a specific section from the main page"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find the section heading
            section_heading = None
            for heading in soup.find_all(['h2', 'h3']):
                if section_title.lower() in heading.get_text().lower():
                    section_heading = heading
                    break
            
            if not section_heading:
                return None
                
            # Extract content until next section or end
            content_parts = []
            current = section_heading.find_next_sibling()
            
            while current and current.name not in ['h2', 'h3']:
                if current.name in ['p', 'ul', 'ol', 'div']:
                    text = current.get_text().strip()
                    if text and len(text) > 20:  # Filter out very short content
                        content_parts.append(text)
                current = current.find_next_sibling()
                
                # Limit to prevent too much content
                if len(content_parts) >= 8:
                    break
            
            if content_parts:
                return '\n\n'.join(content_parts)
            return None
            
        except Exception as e:
            logger.error(f"Error extracting section content: {e}")
            return None
    
    def search_topic(self, query: str, language: str = "en") -> Optional[Dict]:
        """Search for information on a specific topic"""
        query_lower = query.lower()
        
        # Find best matching section
        matched_section = None
        for keyword, section in self.topic_mapping.items():
            if keyword in query_lower:
                matched_section = section
                break
        
        if not matched_section:
            matched_section = "general laws and enforcement"  # Default fallback
        
        # Fetch the main page
        html_content = self.get_page_content(self.main_page_url)
        if not html_content:
            return None
        
        # Extract section content
        section_content = self.extract_section_content(html_content, matched_section)
        if not section_content:
            return None
        
        # Create summary
        summary = self._create_summary([section_content], query)
        
        return {
            "summary": summary,
            "url": self.main_page_url,
            "topic": matched_section,
            "source": "gettingaroundgermany.info"
        }
    
    def _create_summary(self, sections: List[str], query: str = "") -> str:
        """Create a summary from extracted sections with direct answer first"""
        if not sections:
            return "No relevant information found."
        
        # Extract the most relevant direct answer for the query
        direct_answer = self._extract_direct_answer(sections, query)
        
        # Combine sections for additional details
        combined_text = '\n\n'.join(sections)
        
        # Basic cleanup
        combined_text = re.sub(r'\s+', ' ', combined_text)  # Remove extra whitespace
        combined_text = re.sub(r'\n+', '\n', combined_text)  # Remove extra newlines
        
        # Limit length for chat response
        if len(combined_text) > 2000:
            combined_text = combined_text[:2000] + "..."
        
        # Format: Direct answer first, then additional details
        if direct_answer and direct_answer != combined_text.strip():
            return f"{direct_answer}\n\nFor more details:\n\n{combined_text.strip()}"
        else:
            return combined_text.strip()
    
    def _extract_direct_answer(self, sections: List[str], query: str) -> str:
        """Extract the most direct answer to the query from sections"""
        query_lower = query.lower()
        query_words = query_lower.split()
        
        # Keywords that indicate different question types
        speed_keywords = ["speed", "limit", "velocity", "kmh", "mph", "fast", "slow", "geschwindigkeit", "limit", "schnell"]
        parking_keywords = ["park", "parking", "parken", "parkplatz", "einparken"]
        alcohol_keywords = ["alcohol", "drink", "bac", "promille", "alkohol", "trinken"]
        
        # Check what type of question this is
        is_speed_question = any(keyword in query_lower for keyword in speed_keywords)
        is_parking_question = any(keyword in query_lower for keyword in parking_keywords)
        is_alcohol_question = any(keyword in query_lower for keyword in alcohol_keywords)
        
        best_answer = ""
        best_score = 0
        
        for section in sections:
            section_lower = section.lower()
            score = 0
            
            # Score based on keyword matches
            for word in query_words:
                if word in section_lower:
                    score += len(word)  # Longer words get higher scores
            
            # Bonus for specific patterns
            if is_speed_question:
                if any(pattern in section_lower for pattern in ["km/h", "kmh", "mph", "50 km", "30 km", "100 km", "130 km"]):
                    score += 10
                if "speed limit" in section_lower or "geschwindigkeitsbegrenzung" in section_lower:
                    score += 8
                    
            elif is_parking_question:
                if any(pattern in section_lower for pattern in ["park", "parking", "parken"]):
                    score += 10
                if "regulation" in section_lower or "vorschrift" in section_lower:
                    score += 5
                    
            elif is_alcohol_question:
                if any(pattern in section_lower for pattern in ["0.5", "0.05", "promille", "bac", "alcohol"]):
                    score += 10
                if "limit" in section_lower or "grenze" in section_lower:
                    score += 8
            
            # Look for sentences with numbers (often contain specific limits)
            if re.search(r'\b\d+\s*(km/h|mph|promille|%|euros?|€)\b', section_lower):
                score += 5
            
            # Update best answer if this section scores higher
            if score > best_score and score > 3:  # Minimum threshold
                best_score = score
                # Extract the most relevant sentence or paragraph
                sentences = re.split(r'[.!?]+', section)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 20 and any(word in sentence.lower() for word in query_words):
                        best_answer = sentence
                        break
                
                # If no good sentence found, use the first part of the section
                if not best_answer:
                    best_answer = section[:200] + ("..." if len(section) > 200 else "")
        
        return best_answer.strip()

class WebSearchService:
    def __init__(self):
        self.route_scraper = RouteToGermanyScraper()
        self.getting_around_scraper = GettingAroundGermanyScraper()
    
    def search_route_to_germany(self, query: str, language: str = "en") -> Optional[Dict]:
        """Search both websites for driving information with intelligent fallback"""
        # Try both sources and compare relevance
        primary_result = self._search_primary_source(query, language)
        secondary_result = self._search_secondary_source(query, language)
        
        # If only one source has results, use it
        if primary_result and not secondary_result:
            result = primary_result
        elif secondary_result and not primary_result:
            result = secondary_result
        elif not primary_result and not secondary_result:
            return None
        else:
            # If both have results, check relevance and prefer the more relevant one
            primary_relevance = self._calculate_relevance(query, primary_result.get("response", ""))
            secondary_relevance = self._calculate_relevance(query, secondary_result.get("response", ""))
            
            # If secondary is significantly more relevant, use it
            if secondary_relevance > primary_relevance + 0.2:  # 20% threshold
                result = secondary_result
            else:
                result = primary_result  # Default to primary if relevance is similar
        
        # Handle German language requests
        if language == "de" and result:
            result = self._handle_german_response(result)
            
        return result
    
    def _handle_german_response(self, result: Dict) -> Dict:
        """Handle German language response - add note about English source"""
        original_response = result.get("response", "")
        german_note = "\n\n[Hinweis: Diese Informationen stammen aus englischsprachigen Quellen, da deutsche Versionen nicht verfügbar sind.]"
        
        # Add German note to the response
        result["response"] = original_response + german_note
        return result
    
    def _calculate_relevance(self, query: str, content: str) -> float:
        """Calculate how relevant the content is to the query"""
        if not content:
            return 0.0
            
        query_words = query.lower().split()
        content_lower = content.lower()
        
        # Count query word matches in content
        matches = sum(1 for word in query_words if word in content_lower)
        relevance = matches / len(query_words) if query_words else 0
        
        # Bonus for exact phrase matches
        if query.lower() in content_lower:
            relevance += 0.3
            
        return min(relevance, 1.0)  # Cap at 1.0
    
    def _search_primary_source(self, query: str, language: str) -> Optional[Dict]:
        """Search Route to Germany website"""
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
        except Exception as e:
            logger.error(f"Error searching Route to Germany: {e}")
        return None
    
    def _search_secondary_source(self, query: str, language: str) -> Optional[Dict]:
        """Search GettingAroundGermany website as fallback"""
        try:
            result = self.getting_around_scraper.search_topic(query, language)
            if result and result.get("summary") and len(result["summary"].strip()) > 50:
                return {
                    "response": result["summary"],
                    "source": "gettingaroundgermany.info", 
                    "url": result["url"],
                    "topic": result["topic"],
                    "intent": "web_search",
                    "confidence": 0.80  # Slightly lower confidence for secondary source
                }
        except Exception as e:
            logger.error(f"Error searching GettingAroundGermany: {e}")
        return None
