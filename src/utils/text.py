import os
from kiwipiepy import Kiwi

# Singleton Kiwi instance
_kiwi = None

def get_kiwi():
    global _kiwi
    if _kiwi is None:
        _kiwi = Kiwi()
        # Try to load user dictionary if it exists
        # Assuming run from project root, or we need to find the path dynamically
        # Searching in standard locations
        possible_paths = [
            "data/v3/domain_dictionary.txt",
            "../data/v3/domain_dictionary.txt",
            "/Users/leemdo/Workspaces/SKN22-3rd-3Team/data/v3/domain_dictionary.txt"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"📚 Loading User Dictionary from: {path}")
                _kiwi.load_user_dictionary(path)
                break
    return _kiwi

STOPWORDS = {
    '이', '가', '을', '를', '은', '는', '의', '에', '로', '으로', '와', '과', '도', '만',
    '하', '있', '되', '않', '없', '주', '보', '싶', '나', '들', '것', '수', '등', '때'
}

def tokenize_korean(text: str) -> str:
    """
    Tokenizes Korean text using Kiwi (with Domain Dictionary).
    Extracts Nouns (NN*), Verbs (VV), Adjectives (VA), Roots (XR).
    Removes Stopwords.
    """
    if not text:
        return ""
        
    kiwi = get_kiwi()
    tokens = kiwi.tokenize(text)
    
    selected_tokens = []
    for t in tokens:
        # Filter tags: Noun, Verb, Adjective, Root
        if t.tag.startswith(('N', 'V', 'XR')):
            # Filter stopwords and 1-char non-nouns (optional, but good for noise reduction)
            if t.form not in STOPWORDS:
                selected_tokens.append(t.form)
    
    return " ".join(selected_tokens)
