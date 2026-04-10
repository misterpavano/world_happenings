#!/usr/bin/env python3
"""
Generate The Triangle Tribune daily newspaper.
Fetches real news from NewsAPI + RSS feeds, generates HTML, saves as index.html.
"""

import requests
import feedparser
from datetime import datetime
import html
import os

# NewsAPI Key
NEWSAPI_KEY = "36736110f11441729fbcd023357bef1b"

# RSS Feed URLs for each category (topic-based)
RSS_FEEDS = {
    'world': [
        'https://feeds.bbc.co.uk/news/world/rss.xml',
        'https://feeds.reuters.com/reuters/worldNews',
        'http://feeds.aljazeera.com/AJEnglish/rss.xml'
    ],
    'us': [
        'https://feeds.bbc.co.uk/news/us_and_canada/rss.xml',
        'https://feeds.reuters.com/reuters/domesticNews',
        'https://feeds.washingtonpost.com/rss/national'
    ],
    'local': [
        'https://www.wral.com/feed/',
        'https://www.indyweek.com/feed/rss'
    ],
    'sports': [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://www.espn.com/espn/rss/news',
        'https://feeds.sky.com/feeds/skysports/rss.xml'
    ],
    'science': [
        'https://feeds.nasa.gov/pu.rss',
        'https://feeds.nature.com/nature/rss/current',
        'https://www.sciencedaily.com/rss/all.xml'
    ],
    'finance': [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://feeds.cnbc.com/nbcnews/public/business/',
        'https://feeds.reuters.com/reuters/businessNews'
    ],
    'innovation': [
        'https://feeds.arstechnica.com/arstechnica/index',
        'https://www.techcrunch.com/feed/',
        'https://feeds.theverge.com/vergefeeds/rss/index.xml'
    ]
}

def fetch_newsapi(category, num_articles=3):
    """Fetch news from NewsAPI based on category keywords."""
    keywords = {
        'world': 'international OR global',
        'us': 'US OR United States',
        'local': 'Raleigh OR Durham OR "Research Triangle" OR "Chapel Hill"',
        'sports': 'sports OR NBA OR Premier League OR football',
        'science': 'science OR space OR climate',
        'finance': 'business OR finance OR stock market',
        'innovation': 'technology OR AI OR innovation'
    }

    articles = []
    try:
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': keywords.get(category, category),
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': num_articles,
            'apiKey': NEWSAPI_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for article in data.get('articles', [])[:num_articles]:
                articles.append({
                    'headline': article.get('title', 'Breaking News'),
                    'summary': article.get('description', article.get('content', 'Read more at source'))[:200],
                    'source': article.get('source', {}).get('name', 'News'),
                    'url': article.get('url', '#'),
                    'image': article.get('urlToImage', '')
                })
    except Exception as e:
        print(f"NewsAPI error for '{category}': {e}")

    return articles

def fetch_rss_feeds(category, num_articles=3):
    """Fetch news from RSS feeds for the category."""
    articles = []
    feeds = RSS_FEEDS.get(category, [])

    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:2]:
                articles.append({
                    'headline': html.unescape(entry.get('title', 'Breaking News')),
                    'summary': html.unescape(entry.get('summary', 'Read more'))[:200],
                    'source': feed.feed.get('title', 'News Feed'),
                    'url': entry.get('link', '#'),
                    'image': ''
                })
        except Exception as e:
            print(f"RSS feed error for {feed_url}: {e}")

    return articles[:num_articles]

def fetch_today_news():
    """Fetch news for all categories using NewsAPI + RSS feeds."""
    categories = ['world', 'us', 'local', 'sports', 'science', 'finance', 'innovation']
    news_by_category = {}

    for category in categories:
        print(f"🔍 Fetching {category} news...")

        # Try NewsAPI first
        newsapi_articles = fetch_newsapi(category, num_articles=4)

        # Supplement with RSS feeds
        rss_articles = fetch_rss_feeds(category, num_articles=3)

        # Combine and deduplicate
        all_articles = newsapi_articles + rss_articles
        seen_urls = set()
        unique_articles = []

        for article in all_articles:
            if article['url'] not in seen_urls and len(unique_articles) < 9:
                unique_articles.append(article)
                seen_urls.add(article['url'])

        news_by_category[category] = unique_articles
        print(f"  ✓ Got {len(unique_articles)} {category} articles")

    return news_by_category

