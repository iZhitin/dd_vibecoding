MAGIC_LINK_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial,
            sans-serif;
            color: #111827; background-color: #ffffff;
            margin: 0; padding: 40px 20px; text-align: center;
        }}
        .header {{ font-size: 24px; font-weight: 600; margin-bottom: 24px; }}
        .text {{ font-size: 16px; color: #4B5563; margin-bottom: 32px; }}
        .button {{
            display: inline-block; background-color: #111827; color: #ffffff !important;
            text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: 500;
            font-size: 16px; margin-bottom: 32px;
        }}
        .footer {{ font-size: 14px; color: #9CA3AF; }}
    </style>
</head>
<body>
    <div class="header">DD &mdash; Your Login Link</div>
    <div class="text">Click the button below to sign in to your account.</div>
    <a href="{url}" class="button">Sign In</a>
    <div class="footer">This link expires in 15 minutes.</div>
</body>
</html>
"""

REMINDER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial,
            sans-serif;
            color: #111827; background-color: #ffffff;
            margin: 0; padding: 40px 20px; text-align: center;
        }}
        .header {{ font-size: 24px; font-weight: 600; margin-bottom: 24px; }}
        .text {{ font-size: 16px; color: #4B5563; margin-bottom: 32px; }}
        .button {{
            display: inline-block; background-color: #111827; color: #ffffff !important;
            text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: 500;
            font-size: 16px; margin-bottom: 32px;
        }}
    </style>
</head>
<body>
    <div class="header">Time to practice</div>
    <div class="text">You have {card_count} words waiting.</div>
    <a href="{app_url}/practice" class="button">Open DD</a>
</body>
</html>
"""

DAILY_DIGEST_HTML_WRAPPER = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial,
            sans-serif;
            color: #111827; background-color: #ffffff; margin: 0; padding: 40px 20px;
        }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .header {{ font-size: 24px; font-weight: 600; margin-bottom: 24px; text-align: center; }}
        .streak {{
            font-size: 14px; font-weight: 500; color: #6B7280; text-align: center;
            margin-bottom: 32px; text-transform: uppercase; letter-spacing: 0.05em;
        }}
        .item {{ padding: 16px 0; border-bottom: 1px solid #E5E7EB; }}
        .item:last-child {{ border-bottom: none; }}
        .row {{ display: flex; align-items: baseline; margin-bottom: 4px; }}
        .dot {{
            width: 10px; height: 10px; border-radius: 50%; display: inline-block;
            margin-right: 12px; flex-shrink: 0;
        }}
        .GREEN {{ background-color: #10B981; }}
        .GREEN_STAR {{ background-color: #10B981; box-shadow: 0 0 8px #10B981; }}
        .YELLOW {{ background-color: #F59E0B; }}
        .RED {{ background-color: #EF4444; }}
        .word {{ font-weight: 600; font-size: 16px; margin-right: 8px; }}
        .feedback {{
            color: #4B5563; font-size: 15px; margin-left: 22px; margin-top: 4px;
            line-height: 1.5;
        }}
        .praise {{
            color: #059669; font-weight: 500; margin-left: 22px; font-size: 14px; margin-top: 4px;
        }}
        .button-container {{ text-align: center; margin-top: 40px; }}
        .button {{
            display: inline-block; background-color: #111827; color: #ffffff !important;
            text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: 500;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">Your Daily Digest</div>
        <div class="streak">Current Streak: {streak} days</div>
        
        <div class="reviews">
            {reviews_html}
        </div>
        
        <div class="button-container">
            <a href="{app_url}/review/{session_id}" class="button">View Detailed Review</a>
        </div>
    </div>
</body>
</html>
"""

REVIEW_ITEM_HTML = """
        <div class="item">
            <div class="row">
                <span class="dot {grade}"></span>
                <span class="word">{word}</span>
            </div>
            {praise_html}
            <div class="feedback">{feedback}</div>
        </div>
"""
