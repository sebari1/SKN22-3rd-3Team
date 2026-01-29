import unittest
import os
import sys

# Ensure src is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.text import tokenize_korean, get_kiwi

class TestTokenization(unittest.TestCase):
    def test_essential_terms(self):
        """Verify essential domain terms are treated as single tokens."""
        # Force reload or ensure dictionary is loaded (handled by get_kiwi singleton logic)
        
        # Test Case 1: Complex Breed Names
        text = "메인쿤과 아비시니안은 성격이 다르다."
        tokens = tokenize_korean(text)
        print(f"\n[Test 1] '{text}' -> {tokens}")
        self.assertIn("메인쿤", tokens)
        self.assertIn("아비시니안", tokens)
        
    def test_domain_terms(self):
        """Verify domain terms are recognized."""
        text = "집사는 맛동산을 캐기 위해 벤토나이트 모래를 샀다."
        tokens = tokenize_korean(text)
        print(f"\n[Test 2] '{text}' -> {tokens}")
        self.assertIn("집사", tokens)
        self.assertIn("맛동산", tokens)
        self.assertIn("벤토나이트", tokens)
        
    def test_stopwords(self):
        """Verify stopwords are removed."""
        text = "고양이가 밥을 먹었다."
        tokens = tokenize_korean(text)
        print(f"\n[Test 3] '{text}' -> {tokens}")
        self.assertNotIn("가", tokens.split())
        self.assertNotIn("을", tokens.split())
        self.assertIn("고양이", tokens)
        self.assertIn("밥", tokens)
        self.assertIn("먹", tokens) # VV '먹다' stem '먹'

if __name__ == '__main__':
    unittest.main()
