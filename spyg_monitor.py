import os
import smtplib
from email.mime.text import MIMEText
import yfinance as yf

# Updated recipients list
RECIPIENTS = [
    "pranay8thecake@gmail.com",
    "himanshudahiwale01@gmail.com"
]

# The threshold for the alert to trigger
THRESHOLD_PCT = -0.5

# Dictionary of ETFs to track
TICKERS = {
    "SPYG": "SPDR Portfolio S&P 500 Growth ETF",
    "VGT": "Vanguard Information Technology ETF",
    "VOX": "Vanguard Communication Services ETF",
    "VHT": "Vanguard Health Care ETF"
}

def check_and_alert():
    print("Fetching ETF data...")
    
    email_body_parts = ["Daily ETF Performance Update:\n"]
    alert_triggered = False

    for symbol, name in TICKERS.items():
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="2d")

        if len(data) < 2:
            print(f"Error: Insufficient market data returned for {symbol}.")
            continue

        prev_close = float(data["Close"].iloc[-2])
        current_price = float(data["Close"].iloc[-1])
        pct_change = ((current_price - prev_close) / prev_close) * 100

        print(f"{symbol}: Prev Close: {prev_close:.2f} | Current: {current_price:.2f} | Change: {pct_change:.2f}%")

        if pct_change <= THRESHOLD_PCT:
            alert_triggered = True

        direction = "UP" if pct_change >= 0 else "DOWN"
        
        email_body_parts.append(
            f"--- {name} ({symbol}) ---\n"
            f"Current Value: ${current_price:.2f}\n"
            f"Previous Close: ${prev_close:.2f}\n"
            f"Percentage Change: {pct_change:.2f}% ({direction})\n"
        )

    if alert_triggered:
        sender_email = os.environ.get("SENDER_EMAIL")
        app_password = os.environ.get("EMAIL_APP_PASSWORD")

        if not sender_email or not app_password:
            print("Error: Email credentials not found in GitHub Secrets.")
            return

        subject = "MARKET ALERT: One or more tracked ETFs dropped 0.5%+"
        body = "\n".join(email_body_parts)

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = ", ".join(RECIPIENTS)

        try:
            print("Connecting to email server...")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, app_password)
                server.sendmail(sender_email, RECIPIENTS, msg.as_string())
            print(f"Alert email successfully sent to {len(RECIPIENTS)} recipient(s)")
        except Exception as e:
            print(f"Failed to send email: {e}")
    else:
        print("No ETFs dropped by the threshold. No email sent.")

if __name__ == "__main__":
    check_and_alert()
