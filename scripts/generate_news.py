#!/usr/bin/env python3
"""
Generate The Triangle Tribune daily newspaper.
Fetches world and RTP NC news, generates HTML, saves as index.html.
"""

import requests
from datetime import datetime
import re
import json

def search_news(query, num_results=10):
    """Fetch news from web search (using DuckDuckGo as fallback)."""
    # Using a simple search approach via requests
    # In production, you'd use a news API like NewsAPI or Google News
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; TriangleTribune/1.0)'
    }

    results = []
    try:
        # Try a basic web search simulation
        # For real implementation, integrate with NewsAPI.org or similar
        search_url = f"https://www.bing.com/news/search?q={query.replace(' ', '+')}"
        response = requests.get(search_url, headers=headers, timeout=5)

        if response.status_code == 200:
            # Parse basic news results
            # This is a simplified version - real implementation would parse HTML or use API
            results = [{
                'headline': f'News about {query}',
                'summary': f'Latest updates on {query}',
                'source': 'Web Search',
                'url': search_url
            }]
    except Exception as e:
        print(f"Search error for '{query}': {e}")

    return results

def fetch_today_news():
    """Fetch news for all categories: world, US, local, sports, science, finance, innovation."""
    categories = {
        'world': [
            "world news today",
            "international breaking news",
            "Middle East politics news"
        ],
        'us': [
            "US news today",
            "American politics news",
            "US economy inflation"
        ],
        'local': [
            "Raleigh Durham news today",
            "Chapel Hill news",
            "Research Triangle Park news"
        ],
        'sports': [
            "NBA Knicks news",
            "Liverpool Premier League news",
            "sports news today"
        ],
        'science': [
            "science news today",
            "climate change news",
            "medical breakthrough news"
        ],
        'finance': [
            "stock market news today",
            "crypto bitcoin news",
            "business finance news"
        ],
        'innovation': [
            "AI technology news",
            "green energy innovation",
            "biotech CRISPR news"
        ]
    }

    news_by_category = {}
    for category, queries in categories.items():
        print(f"🔍 Fetching {category} news...")
        category_news = []
        for query in queries:
            category_news.extend(search_news(query, 2))
        news_by_category[category] = category_news[:3]

    return news_by_category

def generate_html(news_by_category):
    """Generate newspaper-style HTML."""
    today = datetime.now()
    date_str = today.strftime("%A, %B %d, %Y")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>The Triangle Tribune — {today.strftime('%B %d, %Y')}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: #f4f0e6;
      color: #1a1a1a;
      font-family: 'Source Serif 4', Georgia, serif;
      font-size: 15px;
      line-height: 1.6;
    }}

    .page {{
      max-width: 1100px;
      margin: 0 auto;
      background: #fdfaf3;
      border-left: 1px solid #c8b89a;
      border-right: 1px solid #c8b89a;
      padding: 0 0 40px;
    }}

    .masthead {{
      text-align: center;
      padding: 28px 20px 10px;
      border-bottom: 4px double #1a1a1a;
    }}

    .masthead-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      letter-spacing: .05em;
      color: #555;
      margin-bottom: 6px;
    }}

    .paper-name {{
      font-family: 'UnifrakturMaguntia', cursive;
      font-size: 72px;
      line-height: 1;
      letter-spacing: -1px;
      color: #111;
    }}

    .paper-tagline {{
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: 13px;
      color: #555;
      margin-top: 4px;
      letter-spacing: .06em;
    }}

    .masthead-bottom {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 8px;
      font-size: 11px;
      letter-spacing: .05em;
      color: #444;
      border-top: 1px solid #aaa;
      padding-top: 6px;
    }}

    .section-label {{
      font-family: 'Playfair Display', serif;
      font-weight: 700;
      font-size: 11px;
      letter-spacing: .2em;
      text-transform: uppercase;
      color: #fff;
      background: #1a1a1a;
      display: inline-block;
      padding: 3px 14px;
      margin: 22px 20px 0;
    }}

    .section-label.local {{
      background: #8b2020;
    }}

    .grid {{
      display: grid;
      gap: 0;
      padding: 0 20px;
      grid-template-columns: 1fr 1fr;
      margin-top: 14px;
    }}

    article {{
      padding: 14px 16px;
      border-right: 1px solid #c8b89a;
      border-bottom: 1px solid #c8b89a;
    }}

    article:last-child {{ border-right: none; }}

    .kicker {{
      font-size: 10px;
      letter-spacing: .15em;
      text-transform: uppercase;
      color: #8b2020;
      font-weight: 600;
      margin-bottom: 4px;
    }}

    h3.headline {{
      font-family: 'Playfair Display', serif;
      font-weight: 700;
      font-size: 18px;
      line-height: 1.25;
      margin-bottom: 8px;
    }}

    .body-copy {{
      font-size: 14px;
      line-height: 1.6;
      color: #222;
      margin-bottom: 8px;
    }}

    .source-tag {{
      font-size: 10px;
      letter-spacing: .08em;
      text-transform: uppercase;
      color: #777;
      margin-top: 8px;
    }}

    .source-tag a {{
      color: #8b2020;
      text-decoration: none;
      border-bottom: 1px dotted #8b2020;
    }}

    .source-tag a:hover {{ text-decoration: underline; }}

    .read-more {{
      display: inline-block;
      margin-top: 8px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: .06em;
      text-transform: uppercase;
      color: #8b2020;
      text-decoration: none;
    }}

    .read-more:hover {{ text-decoration: underline; }}

    .ticker {{
      background: #1a1a1a;
      color: #f4f0e6;
      font-size: 11px;
      letter-spacing: .06em;
      padding: 7px 20px;
      margin-top: 28px;
      overflow: hidden;
    }}

    footer {{
      text-align: center;
      font-size: 10px;
      color: #888;
      margin-top: 20px;
      letter-spacing: .05em;
      padding: 0 20px;
    }}

    @media (max-width: 700px) {{
      .grid {{ grid-template-columns: 1fr; }}
      .paper-name {{ font-size: 44px; }}
      article {{ border-right: none; }}
    }}
  </style>
