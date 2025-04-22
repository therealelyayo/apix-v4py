import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tempfile
import json
from attached_assets.send_email import send_email, validate_email, parse_template

class TestSendEmail(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary config file for testing
        self.temp_config = tempfile.NamedTemporaryFile(delete=False, mode='w+')
        config = {
            "smtp_server": "mail.example.com",
            "smtp_port": 587,
            "username": "test@example.com",
            "password": "testpassword",
            "default_from": "noreply@example.com"
        }
        json.dump(config, self.temp_config)
        self.temp_config.close()
        
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_config.name):
            os.unlink(self.temp_config.name)
            
    @patch('attached_assets.send_email.validate_email')
    def test_validate_email(self, mock_validate):
        """Test email validation function"""
        # Test valid email
        mock_validate.return_value = True
        self.assertTrue(validate_email("test@example.com"))
        
        # Test invalid email
        mock_validate.return_value = False
        self.assertFalse(validate_email("invalid-email"))
        
    def test_parse_template(self):
        """Test template parsing function"""
        template = "Hello {{name}}, your email is {{email}}."
        variables = {
            "name": "John",
            "email": "john@example.com"
        }
        
        result = parse_template(template, variables)
        self.assertEqual(result, "Hello John, your email is john@example.com.")
        
        # Test with missing variables
        result = parse_template(template, {"name": "John"})
        self.assertEqual(result, "Hello John, your email is {{email}}.")
        
    @patch('attached_assets.send_email.smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test successful email sending"""
        # Setup SMTP mock
        smtp_instance = MagicMock()
        mock_smtp.return_value = smtp_instance
        
        result = send_email(
            recipient="test@example.com",
            subject="Test Subject",
            body="Test Body",
            config_file=self.temp_config.name
        )
        
        # Verify SMTP was correctly used
        mock_smtp.assert_called_once()
        smtp_instance.starttls.assert_called_once()
        smtp_instance.login.assert_called_once()
        smtp_instance.sendmail.assert_called_once()
        smtp_instance.quit.assert_called_once()
        
        self.assertTrue(result)
        
    @patch('attached_assets.send_email.smtplib.SMTP')
    @patch('attached_assets.send_email.validate_email')
    def test_send_email_invalid_recipient(self, mock_validate, mock_smtp):
        """Test email sending with invalid recipient"""
        mock_validate.return_value = False
        
        result = send_email(
            recipient="invalid-email",
            subject="Test Subject",
            body="Test Body",
            config_file=self.temp_config.name
        )
        
        # SMTP should not be used
        mock_smtp.assert_not_called()
        self.assertFalse(result)
        
    @patch('attached_assets.send_email.smtplib.SMTP')
    def test_send_email_smtp_error(self, mock_smtp):
        """Test email sending with SMTP error"""
        # Setup SMTP mock to raise an exception
        mock_smtp.side_effect = Exception("SMTP connection failed")
        
        result = send_email(
            recipient="test@example.com",
            subject="Test Subject",
            body="Test Body",
            config_file=self.temp_config.name
        )
        
        self.assertFalse(result)
        
if __name__ == '__main__':
    unittest.main()