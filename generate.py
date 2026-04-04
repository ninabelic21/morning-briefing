#!/usr/bin/env python3
"""
Morning Briefing Generator — Autonomous daily news digest for Caroline.
Runs via GitHub Actions on cron schedule. No laptop required.
"""

import os
import json
import datetime
import feedparser
import yfinance as yf
import anthropic
import requests

# ─── Config ───────────────────────────────────────────────────────────
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

WATCHLIST = [
    {"ticker": "NVDA", "name": "NVIDIA", "currency": "USD"},
    {"ticker": "WMT", "name": "Walmart", "currency": "USD"},
    {"ticker": "LLY", "name": "Eli Lilly", "currency": "USD"},
    {"ticker": "MSFT", "name": "Microsoft", "currency": "USD"},
    {"ticker": "MPWR", "name": "Monolithic Power", "currency": "USD"},
    {"ticker": "EIMI.L", "name": "iShares MSCI EM", "currency": "EUR", "display_ticker": "A0RPWJ"},
    {"ticker": "LCWL.DE", "name": "Amundi MSCI World", "currency": "EUR", "display_ticker": "ETF146"},
]

SECTOR_ETFS = [
    ("XLK", "Technology"), ("XLV", "Healthcare"), ("XLF", "Financials"),
    ("XLE", "Energy"), ("XLY", "Consumer"), ("XLI", "Industrial"),
    ("XLB", "Materials"), ("XLU", "Utilities"), ("XLRE", "Real Estate"),
    ("XLC", "Telecom"),
]

INDEX_TICKERS = [
    ("^GSPC", "S&P 500"), ("^IXIC", "NASDAQ"), ("^DJI", "Dow Jones"), ("^GDAXI", "DAX"),
]

RSS_FEEDS = {
    "austria": [
        "https://www.thelocal.at/tag/politics/rss",
    ],
    "geopolitics": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
    ],
}

TODAY = datetime.date.today()
DATE_STR = TODAY.strftime("%B %d, %Y")  # e.g. "April 7, 2026"
DATE_SHORT = TODAY.strftime("%Y-%m-%d")
WEEKDAY = TODAY.strftime("%A")


# ─── Data Fetching ────────────────────────────────────────────────────

def fetch_stock_data(tickers_list):
    """Fetch current price and daily change for a list of tickers."""
    results = []
    for item in tickers_list:
        ticker = item if isinstance(item, str) else item["ticker"]
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            if len(hist) >= 2:
                close = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2]
                change = ((close - prev) / prev) * 100
            elif len(hist) == 1:
                close = hist["Close"].iloc[-1]
                change = 0.0
            else:
                close = 0.0
                change = 0.0
            results.append({"ticker": ticker, "price": round(close, 2), "change": round(change, 2)})
        except Exception as e:
            results.append({"ticker": ticker, "price": 0.0, "change": 0.0, "error": str(e)})
    return results


def fetch_indices():
    """Fetch major index data including weekly performance."""
    results = []
    for ticker, name in INDEX_TICKERS:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="7d")
            if len(hist) >= 2:
                close = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2]
                daily_change = ((close - prev) / prev) * 100
                week_start = hist["Close"].iloc[0]
                weekly_change = ((close - week_start) / week_start) * 100
            else:
                close = 0.0
                daily_change = 0.0
                weekly_change = 0.0
            results.append({
                "name": name, "value": round(close, 2),
                "change": round(daily_change, 2), "weekChange": round(weekly_change, 2)
            })
        except Exception:
            results.append({"name": name, "value": 0, "change": 0, "weekChange": 0})
    return results


def fetch_sectors():
    """Fetch sector ETF daily performance."""
    results = []
    for ticker, name in SECTOR_ETFS:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            if len(hist) >= 2:
                change = ((hist["Close"].iloc[-1] - hist["Close"].iloc[-2]) / hist["Close"].iloc[-2]) * 100
            else:
                change = 0.0
            results.append({"name": name, "change": round(change, 2)})
        except Exception:
            results.append({"name": name, "change": 0.0})
    return results


def fetch_watchlist():
    """Fetch watchlist stock data."""
    results = []
    raw = fetch_stock_data(WATCHLIST)
    for item, data in zip(WATCHLIST, raw):
        results.append({
            "ticker": item.get("display_ticker", item["ticker"]),
            "name": item["name"],
            "price": data["price"],
            "change": data["change"],
            "currency": item["currency"],
        })
    return results


