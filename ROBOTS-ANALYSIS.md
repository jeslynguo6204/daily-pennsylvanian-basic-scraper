# Robots Analysis for the Daily Pennsylvanian

The Daily Pennsylvanian's `robots.txt` file is available at
[https://www.thedp.com/robots.txt](https://www.thedp.com/robots.txt).

## Contents of the `robots.txt` file on 02/19/2025

```
User-agent: *
Crawl-delay: 10
Allow: /

User-agent: SemrushBot
Disallow: /
```

## Explanation

🧐 What This Means
General Rules for All Web Crawlers (User-agent: *)

Crawl-delay: 10 → Web crawlers must wait 10 seconds between requests.
Allow: / → All bots can access all pages of the website.
Specific Rule for SemrushBot

User-agent: SemrushBot → This rule applies only to SemrushBot (an SEO analytics bot).
Disallow: Image → This is an incorrect syntax because "Image" is not a valid directory or file path.
If the intent was to block images, the correct rule would be:
bash
Copy
Edit
Disallow: /images/
🤖 Impact on This Scraper
✅ Our scraper is allowed to access all pages (Allow: /).
⏳ We must respect the 10-second delay between requests (Crawl-delay: 10).
🚫 We are not affected by the SemrushBot rule since it only applies to that bot.

💡 Compliance Strategy
To ensure our scraper follows the site's rules:

We include a 10-second delay between requests using time.sleep(10).
We set a User-Agent header to prevent accidental blocking.
We check for future changes to robots.txt before scraping.