</head>
<body>
<div class="page">

  <header class="masthead">
    <div class="masthead-top">
      <span>MORNING EDITION</span>
      <span>ESTABLISHED 1884</span>
      <span>AUTO-GENERATED DAILY</span>
    </div>
    <div class="paper-name">The Triangle Tribune</div>
    <div class="paper-tagline">All the News Fit to Read — World, Nation & the Research Triangle</div>
    <div class="masthead-bottom">
      <span>{date_str}</span>
      <span>⬥ DAILY EDITION</span>
      <span>RALEIGH · DURHAM · CHAPEL HILL</span>
    </div>
  </header>

  <div class="section-label">World & National News</div>
  <div class="grid">
"""

    # Add world news
    for i, story in enumerate(world_news):
        url = story.get('url', '#')
        html += f"""    <article>
      <div class="kicker">Global News</div>
      <h3 class="headline">{story.get('headline', 'News Update')}</h3>
      <p class="body-copy">{story.get('summary', 'Latest news and updates.')}</p>
      <a class="read-more" href="{url}" target="_blank" rel="noopener">Read Full Story →</a>
      <p class="source-tag">Source: <a href="{url}" target="_blank" rel="noopener">{story.get('source', 'News')}</a></p>
    </article>
"""

    html += """  </div>

  <div class="section-label local">RTP & Triangle Local News</div>
  <div class="grid">
"""

    # Add local news
    for story in local_news:
        url = story.get('url', '#')
        html += f"""    <article>
      <div class="kicker">Triangle Area</div>
      <h3 class="headline">{story.get('headline', 'Local News')}</h3>
      <p class="body-copy">{story.get('summary', 'Latest local updates.')}</p>
      <a class="read-more" href="{url}" target="_blank" rel="noopener">Read Full Story →</a>
      <p class="source-tag">Source: <a href="{url}" target="_blank" rel="noopener">{story.get('source', 'Local News')}</a></p>
    </article>
"""

    html += f"""  </div>

  <div class="ticker">
    ⬤ The Triangle Tribune is auto-generated daily at 7 AM EST via GitHub Actions ·
    ⬤ All stories linked to original sources ·
    ⬤ Coverage: World News, U.S. News, RTP Triangle Area
  </div>

  <footer>
    The Triangle Tribune · Daily Morning Edition · {date_str}<br>
    Serving Raleigh, Durham, Chapel Hill, Cary & the Research Triangle · Auto-published via GitHub Actions
  </footer>

</div>
</body>
</html>
"""

    return html

def main():
    print("📰 Generating The Triangle Tribune...")

    # Fetch news
    news_by_category = fetch_today_news()

    # Generate HTML
    html = generate_html(news_by_category)

    # Save to index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    total_stories = sum(len(stories) for stories in news_by_category.values())
    print(f"✅ Generated index.html with {total_stories} total stories across 7 categories")

if __name__ == '__main__':
    main()
