import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from attached_assets.enhanced_email_parser import EnhancedEmailParser

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.parser = EnhancedEmailParser()
    
    def test_parser_initialization(self):
        """Test that the parser initializes correctly"""
        self.assertIsNotNone(self.parser)
    
    def test_parse_simple_email(self):
        """Test parsing a simple email address"""
        result = self.parser.parse_recipient_line("test@example.com")
        self.assertEqual(result["email"], "test@example.com")
        self.assertEqual(result["emailname"], "test")
        self.assertEqual(result["domain"], "example.com")
    
    def test_parse_complex_recipient(self):
        """Test parsing a recipient with additional fields"""
        result = self.parser.parse_recipient_line("test@example.com|firstname=John|lastname=Doe|company=Acme Inc")
        self.assertEqual(result["email"], "test@example.com")
        self.assertEqual(result["firstname"], "John")
        self.assertEqual(result["lastname"], "Doe")
        self.assertEqual(result["company"], "Acme Inc")
    
    def test_mail_merge_simple(self):
        """Test simple mail merge functionality"""
        template = "Hello, {emailname}! Your email is {email}."
        result = self.parser.apply_enhanced_mail_merge(template, "test@example.com")
        self.assertEqual(result, "Hello, test! Your email is test@example.com.")
    
    def test_mail_merge_double_braces(self):
        """Test mail merge with double braces"""
        template = "Hello, {{emailname}}! Your domain is {{domain}}."
        result = self.parser.apply_enhanced_mail_merge(template, "test@example.com")
        self.assertEqual(result, "Hello, test! Your domain is example.com.")
    
    def test_mail_merge_with_custom_fields(self):
        """Test mail merge with custom fields"""
        template = "Dear {{firstname}} {{lastname}} from {{company}}, your email is {{email}}."
        result = self.parser.apply_enhanced_mail_merge(template, 
                                                     "test@example.com|firstname=John|lastname=Doe|company=Acme Inc")
        self.assertEqual(result, "Dear John Doe from Acme Inc, your email is test@example.com.")

if __name__ == '__main__':
    unittest.main()