def generate_html(news_by_category):
    """Generate newspaper-style HTML from news data."""
    today = datetime.now()
    date_str = today.strftime("%A, %B %d, %Y")

    # Start HTML document
    html_content = f"""<!DOCTYPE html>
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
      font-size: 14px;
      line-height: 1.6;
    }}

    nav.floating-nav {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      background: #1a1a1a;
      border-bottom: 2px solid #8b2020;
      padding: 0;
      z-index: 1000;
      display: flex;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }}

    nav.floating-nav::-webkit-scrollbar {{
      height: 3px;
    }}

    nav.floating-nav::-webkit-scrollbar-thumb {{
      background: #8b2020;
    }}

    nav.floating-nav a {{
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      padding: 10px 16px;
      color: #f4f0e6;
      text-decoration: none;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: .08em;
      text-transform: uppercase;
      border-bottom: 3px solid transparent;
      transition: all 0.2s ease;
      white-space: nowrap;
      min-height: 44px;
      cursor: pointer;
    }}

    nav.floating-nav a:hover {{
      background: #8b2020;
    }}

    nav.floating-nav a.active {{
      background: #8b2020;
      border-bottom-color: #ffd700;
      color: #ffd700;
    }}

    .page-wrapper {{
      margin-top: 50px;
      padding: 0 12px 40px;
    }}

    .page {{
      max-width: 900px;
      margin: 0 auto;
      background: #fdfaf3;
      border-radius: 4px;
    }}

    .masthead {{
      text-align: center;
      padding: 18px 12px 8px;
      border-bottom: 2px solid #1a1a1a;
      background: #fdfaf3;
      border-radius: 4px 4px 0 0;
    }}

    .masthead-top {{
      font-size: 9px;
      letter-spacing: .05em;
      color: #666;
      margin-bottom: 4px;
    }}

    .paper-name {{
      font-family: 'UnifrakturMaguntia', cursive;
      font-size: 48px;
      line-height: 1;
      letter-spacing: -1px;
      color: #111;
      margin: 4px 0;
    }}

    .paper-tagline {{
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: 11px;
      color: #666;
      margin: 3px 0;
      letter-spacing: .03em;
    }}

    .masthead-bottom {{
      font-size: 9px;
      letter-spacing: .04em;
      color: #666;
      border-top: 1px solid #c8b89a;
      padding-top: 4px;
      margin-top: 4px;
    }}

    .section-label {{
      font-family: 'Playfair Display', serif;
      font-weight: 700;
      font-size: 10px;
      letter-spacing: .15em;
      text-transform: uppercase;
      color: #fff;
      background: #1a1a1a;
      display: inline-block;
      padding: 4px 10px;
      margin: 14px 0 8px;
    }}

    .section-label.highlight {{
      background: #8b2020;
    }}

    .grid {{
      display: grid;
      gap: 0;
      grid-template-columns: 1fr;
      margin: 10px 0;
      border: 1px solid #c8b89a;
    }}

    article {{
      padding: 12px;
      border-bottom: 1px solid #c8b89a;
    }}

    article:last-child {{
      border-bottom: none;
    }}

    .kicker {{
      font-size: 9px;
      letter-spacing: .1em;
      text-transform: uppercase;
      color: #8b2020;
      font-weight: 600;
      margin-bottom: 3px;
    }}

    h3.headline {{
      font-family: 'Playfair Display', serif;
      font-weight: 700;
      font-size: 14px;
      line-height: 1.25;
      margin-bottom: 5px;
    }}

    .body-copy {{
      font-size: 13px;
      line-height: 1.5;
      color: #222;
      margin-bottom: 6px;
    }}

    .source-tag {{
      font-size: 9px;
      letter-spacing: .06em;
      text-transform: uppercase;
      color: #777;
      margin-top: 5px;
    }}

    .source-tag a {{
      color: #8b2020;
      text-decoration: none;
      border-bottom: 1px dotted #8b2020;
    }}

    .source-tag a:hover {{
      text-decoration: underline;
    }}

    .read-more {{
      display: inline-block;
      margin-top: 6px;
      font-size: 9px;
      font-weight: 600;
      letter-spacing: .05em;
      text-transform: uppercase;
      color: #8b2020;
      text-decoration: none;
    }}

    .read-more:hover {{
      text-decoration: underline;
    }}

    section.news-section {{
      display: none;
    }}

    section.news-section.active {{
      display: block;
    }}

    .ticker {{
      background: #1a1a1a;
      color: #f4f0e6;
      font-size: 10px;
      letter-spacing: .04em;
      padding: 8px 12px;
      margin: 12px 0;
      overflow: hidden;
      border-radius: 4px;
      line-height: 1.4;
    }}

    .ticker span {{
      display: block;
      margin-bottom: 4px;
    }}

    footer {{
      text-align: center;
      font-size: 9px;
      color: #888;
      padding: 12px;
      border-top: 1px solid #c8b89a;
      margin-top: 12px;
      line-height: 1.4;
    }}

    @media (min-width: 768px) {{
      nav.floating-nav {{
        position: fixed;
        left: 0;
        top: 50%;
        right: auto;
        transform: translateY(-50%);
        flex-direction: column;
        width: 140px;
        border-right: 2px solid #8b2020;
        border-bottom: none;
        border-radius: 0 8px 8px 0;
        overflow: visible;
      }}

      nav.floating-nav a {{
        flex-direction: column;
        border-left: 3px solid transparent;
        border-bottom: none;
        min-height: 50px;
        padding: 12px 10px;
      }}

      nav.floating-nav a.active {{
        border-left-color: #ffd700;
        border-bottom: none;
      }}

      .page-wrapper {{
        margin-top: 0;
        margin-left: 140px;
        padding: 0 16px 40px;
      }}

      .paper-name {{
        font-size: 64px;
      }}

      .grid {{
        grid-template-columns: 1fr 1fr 1fr;
      }}

      article {{
        padding: 14px;
      }}
    }}
  </style>
</head>
<body>

<nav class="floating-nav">
  <a class="nav-link active" data-section="world">World</a>
  <a class="nav-link" data-section="us">U.S.</a>
  <a class="nav-link" data-section="local">Local</a>
  <a class="nav-link" data-section="sports">Sports</a>
  <a class="nav-link" data-section="science">Science</a>
  <a class="nav-link" data-section="finance">Finance</a>
  <a class="nav-link" data-section="innovation">Innovation</a>
</nav>

<div class="page-wrapper">
<div class="page">

  <header class="masthead">
    <div class="masthead-top">VOL. CXLII · NO. 100 · ESTABLISHED 1884</div>
    <div class="paper-name">The Triangle Tribune</div>
    <div class="paper-tagline">All the News Fit to Read</div>
    <div class="masthead-bottom">
      {date_str} · ⬥ MORNING EDITION · RALEIGH · DURHAM · CHAPEL HILL
    </div>
  </header>
"""

    # Generate sections for each category
    categories = ['world', 'us', 'local', 'sports', 'science', 'finance', 'innovation']
    section_labels = {
        'world': 'World News',
        'us': 'U.S. News',
        'local': 'RTP & Triangle Local',
        'sports': 'Sports',
        'science': 'Science',
        'finance': 'Finance',
        'innovation': 'Innovation'
    }

    for idx, category in enumerate(categories):
        active_class = ' active' if idx == 0 else ''
        label_class = 'highlight' if category != 'world' else ''

        html_content += f"""
  <section id="{category}" class="news-section{active_class}">
    <div class="section-label {label_class}">{section_labels[category]}</div>
    <div class="grid">
"""

        articles = news_by_category.get(category, [])
        for article in articles:
            # Escape HTML in article content
            headline = html.escape(article.get('headline', 'Breaking News')[:80])
            summary = html.escape(article.get('summary', 'Read more'))
            source = html.escape(article.get('source', 'News'))
            url = html.escape(article.get('url', '#'))

            html_content += f"""      <article>
        <div class="kicker">{category.upper()}</div>
        <h3 class="headline">{headline}</h3>
        <p class="body-copy">{summary}</p>
        <a class="read-more" href="{url}" target="_blank" rel="noopener">Read Full Story →</a>
        <p class="source-tag">Source: <a href="{url}" target="_blank" rel="noopener">{source}</a></p>
      </article>
"""

        html_content += """    </div>
  </section>
"""

    # Add ticker and footer
    html_content += f"""
  <div class="ticker">
    <span>⬥ Real news updated daily from NewsAPI & RSS feeds</span>
    <span>⬥ All stories link to original sources</span>
    <span>⬥ Auto-published daily at 7 AM EST via GitHub Actions</span>
    <span>⬥ The Triangle Tribune: All the news fit to read</span>
  </div>

  <footer>
    The Triangle Tribune · Digital Morning Edition · {date_str}<br>
    Serving Raleigh, Durham, Chapel Hill, Cary & the Research Triangle · Auto-published via GitHub Actions
  </footer>

</div>
</div>

<script>
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('.news-section');

  navLinks.forEach(link => {{
    link.addEventListener('click', (e) => {{
      e.preventDefault();
      const targetSection = link.getAttribute('data-section');

      sections.forEach(section => section.classList.remove('active'));
      navLinks.forEach(l => l.classList.remove('active'));

      document.getElementById(targetSection).classList.add('active');
      link.classList.add('active');

      if (window.innerWidth < 768) {{
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
      }}
    }});
  }});
</script>

</body>
</html>
"""

    return html_content

def main():
    print("📰 Generating The Triangle Tribune with real news...")

    # Fetch real news
    news_by_category = fetch_today_news()

    # Generate HTML
    html = generate_html(news_by_category)

    # Save to index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    total_stories = sum(len(stories) for stories in news_by_category.values())
    print(f"✅ Generated index.html with {total_stories} REAL stories across 7 categories")
    print("📡 Sources: NewsAPI + RSS feeds from BBC, Reuters, CNN, WRAL, ESPN, TechCrunch, Nature, Bloomberg")

if __name__ == '__main__':
    main()