def fetch_news_headlines():
    """Fetch news from NewsAPI across multiple categories."""
    categories = {
        "tech": "artificial intelligence OR cybersecurity OR tech company",
        "politics": "US politics OR EU politics OR European Union OR NATO",
        "geopolitics": "conflict OR diplomacy OR trade war OR sanctions",
        "markets": "stock market OR S&P 500 OR NASDAQ OR Wall Street",
    }
    all_articles = {}
    for cat, query in categories.items():
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 8,
                "apiKey": NEWSAPI_KEY,
            }
            resp = requests.get(url, params=params, timeout=15)
            data = resp.json()
            articles = data.get("articles", [])
            all_articles[cat] = [
                {"title": a.get("title", ""), "description": a.get("description", ""), "source": a.get("source", {}).get("name", "")}
                for a in articles if a.get("title") and "[Removed]" not in a.get("title", "")
            ][:6]
        except Exception:
            all_articles[cat] = []
    return all_articles


def fetch_rss_feeds():
    """Fetch RSS feeds for Austrian news and geopolitics."""
    results = {}
    for category, urls in RSS_FEEDS.items():
        items = []
        for url in urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:
                    items.append({
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", "")[:200],
                    })
            except Exception:
                pass
        results[category] = items
    return results


# ─── AI Summarization ─────────────────────────────────────────────────

def generate_digest_content(news_headlines, rss_feeds, indices, sectors, watchlist):
    """Use Claude to synthesize raw data into a polished digest."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Build context for Claude
    context = f"""Today is {WEEKDAY}, {DATE_STR}.

## Raw News Headlines (from NewsAPI)
### Tech:
{json.dumps(news_headlines.get('tech', []), indent=2)}

### World Politics:
{json.dumps(news_headlines.get('politics', []), indent=2)}

### Geopolitics:
{json.dumps(news_headlines.get('geopolitics', []), indent=2)}

### Markets:
{json.dumps(news_headlines.get('markets', []), indent=2)}

## Austrian News (RSS):
{json.dumps(rss_feeds.get('austria', []), indent=2)}

## Geopolitics RSS:
{json.dumps(rss_feeds.get('geopolitics', []), indent=2)}

## Market Data:
Indices: {json.dumps(indices)}
Sectors: {json.dumps(sectors)}
Watchlist: {json.dumps(watchlist)}
"""

    prompt = f"""You are writing Caroline's daily morning news briefing. Using the raw data below, write a polished digest.

{context}

Write exactly these sections, each as 2-3 substantive paragraphs (5-10 sentences total per section). Use plain text, no markdown:

1. TECH — AI, cybersecurity, major tech news
2. POLITICS_WORLD — US, EU, major global political events
3. POLITICS_AUSTRIA — Austrian domestic politics, policy. If no Austrian news found, write about recent Austrian developments you know about.
4. MARKETS — Index performance, notable movers, economic data context
5. GEOPOLITICS — Conflicts, diplomacy, trade tensions
6. SPOTLIGHT_TITLE — A short title for today's most compelling data story
7. SPOTLIGHT_TEXT — 2-3 paragraphs about the spotlight topic
8. SPOTLIGHT_STATS — 4 key stats as "label:value" pairs, comma-separated

Format your response as JSON:
{{
  "tech": "paragraph text...",
  "politics_world": "paragraph text...",
  "politics_austria": "paragraph text...",
  "markets": "paragraph text...",
  "geopolitics": "paragraph text...",
  "spotlight_title": "short title",
  "spotlight_text": "paragraph text...",
  "spotlight_stats": [
    {{"label": "Label", "value": "Value", "color": "green|red|gold|accent"}},
    ...
  ]
}}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    # Extract JSON from response
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(text[start:end])
    return {
        "tech": "Unable to generate digest today.",
        "politics_world": "", "politics_austria": "", "markets": "",
        "geopolitics": "", "spotlight_title": "Daily Update",
        "spotlight_text": "", "spotlight_stats": []
    }


# ─── HTML Generation ──────────────────────────────────────────────────

