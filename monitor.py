import os
import smtplib
from email.mime.text import MIMEText
import yfinance as yf

# Replace with your friend's email address
RECIPIENT_EMAIL = "pranay8thecake@gmail.com" 

def fetch_and_email():
    print("Fetching Nifty 50 data...")
    ticker = yf.Ticker("^NSEI")
    data = ticker.history(period="1d")

    if len(data) < 1:
        print("Error: Insufficient market data returned.")
        return

    current_price = float(data["Close"].iloc[-1])
    print(f"SUCCESS! Current Nifty 50 Value is: {current_price:.2f}")

    sender_email = os.environ.get("SENDER_EMAIL")
    app_password = os.environ.get("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        print("Error: Email credentials not found in GitHub Secrets.")
        return

    subject = f"TEST: Current Nifty 50 Value is {current_price:.2f}"
    body = f"Hello!\n\nThe current Nifty 50 index value is: {current_price:.2f}\n\nThis is an automated test."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = RECIPIENT_EMAIL

    try:
        print("Connecting to email server...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, [RECIPIENT_EMAIL], msg.as_string())
        print(f"Email successfully sent to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    fetch_and_email()
