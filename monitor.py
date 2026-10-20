import os
import smtplib
from email.mime.text import MIMEText
import yfinance as yf

# Updated recipients list (Sanjaykumar removed)
RECIPIENTS = [
    "himanshudahiwale01@gmail.com",
    "pranay8thecake@gmail.com"
]

def fetch_and_email():
    print("Fetching Nifty 50 data...")
    ticker = yf.Ticker("^NSEI")
    data = ticker.history(period="2d")

    if len(data) < 2:
        print("Error: Insufficient market data returned.")
        return

    prev_close = float(data["Close"].iloc[-2])
    current_price = float(data["Close"].iloc[-1])
    pct_change = ((current_price - prev_close) / prev_close) * 100

    print(f"Prev Close: {prev_close:.2f} | Current: {current_price:.2f} | Change: {pct_change:.2f}%")

    sender_email = os.environ.get("SENDER_EMAIL")
    app_password = os.environ.get("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        print("Error: Email credentials not found in GitHub Secrets.")
        return

    direction = "UP" if pct_change >= 0 else "DOWN"
    subject = f"Nifty 50 is {direction} {abs(pct_change):.2f}% at 12 PM"
    
    body = (
        f"Daily 12 PM Nifty 50 Update:\n\n"
        f"Current Value: {current_price:.2f}\n"
        f"Previous Close: {prev_close:.2f}\n"
        f"Percentage Change: {pct_change:.2f}%\n"
    )

    try:
        print("Connecting to email server...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            
            # Loop through each recipient and send an individual email for privacy
            for recipient in RECIPIENTS:
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = recipient
                
                server.sendmail(sender_email, [recipient], msg.as_string())
                
        print(f"Email successfully sent individually to {len(RECIPIENTS)} recipient(s)")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    fetch_and_email()