def generate_html(digest, indices, sectors, watchlist):
    """Generate the full standalone HTML page."""

    # Determine market status
    is_weekend = TODAY.weekday() >= 5
    if is_weekend:
        market_note = f"Markets closed (weekend) · Last trading data shown"
    else:
        market_note = f"Data as of latest market close"

    # Build index ribbon
    ribbon_html = ""
    for idx in indices:
        arrow = "▲" if idx["change"] >= 0 else "▼"
        badge_class = "up" if idx["change"] >= 0 else "down"
        ribbon_html += f'''<div class="ribbon-item"><div class="label">{idx["name"]}</div><div class="value">{idx["value"]:,.2f}</div><span class="badge {badge_class}">{arrow} {abs(idx["change"]):.2f}%</span></div>\n'''

    # Build sector heatmap
    heatmap_html = ""
    for s in sectors:
        intensity = min(abs(s["change"]) / 3, 1)
        if s["change"] >= 0:
            bg = f"rgba(34,197,94,{0.12 + intensity * 0.4:.2f})"
            color = "var(--green)"
            sign = "+"
        else:
            bg = f"rgba(239,68,68,{0.12 + intensity * 0.4:.2f})"
            color = "var(--red)"
            sign = ""
        heatmap_html += f'<div class="heat-cell" style="background:{bg}"><div class="name">{s["name"]}</div><div class="val" style="color:{color}">{sign}{s["change"]:.1f}%</div></div>\n'

    # Build daily index bars
    max_weekly = max(abs(idx["weekChange"]) for idx in indices) if indices else 5
    index_daily_bars = ""
    index_weekly_bars = ""
    for idx in indices:
        # Daily
        width = max(min(abs(idx["change"]) / 2 * 100, 100), 3)
        fill_class = "positive" if idx["change"] >= 0 else "negative"
        sign = "+" if idx["change"] >= 0 else ""
        color = "var(--green)" if idx["change"] >= 0 else "var(--red)"
        index_daily_bars += f'<div class="bar-row"><span class="bar-label">{idx["name"]}</span><div class="bar-track"><div class="bar-fill {fill_class}" style="width:{width:.0f}%"></div></div><span class="bar-value" style="color:{color}">{sign}{idx["change"]:.2f}%</span></div>\n'
        # Weekly
        width_w = max(min(abs(idx["weekChange"]) / max_weekly * 90, 95), 3)
        fill_class_w = "positive" if idx["weekChange"] >= 0 else "negative"
        sign_w = "+" if idx["weekChange"] >= 0 else ""
        color_w = "var(--green)" if idx["weekChange"] >= 0 else "var(--red)"
        label_inside = f'{sign_w}{idx["weekChange"]:.1f}%' if width_w > 20 else ""
        index_weekly_bars += f'<div class="bar-row"><span class="bar-label">{idx["name"]}</span><div class="bar-track"><div class="bar-fill {fill_class_w}" style="width:{width_w:.0f}%">{label_inside}</div></div><span class="bar-value" style="color:{color_w}">{sign_w}{idx["weekChange"]:.2f}%</span></div>\n'

    # Build watchlist
    sorted_wl = sorted(watchlist, key=lambda x: x["change"], reverse=True)
    max_wl_change = max(abs(w["change"]) for w in sorted_wl) if sorted_wl else 2

    wl_rows = ""
    wl_bars = ""
    for w in watchlist:
        arrow = "▲" if w["change"] >= 0 else "▼"
        badge_class = "up" if w["change"] >= 0 else "down"
        curr = "€" if w["currency"] == "EUR" else "$"
        wl_rows += f'<div class="watchlist-row"><div><span class="ticker">{w["ticker"]}</span><span class="name">{w["name"]}</span></div><div class="right"><span class="price">{curr}{w["price"]:,.2f}</span><span class="badge {badge_class}">{arrow} {abs(w["change"]):.2f}%</span></div></div>\n'

    for w in sorted_wl:
        width = max(min(abs(w["change"]) / max_wl_change * 90, 98), 3)
        fill_class = "positive" if w["change"] >= 0 else "negative"
        sign = "+" if w["change"] >= 0 else ""
        color = "var(--green)" if w["change"] >= 0 else "var(--red)"
        label = f'{sign}{w["change"]:.2f}%' if width > 15 else ""
        wl_bars += f'<div class="bar-row"><span class="bar-label">{w["ticker"]}</span><div class="bar-track"><div class="bar-fill {fill_class}" style="width:{width:.0f}%">{label}</div></div><span class="bar-value" style="color:{color}">{sign}{w["change"]:.2f}%</span></div>\n'

    # Build spotlight stats
    spotlight_stats_html = ""
    for stat in digest.get("spotlight_stats", []):
        color = {
            "green": "var(--green)", "red": "var(--red)",
            "gold": "var(--gold)", "accent": "var(--accent-light)"
        }.get(stat.get("color", "accent"), "var(--accent-light)")
        spotlight_stats_html += f'<div class="spotlight-stat"><div class="num" style="color:{color}">{stat["value"]}</div><div class="lab">{stat["label"]}</div></div>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Morning Briefing — {DATE_STR}</title>
