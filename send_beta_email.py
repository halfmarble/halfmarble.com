#!/usr/bin/env python3
"""
send_beta_email.py — send the halfmarble beta welcome email via Gmail SMTP

Setup (one time):
  1. Enable 2FA on your Gmail account (required for App Passwords)
     https://myaccount.google.com/security
  2. Create an App Password:
     https://myaccount.google.com/apppasswords
     Name it "halfmarble" — you'll get a 16-character password
  3. Add to your shell profile (~/.zshrc):
       export GMAIL_ADDRESS="gerard@halfmarble.com"
       export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
     Then: source ~/.zshrc

Usage:
  ./send_beta_email.py recipient@example.com
  ./send_beta_email.py recipient@example.com "Jane Doe"

Dry run (preview without sending):
  DRY_RUN=1 ./send_beta_email.py recipient@example.com

Notes:
  - Uses Python 3 stdlib only — no pip install needed
  - Gmail sends emails with your configured address as "From"
  - If gerard@halfmarble.com is a Google Workspace alias on a Gmail
    account, make sure it's added as a "Send mail as" alias in Gmail
    settings, otherwise the From field will be overridden
"""

import os
import sys
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
HTML_FILE = SCRIPT_DIR / "email_beta_welcome.html"
SUBJECT = "You're in — welcome to the fight"
SENDER_NAME = "Gerard Ziemski"
BCC_RECIPIENTS = ["gerard@halfmarble.com", "anya@halfmarble.com"]
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def main() -> int:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} recipient@example.com [\"Recipient Name\"]", file=sys.stderr)
        return 1

    recipient = sys.argv[1]
    recipient_name = sys.argv[2] if len(sys.argv) > 2 else ""

    to_header = f"{recipient_name} <{recipient}>" if recipient_name else recipient

    gmail_address = os.environ.get("GMAIL_ADDRESS")
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not gmail_address or not gmail_password:
        print("Error: GMAIL_ADDRESS and GMAIL_APP_PASSWORD environment variables must be set", file=sys.stderr)
        print("Add to your shell profile:", file=sys.stderr)
        print('  export GMAIL_ADDRESS="you@gmail.com"', file=sys.stderr)
        print('  export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"', file=sys.stderr)
        return 1

    if not HTML_FILE.exists():
        print(f"Error: HTML template not found: {HTML_FILE}", file=sys.stderr)
        return 1

    html_body = HTML_FILE.read_text(encoding="utf-8")

    # Plain text fallback for clients that don't render HTML
    text_body = (
        "You are in — welcome to the fight\n\n"
        "Thank you for signing up. Two tools, one fight:\n\n"
        "SteadyDoseTracker — https://halfmarble.com/steady_dose_tracker_demo.html\n"
        "SteadyFastingTracker    — https://halfmarble.com/steady_fasting_tracker_demo.html\n\n"
        "What \"Glass Box\" means for you:\n"
        "  ANCHORED  — The AI is pinned to static, versioned data. It cannot drift.\n"
        "  ON-DEVICE — The AI model lives on your phone. Nothing runs in the cloud.\n"
        "  LOCAL     — Your data stays on your phone. Join the fight by opting in to share anonymized patterns with researchers.\n"
        "  TRACEABLE — Every claim cites a published paper. No hallucinations.\n"
        "  OPEN      — Source code will be released for independent review.\n\n"
        "We'll email you when the beta is ready. No spam, no selling your email, no tracking pixels in this message.\n\n"
        "This is a personal project. My wife Anya and I are building it because I need it.\n\n"
        "Gerard Ziemski\n"
        "Cofounder, Platform Architect | Halfmarble LLC\n"
    )

    msg = EmailMessage()
    msg["Subject"] = SUBJECT
    msg["From"] = f"{SENDER_NAME} <{gmail_address}>"
    msg["To"] = to_header
    if BCC_RECIPIENTS:
        msg["Bcc"] = ", ".join(BCC_RECIPIENTS)
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    if os.environ.get("DRY_RUN") == "1":
        print(f"[DRY RUN] Would send to: {to_header}")
        if BCC_RECIPIENTS:
            print(f"[DRY RUN] Bcc: {', '.join(BCC_RECIPIENTS)}")
        print(f"[DRY RUN] Subject: {SUBJECT}")
        print(f"[DRY RUN] HTML size: {len(html_body)} bytes")
        print(f"[DRY RUN] Text fallback size: {len(text_body)} bytes")
        print("[DRY RUN] No request sent.")
        return 0

    print(f"Sending beta welcome email to: {to_header}")

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(gmail_address, gmail_password)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication failed: {e}", file=sys.stderr)
        print("Check that GMAIL_APP_PASSWORD is a valid App Password (not your Gmail password)", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Failed to send: {e}", file=sys.stderr)
        return 1

    print("Sent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
