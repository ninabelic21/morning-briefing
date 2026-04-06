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

# ─── Config ───────────────────────────────────────────────────────────────────

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
DATE_STR = TODAY.strftime("%B %d, %Y")
DATE_SHORT = TODAY.strftime("%Y-%m-%d")
WEEKDAY = TODAY.strftime("%A")

# ─── Data Fetching ────────────────────────────────────────────────────────────────

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
                "name": name,
                "value": round(close, 2),
                "change": round(daily_change, 2),
                "weekChange": round(weekly_change, 2)
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

# ─── AI Summarization ─────────────────────────────────────────────────────────────

def generate_digest_content(news_headlines, rss_feeds, indices, sectors, watchlist):
    """Use Claude to synthesize raw data into a polished digest."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

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

Indices:
{json.dumps(indices)}

Sectors:
{json.dumps(sectors)}

Watchlist:
{json.dumps(watchlist)}
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

    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(text[start:end])

    return {
        "tech": "Unable to generate digest today.",
        "politics_world": "",
        "politics_austria": "",
        "markets": "",
        "geopolitics": "",
        "spotlight_title": "Daily Update",
        "spotlight_text": "",
        "spotlight_stats": []
    }

# ─── Data.js Generation ────────────────────────────────────────────────────────────

def generate_data_js(digest, indices, sectors, watchlist):
    """Generate data.js with all briefing data in JSON format."""

    is_weekend = TODAY.weekday() >= 5
    if is_weekend:
        market_note = f"Markets closed (weekend) · Last trading data shown"
        trading = {"closedMessage": "Markets closed today"}
    else:
        market_note = f"Data as of latest market close"
        trading = {}

    market_ribbon = []
    for idx in indices:
        market_ribbon.append({
            "label": idx["name"],
            "value": f"{idx['value']:,.2f}",
            "change": f"+{idx['change']:.2f}%" if idx['change'] >= 0 else f"−{abs(idx['change']):.2f}%"
        })

    digest_sections = []
    section_map = {
        "tech": {"title": "Tech & AI", "color": "#6366f1"},
        "politics_world": {"title": "World Politics", "color": "#7c3aed"},
        "politics_austria": {"title": "Austria", "color": "#d946ef"},
        "markets": {"title": "Stock Market", "color": "#16a34a"},
        "geopolitics": {"title": "Geopolitics", "color": "#ea580c"},
    }

    for key, metadata in section_map.items():
        text = digest.get(key, "")
        if text:
            digest_sections.append({
                "title": metadata["title"],
                "color": metadata["color"],
                "stories": [{
                    "headline": metadata["title"],
                    "text": text,
                    "sources": []
                }]
            })

    daily_change = []
    max_change = max(abs(s["change"]) for s in sectors) if sectors else 2
    for s in sectors:
        width = max(min(abs(s["change"]) / max_change * 100, 100), 3) if max_change > 0 else 3
        daily_change.append({
            "label": s["name"],
            "change": f"+{s['change']:.2f}%" if s["change"] >= 0 else f"−{abs(s['change']):.2f}%",
            "width": width
        })

    sector_data = []
    for s in sectors:
        intensity = min(abs(s["change"]) / 3, 1) if s["change"] else 0
        if s["change"] >= 0:
            color = "#3D7A47"
            bg = f"rgba(22,163,74,{0.08 + intensity * 0.25:.2f})"
        else:
            color = "#B5342B"
            bg = f"rgba(220,38,38,{0.08 + intensity * 0.25:.2f})"

        sector_data.append({
            "name": s["name"],
            "value": f"+{s['change']:.1f}%" if s["change"] >= 0 else f"−{abs(s['change']):.1f}%",
            "color": color,
            "bg": bg
        })

    sorted_wl = sorted(watchlist, key=lambda x: x["change"], reverse=True)
    max_wl_change = max(abs(w["change"]) for w in sorted_wl) if sorted_wl else 2

    watchlist_items = []
    wl_chart = []
    for w in sorted_wl:
        width = max(min(abs(w["change"]) / max_wl_change * 90, 98), 3) if max_wl_change > 0 else 3
        curr_sym = "€" if w["currency"] == "EUR" else "$"

        watchlist_items.append({
            "ticker": w["ticker"],
            "name": w["name"],
            "priceEUR": f"{w['price']:.2f}" if w["currency"] == "EUR" else "",
            "priceUSD": f"{w['price']:,.2f}" if w["currency"] == "USD" else "",
            "change": f"+{w['change']:.2f}%" if w["change"] >= 0 else f"−{abs(w['change']):.2f}%"
        })

        wl_chart.append({
            "label": w["ticker"],
            "change": f"+{w['change']:.2f}%" if w["change"] >= 0 else f"−{abs(w['change']):.2f}%",
            "width": width
        })

    watchlist_data = {
        "note": "Your personal watchlist",
        "periods": {
            "daily": {"chart": wl_chart, "items": watchlist_items},
            "weekly": {"chart": wl_chart, "items": watchlist_items},
            "monthly": {"chart": wl_chart, "items": watchlist_items},
            "threeMonth": {"chart": wl_chart, "items": watchlist_items}
        }
    }

    markets_data = {
        "dailyChange": daily_change,
        "sectors": sector_data
    }

    spotlight_stats = digest.get("spotlight_stats", [])
    spotlight_data = {
        "tag": "Market Insight",
        "title": digest.get("spotlight_title", "Today's Spotlight"),
        "intro": digest.get("spotlight_text", ""),
        "stats": spotlight_stats,
        "charts": [],
        "legend": [],
        "sources": []
    }

    briefing_data = {
        "date": f"{WEEKDAY}, {DATE_STR}",
        "greeting": "Good Morning, Caroline",
        "subtitle": market_note,
        "trading": trading,
        "marketRibbon": market_ribbon,
        "digest": digest_sections,
        "markets": markets_data,
        "watchlist": watchlist_data,
        "spotlight": spotlight_data,
        "footer": f"Generated {DATE_STR} · Not financial advice"
    }

    js_code = "window.BRIEFING = " + json.dumps(briefing_data, indent=2, ensure_ascii=False) + ";"
    return js_code

# ─── Main ────────────────────────────────────────────────────────────────────

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

    print("Generating data.js...")
    data_js = generate_data_js(digest, indices, sectors, watchlist)

    # Write to data.js (GitHub Pages will serve this)
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(data_js)

    print(f"Done! data.js generated ({len(data_js):,} bytes)")

if __name__ == "__main__":
    main()
