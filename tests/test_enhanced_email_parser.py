import sys
import os
import unittest
from attached_assets.enhanced_email_parser import EnhancedEmailParser

class TestEnhancedEmailParser(unittest.TestCase):
    def setUp(self):
        self.parser = EnhancedEmailParser()
        
    def test_parse_basic_variables(self):
        """Test parsing of basic variables in email templates"""
        template = """
        Hello {{recipient_name}},
        
        Thank you for your interest in our company {{company_name}}.
        Your account has been created with email: {{email}}.
        
        Best regards,
        The {{company_name}} Team
        """
        
        variables = {
            "recipient_name": "John Doe",
            "company_name": "MailChats",
            "email": "john.doe@example.com"
        }
        
        parsed = self.parser.parse_template(template, variables)
        
        self.assertIn("Hello John Doe", parsed)
        self.assertIn("Thank you for your interest in our company MailChats", parsed)
        self.assertIn("Your account has been created with email: john.doe@example.com", parsed)
        self.assertIn("The MailChats Team", parsed)
        
    def test_fallback_values(self):
        """Test fallback values for missing variables"""
        template = """
        Hello {{recipient_name|Friend}},
        
        Your account: {{email|your email address}}
        """
        
        # Without providing variables
        parsed = self.parser.parse_template(template, {})
        
        self.assertIn("Hello Friend", parsed)
        self.assertIn("Your account: your email address", parsed)
        
        # With some variables provided
        parsed = self.parser.parse_template(template, {"email": "test@example.com"})
        
        self.assertIn("Hello Friend", parsed)
        self.assertIn("Your account: test@example.com", parsed)
        
    def test_enhanced_variables(self):
        """Test enhanced variables like domain extraction"""
        template = """
        Hello from {{domain}} ({{full_domain}}).
        
        Your company: {{company}}
        """
        
        variables = {
            "email": "user@mailchats.com",
            "domain": "should-be-overwritten"  # This should be overwritten
        }
        
        parsed = self.parser.parse_template(template, variables)
        
        # The domain should be extracted from the email
        self.assertIn("Hello from mailchats (mailchats.com)", parsed)
        self.assertIn("Your company: MailChats", parsed)
        
    def test_both_variable_formats(self):
        """Test support for both {var} and {{var}} formats"""
        template = """
        Single brace: {recipient_name}
        Double brace: {{recipient_name}}
        """
        
        variables = {
            "recipient_name": "John Doe"
        }
        
        parsed = self.parser.parse_template(template, variables)
        
        self.assertIn("Single brace: John Doe", parsed)
        self.assertIn("Double brace: John Doe", parsed)
        
if __name__ == '__main__':
    unittest.main()