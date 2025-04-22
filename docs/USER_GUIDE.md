# APIX-V4PY User Guide

## Getting Started

APIX-V4PY is a standalone Python application that provides an interface to the MailChats Trly APIX2 email management system.

### First Launch

When you first launch the application, you'll be presented with the login screen. You can use your existing MailChats account or create a new one.

### Main Interface

The main interface consists of the following components:

1. **Dashboard** - Provides an overview of your email campaigns and statistics.
2. **Template Editor** - Create and edit email templates with HTML support.
3. **Campaign Manager** - Manage your email campaigns and recipient lists.
4. **Analytics** - View detailed reports on email performance.
5. **Settings** - Configure application and account settings.

## Working with Templates

### Creating a Template

1. Go to the Template Editor section.
2. Click "New Template".
3. Design your email using the visual editor or HTML mode.
4. Use variables like `{{email}}`, `{{emailname}}`, and `{{domain}}` for personalization.
5. Save your template.

### Enhanced Personalization

The application supports advanced personalization with variables like:

- `{{email}}` - Recipient's email address
- `{{emailname}}` - Name part of the email address
- `{{domain}}` - Domain part of the email address
- `{{time}}` - Current time
- `{{firstname}}` - First name (if provided)
- `{{lastname}}` - Last name (if provided)
- `{{company}}` - Company name (if provided)
- `{{position}}` - Job position (if provided)

## Managing Campaigns

### Creating a Campaign

1. Go to the Campaign Manager section.
2. Click "New Campaign".
3. Select a template for your campaign.
4. Upload or select a recipient list.
5. Configure sending options (schedule, sender information, etc.).
6. Review and start the campaign.

### Recipient Lists

Recipient lists can be uploaded in CSV or TXT format. The application supports various formats:

1. **Simple format**: One email per line
   ```
   email1@example.com
   email2@example.com
   ```

2. **Advanced format**: Email with custom fields
   ```
   email1@example.com|firstname=John|lastname=Doe|company=Acme Inc
   email2@example.com|firstname=Jane|lastname=Smith|company=XYZ Corp
   ```

## Analyzing Results

The Analytics section provides detailed reports on your email campaigns, including:

- Open rates
- Click-through rates
- Delivery status
- Bounce rates
- Geographic distribution

## Customizing Settings

In the Settings section, you can configure:

- SMTP server settings
- Default sender information
- Application theme
- Time zone and language preferences
- License information

## Troubleshooting

If you encounter any issues:

1. Check the application logs in the data/logs directory.
2. Verify your internet connection.
3. Ensure your SMTP settings are correct.
4. Check that your license is valid and active.

For additional support, please refer to the GitHub repository or contact support.