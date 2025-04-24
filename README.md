<h3> .env file Setup</h3>
🔐 Environment Variables Setup
create a `.env` file in the root of your project directory. This file should contain all your sensitive keys used for authentication and mailing.

> ⚠️ **Never share your `.env` file or commit it to version control.**

📄 Sample `.env` Format

```env
# Twilio Credentials
ACCOUNT_SID=**********ef19bcd9e5cd37c469f6c3eb
AUTH_TOKEN=***********f416b62960d5f20a88a2ce
TWILIO_PHONE_NUMBER=+173421*****

# SMTP Mail Credentials
MAIL_USERNAME=ksandhyarani5200@gmail.com
MAIL_PASSWORD=cpwnpkjeyqaa****
MAIL_FROM=ksandhyarani5200@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

> ✅ Make sure your code loads this file using `dotenv` to access these variables securely.

<h2> Please refer to User_Authentication_important_guide.docx in the project directory for detailed setup instructions and credentials management.</h2>
