"""
Sign Language Dictionary and Learning Resources
"""
from typing import Dict, List, Optional, Tuple
import json

class SignDictionary:
    """
    Comprehensive sign language dictionary with ASL mappings
    """
    
    def __init__(self):
        # Basic vocabulary with sign descriptions
        self.vocabulary = {
            # Greetings
            "hello": {
                "category": "greeting",
                "description": "Open hand, palm facing out, move in small wave",
                "difficulty": "beginner",
                "hand_shape": "open_palm",
                "movement": "wave",
                "orientation": "forward"
            },
            "goodbye": {
                "category": "greeting", 
                "description": "Open hand, fingers together, wave side to side",
                "difficulty": "beginner",
                "hand_shape": "open_palm",
                "movement": "wave",
                "orientation": "forward"
            },
            "thank_you": {
                "category": "greeting",
                "description": "Flat hand starts at chin, moves forward",
                "difficulty": "beginner",
                "hand_shape": "flat",
                "movement": "forward_arc",
                "orientation": "palm_in"
            },
            "please": {
                "category": "greeting",
                "description": "Flat hand circles on chest",
                "difficulty": "beginner",
                "hand_shape": "flat",
                "movement": "circular",
                "orientation": "chest"
            },
            "sorry": {
                "category": "greeting",
                "description": "Closed fist circles on chest",
                "difficulty": "beginner",
                "hand_shape": "fist",
                "movement": "circular",
                "orientation": "chest"
            },
            
            # Common words
            "yes": {
                "category": "response",
                "description": "Closed fist nods up and down",
                "difficulty": "beginner",
                "hand_shape": "fist",
                "movement": "nodding",
                "orientation": "forward"
            },
            "no": {
                "category": "response",
                "description": "Index and middle finger tap thumb",
                "difficulty": "beginner",
                "hand_shape": "modified_n",
                "movement": "tap",
                "orientation": "forward"
            },
            "help": {
                "category": "action",
                "description": "Flat hand on opposite fist, both lift up",
                "difficulty": "beginner",
                "hand_shape": "flat_on_fist",
                "movement": "lift",
                "orientation": "upward"
            },
            "stop": {
                "category": "action",
                "description": "Flat hand chops down on opposite palm",
                "difficulty": "beginner",
                "hand_shape": "flat",
                "movement": "chop",
                "orientation": "downward"
            },
            "wait": {
                "category": "action",
                "description": "Both hands wiggle fingers facing up",
                "difficulty": "beginner",
                "hand_shape": "wiggling_fingers",
                "movement": "wiggle",
                "orientation": "upward"
            },
            
            # Numbers
            "one": {
                "category": "number",
                "description": "Index finger up",
                "difficulty": "beginner",
                "hand_shape": "index_up",
                "movement": "static",
                "orientation": "upward"
            },
            "two": {
                "category": "number",
                "description": "Index and middle finger up",
                "difficulty": "beginner",
                "hand_shape": "peace_sign",
                "movement": "static",
                "orientation": "upward"
            },
            "three": {
                "category": "number",
                "description": "Index, middle, and ring finger up",
                "difficulty": "beginner",
                "hand_shape": "three_fingers",
                "movement": "static",
                "orientation": "upward"
            },
            
            # Questions
            "what": {
                "category": "question",
                "description": "Both hands palm up, shake side to side",
                "difficulty": "intermediate",
                "hand_shape": "open_palms",
                "movement": "shake",
                "orientation": "upward"
            },
            "where": {
                "category": "question",
                "description": "Index finger up, shake side to side",
                "difficulty": "intermediate",
                "hand_shape": "index_up",
                "movement": "shake",
                "orientation": "upward"
            },
            "when": {
                "category": "question",
                "description": "Index finger circles around opposite index",
                "difficulty": "intermediate",
                "hand_shape": "index_fingers",
                "movement": "circular",
                "orientation": "forward"
            },
            "why": {
                "category": "question",
                "description": "Middle fingers on forehead, move forward to 'Y' shape",
                "difficulty": "intermediate",
                "hand_shape": "middle_finger",
                "movement": "forward",
                "orientation": "forehead"
            },
            "how": {
                "category": "question",
                "description": "Bent fingers together, twist outward",
                "difficulty": "intermediate",
                "hand_shape": "bent_fingers",
                "movement": "twist",
                "orientation": "forward"
            }
        }
        
        # Alphabet for finger spelling
        self.alphabet = {
            'a': 'Closed fist with thumb on side',
            'b': 'Flat fingers up, thumb across palm',
            'c': 'Curved hand in C shape',
            'd': 'Index finger up, others touch thumb',
            'e': 'Fingers bent, touching thumb',
            'f': 'Index and thumb circle, others up',
            'g': 'Index pointing sideways, thumb up',
            'h': 'Index and middle sideways',
            'i': 'Pinky up, fist closed',
            'j': 'Pinky up, draw J in air',
            'k': 'Index up, middle forward, thumb between',
            'l': 'L shape with index and thumb',
            'm': 'Three fingers over thumb',
            'n': 'Two fingers over thumb',
            'o': 'Fingers and thumb form O',
            'p': 'Like K but pointing down',
            'q': 'Like G but pointing down',
            'r': 'Index and middle crossed',
            's': 'Closed fist with thumb over fingers',
            't': 'Thumb between index and middle',
            'u': 'Index and middle up together',
            'v': 'Peace sign',
            'w': 'Three fingers up',
            'x': 'Index bent like hook',
            'y': 'Thumb and pinky out',
            'z': 'Index draws Z in air'
        }
        
        # Common phrases
        self.phrases = {
            "how are you": ["how", "you"],
            "nice to meet you": ["nice", "meet", "you"],
            "what's your name": ["what", "your", "name"],
            "i love you": ["i", "love", "you"],
            "thank you very much": ["thank_you", "very", "much"],
            "i don't understand": ["i", "not", "understand"],
            "can you help me": ["you", "help", "me", "please"],
            "excuse me": ["excuse", "me"],
            "i'm sorry": ["i", "sorry"]
        }
    
    def get_sign(self, word: str) -> Optional[Dict]:
        """Get sign information for a word"""
        return self.vocabulary.get(word.lower())
    
    def get_letter(self, letter: str) -> Optional[str]:
        """Get finger spelling for a letter"""
        return self.alphabet.get(letter.lower())
    
    def finger_spell(self, word: str) -> List[str]:
        """Convert word to finger spelling sequence"""
        return [self.alphabet.get(letter.lower(), '') for letter in word if letter.isalpha()]
    
    def get_phrase_signs(self, phrase: str) -> List[str]:
        """Break down phrase into signs"""
        phrase_lower = phrase.lower()
        
        # Check if it's a known phrase
        if phrase_lower in self.phrases:
            return self.phrases[phrase_lower]
        
        # Otherwise, break into words and check each
        words = phrase_lower.split()
        signs = []
        
        for word in words:
            if word in self.vocabulary:
                signs.append(word)
            else:
                # Finger spell unknown words
                signs.extend([f"[{letter}]" for letter in word])
        
        return signs
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        categories = set()
        for sign_info in self.vocabulary.values():
            categories.add(sign_info['category'])
        return sorted(list(categories))
    
    def get_signs_by_category(self, category: str) -> Dict[str, Dict]:
        """Get all signs in a category"""
        return {
            word: info 
            for word, info in self.vocabulary.items() 
            if info['category'] == category
        }
    
    def get_signs_by_difficulty(self, difficulty: str) -> Dict[str, Dict]:
        """Get all signs by difficulty level"""
        return {
            word: info 
            for word, info in self.vocabulary.items() 
            if info['difficulty'] == difficulty
        }
    
    def search_signs(self, query: str) -> Dict[str, Dict]:
        """Search signs by word or description"""
        query_lower = query.lower()
        results = {}
        
        for word, info in self.vocabulary.items():
            if (query_lower in word or 
                query_lower in info['description'].lower() or
                query_lower in info['category']):
                results[word] = info
        
        return results
    
    def get_learning_path(self, level: str = "beginner") -> List[Dict]:
        """Get recommended learning path for a level"""
        paths = {
            "beginner": [
                {"lesson": "Basic Greetings", "signs": ["hello", "goodbye", "thank_you", "please"]},
                {"lesson": "Yes and No", "signs": ["yes", "no"]},
                {"lesson": "Essential Actions", "signs": ["help", "stop", "wait"]},
                {"lesson": "Numbers 1-3", "signs": ["one", "two", "three"]},
                {"lesson": "Alphabet A-E", "letters": ["a", "b", "c", "d", "e"]}
            ],
            "intermediate": [
                {"lesson": "Question Words", "signs": ["what", "where", "when", "why", "how"]},
                {"lesson": "Common Phrases", "phrases": ["how are you", "nice to meet you"]},
                {"lesson": "Full Alphabet", "letters": list(self.alphabet.keys())},
                {"lesson": "Numbers 1-10", "signs": ["one", "two", "three", "four", "five"]}
            ]
        }
        
        return paths.get(level, paths["beginner"])
    
    def to_json(self) -> str:
        """Export dictionary as JSON"""
        return json.dumps({
            "vocabulary": self.vocabulary,
            "alphabet": self.alphabet,
            "phrases": self.phrases
        }, indent=2)