<style>
  :root {{
    --bg: #0f1117; --card: #1a1d27; --text: #e2e8f0; --muted: #94a3b8;
    --green: #22c55e; --red: #ef4444; --accent: #6366f1; --accent-light: #818cf8;
    --border: #2d3148; --gold: #f59e0b; --green-bg: rgba(34,197,94,0.12); --red-bg: rgba(239,68,68,0.12);
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--text); font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; }}
  .header {{ background: linear-gradient(135deg, #1e1b4b, #312e81); padding: 28px 20px 20px; border-bottom: 1px solid var(--border); }}
  .header h1 {{ font-size: 24px; font-weight: 700; letter-spacing: -0.5px; }}
  .header p {{ color: var(--muted); font-size: 13px; margin-top: 4px; }}
  .container {{ max-width: 900px; margin: 0 auto; padding: 0 16px; }}
  .tabs {{ display: flex; gap: 4px; border-bottom: 1px solid var(--border); padding-top: 12px; overflow-x: auto; }}
  .tabs input[type="radio"] {{ display: none; }}
  .tabs label {{ padding: 10px 14px; font-size: 13px; color: var(--muted); cursor: pointer; border-bottom: 2px solid transparent; white-space: nowrap; transition: all 0.2s; }}
  .tabs label:hover {{ color: var(--text); }}
  .tab-content {{ display: none; padding: 20px 0 40px; }}
  #tab-digest:checked ~ .tab-content.digest-content,
  #tab-markets:checked ~ .tab-content.markets-content,
  #tab-watchlist:checked ~ .tab-content.watchlist-content,
  #tab-spotlight:checked ~ .tab-content.spotlight-content {{ display: block; }}
  #tab-digest:checked ~ .tabs label[for="tab-digest"],
  #tab-markets:checked ~ .tabs label[for="tab-markets"],
  #tab-watchlist:checked ~ .tabs label[for="tab-watchlist"],
  #tab-spotlight:checked ~ .tabs label[for="tab-spotlight"] {{ color: var(--text); border-bottom-color: var(--accent); font-weight: 600; background: var(--card); border-radius: 8px 8px 0 0; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px; }}
  .card h3 {{ font-size: 17px; margin-bottom: 12px; }}
  .card p {{ color: var(--muted); font-size: 14px; margin-bottom: 10px; }}
  .ribbon {{ display: flex; gap: 10px; margin-bottom: 20px; overflow-x: auto; padding-bottom: 4px; }}
  .ribbon-item {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 10px 14px; flex: 1 0 120px; min-width: 120px; }}
  .ribbon-item .label {{ font-size: 11px; color: var(--muted); }}
  .ribbon-item .value {{ font-size: 15px; font-weight: 600; margin: 2px 0; }}
  .badge {{ font-size: 13px; font-weight: 600; padding: 2px 7px; border-radius: 5px; display: inline-block; }}
  .badge.up {{ color: var(--green); background: var(--green-bg); }}
  .badge.down {{ color: var(--red); background: var(--red-bg); }}
  .bar-chart {{ margin: 12px 0; }}
  .bar-row {{ display: flex; align-items: center; margin-bottom: 8px; }}
  .bar-label {{ width: 90px; font-size: 12px; color: var(--muted); flex-shrink: 0; }}
  .bar-track {{ flex: 1; height: 24px; background: rgba(255,255,255,0.04); border-radius: 4px; position: relative; overflow: hidden; }}
  .bar-fill {{ height: 100%; border-radius: 4px; display: flex; align-items: center; padding: 0 8px; font-size: 11px; font-weight: 600; min-width: 40px; transition: width 0.6s ease; }}
  .bar-fill.positive {{ background: var(--green); color: #fff; }}
  .bar-fill.negative {{ background: var(--red); color: #fff; }}
  .bar-value {{ font-size: 12px; color: var(--muted); width: 55px; text-align: right; flex-shrink: 0; margin-left: 8px; }}
  .heatmap {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 8px; }}
  .heat-cell {{ border-radius: 8px; padding: 12px 10px; text-align: center; }}
  .heat-cell .name {{ font-size: 13px; font-weight: 500; }}
  .heat-cell .val {{ font-size: 15px; font-weight: 700; margin-top: 4px; }}
  .watchlist-row {{ display: flex; justify-content: space-between; align-items: center; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; }}
  .watchlist-row .ticker {{ font-weight: 700; font-size: 15px; }}
  .watchlist-row .name {{ color: var(--muted); font-size: 13px; margin-left: 8px; }}
  .watchlist-row .right {{ display: flex; align-items: center; gap: 14px; }}
  .watchlist-row .price {{ font-weight: 600; font-size: 15px; }}
  .spotlight-stat {{ text-align: center; }}
  .spotlight-stat .num {{ font-size: 22px; font-weight: 700; }}
  .spotlight-stat .lab {{ font-size: 12px; color: var(--muted); margin-top: 2px; }}
  .stat-grid {{ display: flex; justify-content: space-around; flex-wrap: wrap; gap: 12px; margin-top: 20px; }}
  footer {{ text-align: center; padding: 16px; color: var(--muted); font-size: 12px; border-top: 1px solid var(--border); }}
  @media (max-width: 600px) {{
    .header h1 {{ font-size: 20px; }}
    .ribbon {{ gap: 8px; }}
    .ribbon-item {{ flex: 1 0 100px; min-width: 100px; padding: 8px 10px; }}
    .heatmap {{ grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); }}
    .watchlist-row {{ flex-wrap: wrap; gap: 8px; }}
    .stat-grid {{ gap: 8px; }}
  }}
</style>
</head>
<body>

<div class="header">
  <div class="container">
    <h1>Good Morning, Caroline</h1>
    <p>{WEEKDAY}, {DATE_STR} &middot; {market_note}</p>
  </div>
</div>

<div class="container">
  <input type="radio" name="tabs" id="tab-digest" checked>
  <input type="radio" name="tabs" id="tab-markets">
  <input type="radio" name="tabs" id="tab-watchlist">
  <input type="radio" name="tabs" id="tab-spotlight">

  <div class="tabs">
    <label for="tab-digest">Digest</label>
    <label for="tab-markets">Markets</label>
    <label for="tab-watchlist">Watchlist</label>
    <label for="tab-spotlight">Spotlight</label>
  </div>

  <div class="tab-content digest-content">
    <div class="ribbon">
      {ribbon_html}
    </div>

    <div class="card">
      <h3>Tech &amp; AI</h3>
      <p>{digest.get("tech", "No tech news available today.")}</p>
    </div>

    <div class="card">
      <h3>World Politics</h3>
      <p>{digest.get("politics_world", "No world politics news available today.")}</p>
    </div>

    <div class="card">
      <h3>Austria</h3>
      <p>{digest.get("politics_austria", "No Austrian news available today.")}</p>
    </div>

    <div class="card">
      <h3>Stock Market</h3>
      <p>{digest.get("markets", "No market commentary available today.")}</p>
    </div>

    <div class="card">
      <h3>Geopolitics</h3>
      <p>{digest.get("geopolitics", "No geopolitics news available today.")}</p>
    </div>
  </div>

  <div class="tab-content markets-content">
    <div class="card">
      <h3>Daily Index Performance</h3>
      <div class="bar-chart">
        {index_daily_bars}
      </div>
    </div>
    <div class="card">
      <h3>Weekly Performance</h3>
      <div class="bar-chart">
        {index_weekly_bars}
      </div>
    </div>
    <div class="card">
      <h3>Sector Heatmap</h3>
      <div class="heatmap">
        {heatmap_html}
      </div>
    </div>
  </div>

  <div class="tab-content watchlist-content">
    <div class="card">
      <h3>Your Watchlist</h3>
      {wl_rows}
    </div>
    <div class="card">
      <h3>Watchlist Daily Changes</h3>
      <div class="bar-chart">
        {wl_bars}
      </div>
    </div>
  </div>

  <div class="tab-content spotlight-content">
    <div class="card">
      <h3>{digest.get("spotlight_title", "Today's Spotlight")}</h3>
      <p>{digest.get("spotlight_text", "No spotlight content available today.")}</p>
      <div class="stat-grid">
        {spotlight_stats_html}
      </div>
    </div>
  </div>

</div>

<footer>Generated {DATE_STR} &middot; Not financial advice</footer>

</body>
</html>"""
    return html


# ─── Main ─────────────────────────────────────────────────────────────

def main():
    print(f"Generating morning briefing for {DATE_STR}...")

    print("Fetching indices...")
    indices = fetch_indices()

    print("Fetching sectors...")
    sectors = fetch_sectors()

    print("Fetching watchlist...")
    watchlist = fetch_watchlist()

    print("Fetching news headlines...")
    news = fetch_news_headlines()

    print("Fetching RSS feeds...")
    rss = fetch_rss_feeds()

    print("Generating digest with Claude...")
    digest = generate_digest_content(news, rss, indices, sectors, watchlist)

    print("Generating HTML...")
    html = generate_html(digest, indices, sectors, watchlist)

    # Write to index.html (GitHub Pages will serve this)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done! index.html generated ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
