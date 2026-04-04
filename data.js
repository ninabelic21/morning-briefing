window.BRIEFING = {
  date: "Saturday, April 4, 2026",
  greeting: "Good Morning, Caroline",
  subtitle: "Markets closed \u00b7 Good Friday weekend \u00b7 Last trading: April 2",

  marketRibbon: [
    { label: "S&P 500", value: "6,582.69", change: "+0.11%" },
    { label: "NASDAQ", value: "21,879.18", change: "+0.18%" },
    { label: "Dow", value: "46,504.67", change: "\u22120.13%" },
    { label: "DAX", value: "22,772", change: "\u22122.26%" }
  ],

  digest: [
    {
      title: "Tech & AI",
      color: "#8B6834",
      stories: [
        {
          headline: "Three Frontier Models Race for Supremacy",
          text: "Three frontier AI models launched in quick succession this spring. OpenAI released GPT-5.4 on March 5 in Standard, Pro, and Thinking variants, featuring a 1-million token context window and 75% computer use capability on the OSWorld benchmark \u2014 a 27.7pp jump over GPT-5.2. The model is 33% less likely to make individual claim errors compared to its predecessor. Google followed with Gemini 3.1 Pro, achieving 77.1% on the ARC-AGI-2 benchmark for novel logic pattern-solving, with a 1-million token context window spanning text, audio, images, video, and code. Meanwhile, xAI\u2019s Grok 4.20 moved from beta to production in February, posting a 78% non-hallucination rate \u2014 the highest of any tested model \u2014 using a novel 4-agent architecture where parallel agents cross-verify outputs.",
          sources: [
            { name: "TechCrunch", url: "https://techcrunch.com/2026/03/05/openai-launches-gpt-5-4-with-pro-and-thinking-versions/" },
            { name: "Google AI Blog", url: "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/" },
            { name: "WinBuzzer", url: "https://winbuzzer.com/2026/03/25/xai-grok-420-honesty-record-intelligence-gap-xcxwbn/" }
          ]
        },
        {
          headline: "Meta\u2019s Custom Chip Play & the Agentic Safety Gap",
          text: "Meta unveiled four custom MTIA chip generations for AI inference, with MTIA 300 already deployed and MTIA 400, 450, and 500 following on a six-month cadence through 2027. Developed with Broadcom, the chips reduce Meta\u2019s dependency on NVIDIA and AMD, handling ranking, recommendations training, and GenAI inference workloads. The industry\u2019s pivot to agentic AI continues: Google\u2019s Gemma 4 (April 2) delivered strong agentic workflow performance, while OpenClaw surpassed 302,000 GitHub stars as the fastest-growing autonomous agent framework. However, security research reveals multi-agent systems have safety pass rates as low as 7.1%, highlighting significant risks in production deployments.",
          sources: [
            { name: "Meta AI Blog", url: "https://ai.meta.com/blog/meta-mtia-scale-ai-chips-for-billions/" },
            { name: "Tom\u2019s Hardware", url: "https://www.tomshardware.com/tech-industry/semiconductors/meta-reveals-four-new-mtia-chips-built-for-ai-inference" },
            { name: "Defense One", url: "https://www.defenseone.com/technology/2026/04/startup-takes-different-approach-ai-assistants/412545/" }
          ]
        },
        {
          headline: "Anthropic Cuts Agent Access; AGS Health Eyes $500M IPO",
          text: "Effective today (April 4), Anthropic ended third-party agentic tool access for Claude subscribers, specifically targeting platforms like OpenClaw that placed \u2018outsized strain\u2019 on infrastructure. Users must migrate to pay-as-you-go API pricing for agent workflows, though Anthropic offered a one-time credit and up to 30% discount on pre-purchased usage bundles. Separately, Blackstone-owned AGS Health filed for a $500M IPO in India targeting a $3B valuation, backed by AI-driven medical coding and billing technology for US healthcare providers. The offering, advised by JM Financial, Jefferies, and JP Morgan, is expected late April or May.",
          sources: [
            { name: "VentureBeat", url: "https://venturebeat.com/technology/anthropic-cuts-off-the-ability-to-use-claude-subscriptions-with-openclaw-and" },
            { name: "Bloomberg", url: "https://www.bloomberg.com/news/articles/2026-04-02/blackstone-s-ags-health-said-to-file-for-500-million-india-ipo" }
          ]
        }
      ]
    },
    {
      title: "World Politics",
      color: "#7D5A2F",
      stories: [
        {
          headline: "Hungary\u2019s Watershed Vote: Orb\u00e1n Faces Strongest Challenge in 16 Years",
          text: "Europe\u2019s most consequential 2026 vote takes place April 12 in Hungary, where Prime Minister Viktor Orb\u00e1n \u2014 in power for 16 years \u2014 faces challenger P\u00e9ter Magyar\u2019s center-right Tisza party. Magyar\u2019s movement, which won 30% in last year\u2019s EU Parliament elections, is pro-European and seeks to restore frozen EU funds and reduce Budapest\u2019s ties to Moscow. Polls are deeply polarized: PolitPro shows Tisza at 48.7% vs. Fidesz/KDNP at 40.8%, while the Orb\u00e1n-aligned N\u00e9z\u0151pont institute puts Fidesz ahead 46\u201340. Under Orb\u00e1n, Hungary has blocked EU asylum reform, defense coordination, energy autonomy measures, Ukraine\u2019s membership talks, and \u20ac90B in collective loans. Hungary\u2019s economy grew only 0.5% on average in 2024\u20132025 with a 5% budget deficit \u2014 well above the 3% EU target \u2014 making economic stagnation a central campaign issue.",
          sources: [
            { name: "CSIS Analysis", url: "https://www.csis.org/analysis/what-stake-hungarys-election" },
            { name: "Euronews", url: "https://www.euronews.com/my-europe/2026/04/03/podcast-everything-you-need-to-know-about-the-hungarian-elections" },
            { name: "Carnegie Endowment", url: "https://carnegieendowment.org/europe/strategic-europe/2026/04/win-or-lose-orban-has-broken-hungarys-democracy" }
          ]
        },
        {
          headline: "Liberation Day at One Year: Tariffs Struck Down, Fresh Ones Imposed",
          text: "April 2 marked the one-year anniversary of Trump\u2019s \u2018Liberation Day\u2019 Executive Order 14257, which imposed sweeping reciprocal tariffs including 34% on China, 20% on the EU, and 46% on Vietnam. The initial shock sent US stocks plunging 12.4% \u2014 the biggest drop since COVID-19 \u2014 before a 9.52% single-day surge when parts of the policy were paused, the largest one-day S&P 500 gain since 2008. The US Court of International Trade vacated the tariffs in May 2025, the Federal Circuit affirmed in August, and in February 2026 the Supreme Court upheld the ruling in Learning Resources v. Trump, finding the use of emergency powers exceeded constitutional authority. Despite this, the government collected $166B from over 330,000 businesses before the ruling. On the anniversary, Trump imposed fresh 100% tariffs on patented pharmaceuticals and 50% on goods with high aluminum, steel, or copper content.",
          sources: [
            { name: "Bloomberg", url: "https://www.bloomberg.com/news/newsletters/2026/03/30/trump-liberation-day-tariff-anniversary" },
            { name: "NPR", url: "https://www.npr.org/2026/04/02/nx-s1-5766424/trump-tariffs-inflation-economy" },
            { name: "Wikipedia", url: "https://en.wikipedia.org/wiki/Liberation_Day_tariffs" }
          ]
        },
        {
          headline: "MEP Hassan Detained in France; NATO Allies Hit 2% Target",
          text: "In France, Palestinian-French MEP Rima Hassan was detained on April 2 on suspicion of \u2018apology for terrorism\u2019 over a social media post referencing the 1972 Ben Gurion Airport attack. The lawyer and Gaza conflict critic, elected to the European Parliament in 2024, was released after several hours and scheduled for trial in July. Her La France Insoumise party condemned the detention as political harassment. Meanwhile, European defense integration accelerates: all NATO allies are expected to meet the 2% GDP spending target, with a new 3.5% baseline committed at The Hague summit. European allies invested \u20ac106 billion in 2024 alone \u2014 a 42% year-over-year increase \u2014 with projected spending reaching \u20ac800 billion by 2030.",
          sources: [
            { name: "Al Jazeera", url: "https://www.aljazeera.com/news/2026/4/2/european-parliament-member-rima-hassan-taken-into-french-police-custody" },
            { name: "NATO Official", url: "https://www.nato.int/en/what-we-do/introduction-to-nato/defence-expenditures-and-natos-5-commitment" },
            { name: "EU Council", url: "https://www.consilium.europa.eu/en/policies/defence-numbers/" }
          ]
        }
      ]
    },
    {
      title: "Austria",
      color: "#A04040",
      stories: [
        {
          headline: "Fuel-Price Brake Takes Effect, Cutting Pump Prices by 10 Cents",
          text: "Austria\u2019s fuel-price brake (Spritpreisbremse) took effect April 2 at noon, cutting pump prices by 10 cents per litre through a two-part mechanism: a temporary 5-cent mineral oil tax reduction plus a mandatory 5-cent net selling price cut by fuel companies. The measure was triggered after Iran-conflict-driven oil surges caused EU benchmark prices to rise over 30% within two months. Small operators running 30 or fewer stations and highway stations are exempt. E-Control monitors compliance against relevant product quotations, and the measure automatically expires December 31, 2026. The FP\u00d6, holding 57 of 183 National Council seats as the largest opposition party, continues aggressive parliamentary scrutiny of the \u00d6VP-SP\u00d6-NEOS coalition.",
          sources: [
            { name: "Bundesministerium", url: "https://www.bmwet.gv.at/Presse/AktuellePressemeldungen/Spritpreisbremse.html" },
            { name: "Parlament.gv.at", url: "https://www.parlament.gv.at/aktuelles/pk/jahr_2026/pk0262" },
            { name: "\u00d6AMTC", url: "https://www.oeamtc.at/news/spritpreise-steigen-was-die-spritpreisbremse-bringt-85985762" }
          ]
        },
        {
          headline: "Pay Transparency Deadline Looms; Red-White-Red Card Overhaul Underway",
          text: "Austria faces a June 7 deadline to transpose the EU Pay Transparency Directive, but has not yet published a final draft law. By that date, all EU member states must implement binding rules requiring companies with 100+ employees to publish regular pay gap reports and all employers to state minimum salary ranges in job advertisements. Separately, the government\u2019s largest Red-White-Red Card reform since 2011 is underway, with a draft bill circulating for public comment. The overhaul will migrate all applications to a single online portal managed by WK\u00d6 and AMS, cutting processing times from 3\u20136 months to a guaranteed 8 weeks. For 2026, the Fachkr\u00e4fteverordnung expanded to 64 priority occupations including software developers, AI safety experts, electricians, nurses, and doctors.",
          sources: [
            { name: "Schulmeister Consulting", url: "https://www.schulmeister-consulting.com/en/magazine/overview/detail/the-eu-pay-transparency-directive-what-companies-in-austria-need-to-know-now" },
            { name: "Migration.gv.at", url: "https://www.migration.gv.at/en/types-of-immigration/permanent-immigration/other-key-workers/" }
          ]
        }
      ]
    },
    {
      title: "Stock Market",
      color: "#3D7A47",
      stories: [
        {
          headline: "Wild Intraday Swings Before Good Friday; Weekly Gains Hold Strong",
          text: "Markets closed for Good Friday (April 3) through the weekend. The last session (April 2) saw dramatic intraday swings: the Dow fell 600+ points and the S&P and NASDAQ dropped 1.5\u20132.2% in early trading on an oil surge after Trump\u2019s Iran war comments, before recovering on reports of Oman-mediated Hormuz negotiations. At close, the S&P 500 stood at 6,582.69 (+0.11%), NASDAQ at 21,879.18 (+0.18%), and the Dow at 46,504.67 (\u22120.13%). The DAX plunged 2.26% to 22,772, giving back most of the prior day\u2019s 2.73% rally. Weekly performance was strong: NASDAQ +4.4%, S&P +3.4%, Dow +3%. The March jobs report beat expectations with 178,000 nonfarm payrolls added (vs. 60,000 forecast), unemployment held at 4.3%, and healthcare led with +76,400 positions. Walmart received multiple analyst upgrades \u2014 Bernstein raised its target from $122 to $129 \u2014 with the stock trading at $125.79, up 28% over the past year on explosive advertising revenue growth (+37% YoY).",
          sources: [
            { name: "TheStreet", url: "https://www.thestreet.com/latest-news/stock-market-today-apr-2-2026-updates" },
            { name: "Motley Fool", url: "https://www.fool.com/investing/2026/04/02/dow-sp-500-nasdaq-from-morning-meltdown-to-midday/" },
            { name: "BLS", url: "https://www.bls.gov/news.release/empsit.nr0.htm" }
          ]
        }
      ]
    },
    {
      title: "Geopolitics",
      color: "#6B5B3E",
      stories: [
        {
          headline: "Hormuz Blockade Enters Fifth Week; Brent Peaked at $126",
          text: "Iran has blocked the Strait of Hormuz to shipping since US-Israeli strikes began February 28, declaring formal closure from March 4. As of April 2, Iran agreed to allow Philippine-flagged vessels to transit following talks, but the broader blockade continues. On April 4, a 40-nation coalition led by UK Foreign Secretary Yvette Cooper discussed diplomatic measures to reopen the strait, though no concrete agreements emerged. The energy impact has been severe: Brent crude exceeded $100/barrel on March 8 and peaked at $126 \u2014 the largest supply disruption since the 1970s oil crisis. Two US planes have been downed and Iran struck Gulf refineries, extending the conflict into its fifth week. The humanitarian toll extends across the region: Hezbollah\u2019s return to combat with Israel triggered a ground invasion of Lebanon, displacing over 1 million people.",
          sources: [
            { name: "Al Jazeera", url: "https://www.aljazeera.com/news/2026/4/2/can-starmers-40-nation-coalition-open-the-strait-of-hormuz" },
            { name: "CNN", url: "https://www.cnn.com/2026/04/02/world/live-news/iran-war-us-trump-oil-intl-hnk" },
            { name: "NPR", url: "https://www.npr.org/2026/04/03/g-s1-116314/iran-hits-gulf-refineries-as-trump-warns-u-s-will-attack-iranian-bridges-power-plants" }
          ]
        },
        {
          headline: "Trump\u2013Xi Summit Delayed to Mid-May Amid Iran Escalation",
          text: "Trump\u2019s originally scheduled March 31\u2013April 2 Beijing visit with Xi Jinping was postponed to mid-May, with conflicting reports suggesting a possible April 6\u20137 meeting at Mar-a-Lago. The White House attributed the delay to managing the Iran escalation and Hormuz reopening efforts, though analysts point to months of mounting frustrations and misaligned expectations. The summit could be the first of four 2026 meetings between the leaders, with topics expected to include the US-China truce set to expire November 2026, semiconductor restrictions, and rare earth export controls. UN Secretary-General Guterres warned the world is \u2018on the edge of wider war\u2019 as multiple flashpoints remain active across the Middle East.",
          sources: [
            { name: "Bloomberg", url: "https://www.bloomberg.com/news/articles/2026/03/31/trump-s-delayed-xi-summit-gives-us-china-irritants-room-to-grow" },
            { name: "The Diplomat", url: "https://thediplomat.com/2026/04/when-trump-goes-to-china-its-the-strategy-that-matters/" },
            { name: "Security Council Report", url: "https://www.securitycouncilreport.org/monthly-forecast/2026-04/the-middle-east-including-the-palestinian-question-24.php" }
          ]
        }
      ]
    }
  ],

  markets: {
    dailyChange: [
      { label: "S&P", change: "+0.11%", width: "40%" },
      { label: "NDQ", change: "+0.18%", width: "42%" },
      { label: "Dow", change: "\u22120.13%", width: "38%" },
      { label: "DAX", change: "\u22122.26%", width: "92%" }
    ],
    sectors: [
      { name: "Tech", value: "+0.45%", color: "#3D7A47", bg: "rgba(61,122,71,0.16)" },
      { name: "Healthcare", value: "\u22121.20%", color: "#B5342B", bg: "rgba(181,52,43,0.27)" },
      { name: "Financials", value: "+0.32%", color: "#3D7A47", bg: "rgba(61,122,71,0.13)" },
      { name: "Energy", value: "\u22120.78%", color: "#B5342B", bg: "rgba(181,52,43,0.21)" },
      { name: "Consumer", value: "+0.58%", color: "#3D7A47", bg: "rgba(61,122,71,0.19)" },
      { name: "Industrial", value: "\u22120.15%", color: "#B5342B", bg: "rgba(181,52,43,0.07)" },
      { name: "Materials", value: "\u22120.42%", color: "#B5342B", bg: "rgba(181,52,43,0.15)" },
      { name: "Utilities", value: "+0.21%", color: "#3D7A47", bg: "rgba(61,122,71,0.10)" },
      { name: "Telecom", value: "+0.12%", color: "#3D7A47", bg: "rgba(61,122,71,0.08)" }
    ]
  },

  watchlist: {
    note: "EUR/USD rate: ~0.862 (April 2) \u00b7 ETF prices in EUR",
    periods: {
      daily: {
        chart: [
          { label: "WMT", change: "+0.58%", width: "29%" },
          { label: "MSFT", change: "+0.25%", width: "13%" },
          { label: "ETF146", change: "\u22120.38%", width: "19%" },
          { label: "NVDA", change: "\u22120.44%", width: "22%" },
          { label: "MPWR", change: "\u22120.49%", width: "25%" },
          { label: "A0RPWJ", change: "\u22121.12%", width: "56%" },
          { label: "LLY", change: "\u22121.98%", width: "79%" }
        ],
        items: [
          { ticker: "WMT", name: "Walmart", priceEUR: "\u20ac108.44", priceUSD: "$125.79", change: "+0.58%" },
          { ticker: "MSFT", name: "Microsoft", priceEUR: "\u20ac321.88", priceUSD: "$373.46", change: "+0.25%" },
          { ticker: "ETF146", name: "Amundi MSCI World", priceEUR: "\u20ac586.26", priceUSD: "\u2014", change: "\u22120.38%" },
          { ticker: "NVDA", name: "NVIDIA", priceEUR: "\u20ac152.89", priceUSD: "$177.39", change: "\u22120.44%" },
          { ticker: "MPWR", name: "Monolithic Power", priceEUR: "\u20ac963.92", priceUSD: "$1,118.49", change: "\u22120.49%" },
          { ticker: "A0RPWJ", name: "iShares MSCI EM", priceEUR: "\u20ac56.59", priceUSD: "\u2014", change: "\u22121.12%" },
          { ticker: "LLY", name: "Eli Lilly", priceEUR: "\u20ac879.80", priceUSD: "$935.58", change: "\u22121.98%" }
        ]
      },
      weekly: {
        chart: [
          { label: "WMT", change: "+3.2%", width: "48%" },
          { label: "MSFT", change: "+2.1%", width: "32%" },
          { label: "NVDA", change: "+1.8%", width: "27%" },
          { label: "MPWR", change: "+0.9%", width: "14%" },
          { label: "ETF146", change: "\u22120.2%", width: "3%" },
          { label: "A0RPWJ", change: "\u22121.5%", width: "23%" },
          { label: "LLY", change: "\u22123.1%", width: "47%" }
        ],
        items: [
          { ticker: "WMT", name: "Walmart", priceEUR: "\u20ac108.44", priceUSD: "$125.79", change: "+3.2%" },
          { ticker: "MSFT", name: "Microsoft", priceEUR: "\u20ac321.88", priceUSD: "$373.46", change: "+2.1%" },
          { ticker: "NVDA", name: "NVIDIA", priceEUR: "\u20ac152.89", priceUSD: "$177.39", change: "+1.8%" },
          { ticker: "MPWR", name: "Monolithic Power", priceEUR: "\u20ac963.92", priceUSD: "$1,118.49", change: "+0.9%" },
          { ticker: "ETF146", name: "Amundi MSCI World", priceEUR: "\u20ac586.26", priceUSD: "\u2014", change: "\u22120.2%" },
          { ticker: "A0RPWJ", name: "iShares MSCI EM", priceEUR: "\u20ac56.59", priceUSD: "\u2014", change: "\u22121.5%" },
          { ticker: "LLY", name: "Eli Lilly", priceEUR: "\u20ac879.80", priceUSD: "$935.58", change: "\u22123.1%" }
        ]
      },
      monthly: {
        chart: [
          { label: "NVDA", change: "+8.4%", width: "84%" },
          { label: "MPWR", change: "+5.2%", width: "52%" },
          { label: "MSFT", change: "+4.1%", width: "41%" },
          { label: "WMT", change: "+2.8%", width: "28%" },
          { label: "ETF146", change: "+1.2%", width: "12%" },
          { label: "A0RPWJ", change: "\u22120.8%", width: "8%" },
          { label: "LLY", change: "\u22125.6%", width: "56%" }
        ],
        items: [
          { ticker: "NVDA", name: "NVIDIA", priceEUR: "\u20ac152.89", priceUSD: "$177.39", change: "+8.4%" },
          { ticker: "MPWR", name: "Monolithic Power", priceEUR: "\u20ac963.92", priceUSD: "$1,118.49", change: "+5.2%" },
          { ticker: "MSFT", name: "Microsoft", priceEUR: "\u20ac321.88", priceUSD: "$373.46", change: "+4.1%" },
          { ticker: "WMT", name: "Walmart", priceEUR: "\u20ac108.44", priceUSD: "$125.79", change: "+2.8%" },
          { ticker: "ETF146", name: "Amundi MSCI World", priceEUR: "\u20ac586.26", priceUSD: "\u2014", change: "+1.2%" },
          { ticker: "A0RPWJ", name: "iShares MSCI EM", priceEUR: "\u20ac56.59", priceUSD: "\u2014", change: "\u22120.8%" },
          { ticker: "LLY", name: "Eli Lilly", priceEUR: "\u20ac879.80", priceUSD: "$935.58", change: "\u22125.6%" }
        ]
      },
      threeMonth: {
        chart: [
          { label: "NVDA", change: "+14.2%", width: "71%" },
          { label: "MPWR", change: "+9.8%", width: "49%" },
          { label: "MSFT", change: "+7.3%", width: "37%" },
          { label: "WMT", change: "+6.1%", width: "31%" },
          { label: "A0RPWJ", change: "+3.4%", width: "17%" },
          { label: "ETF146", change: "+2.9%", width: "15%" },
          { label: "LLY", change: "\u22122.1%", width: "11%" }
        ],
        items: [
          { ticker: "NVDA", name: "NVIDIA", priceEUR: "\u20ac152.89", priceUSD: "$177.39", change: "+14.2%" },
          { ticker: "MPWR", name: "Monolithic Power", priceEUR: "\u20ac963.92", priceUSD: "$1,118.49", change: "+9.8%" },
          { ticker: "MSFT", name: "Microsoft", priceEUR: "\u20ac321.88", priceUSD: "$373.46", change: "+7.3%" },
          { ticker: "WMT", name: "Walmart", priceEUR: "\u20ac108.44", priceUSD: "$125.79", change: "+6.1%" },
          { ticker: "A0RPWJ", name: "iShares MSCI EM", priceEUR: "\u20ac56.59", priceUSD: "\u2014", change: "+3.4%" },
          { ticker: "ETF146", name: "Amundi MSCI World", priceEUR: "\u20ac586.26", priceUSD: "\u2014", change: "+2.9%" },
          { ticker: "LLY", name: "Eli Lilly", priceEUR: "\u20ac879.80", priceUSD: "$935.58", change: "\u22122.1%" }
        ]
      }
    }
  },

  spotlight: {
    tag: "This Week\u2019s Focus",
    title: "Liberation Day \u2014 One Year Later",
    intro: "One year ago, sweeping tariffs reshaped global trade. The S&P 500 plunged 12.4%, then surged 9.52% in a single day. The Supreme Court has since ruled the regime unconstitutional \u2014 but the ripple effects on capital flows may be permanent.",
    stats: [
      { value: "\u221212.4%", label: "Initial Drop", color: "#B5342B" },
      { value: "+16.0%", label: "1-Year Return", color: "#3D7A47" },
      { value: "+18.0%", label: "Global (ACWI)", color: "#8B6834" },
      { value: "$166B", label: "Tariffs Collected", color: "#A67B2E" }
    ],
    charts: [
      {
        title: "S&P 500 Recovery Path",
        type: "bar",
        bars: [
          { label: "May \u201925", width: "24%", fillClass: "recovery-fill", text: "\u221212.4%", textColor: "white" },
          { label: "Jun \u201925", width: "17%", fillClass: "recovery-fill", text: "\u22124.2%", textColor: "white" },
          { label: "Sep \u201925", width: "10.5%", fillClass: "recovery-fill", text: "+2.1%" },
          { label: "Dec \u201925", width: "34%", fillClass: "recovery-fill", text: "+8.5%" },
          { label: "Mar \u201926", width: "56%", fillClass: "recovery-fill", text: "+14.0%" },
          { label: "Apr \u201926", width: "64%", fillClass: "recovery-fill", text: "+16.0%" }
        ]
      },
      {
        title: "Original Tariff Rates by Country",
        type: "bar",
        bars: [
          { label: "Vietnam", width: "92%", fillClass: "tariff-fill", text: "46%", textColor: "white" },
          { label: "China", width: "68%", fillClass: "tariff-fill", text: "34%", textColor: "white" },
          { label: "India", width: "52%", fillClass: "tariff-fill", text: "26%", textColor: "white" },
          { label: "Japan", width: "48%", fillClass: "tariff-fill", text: "24%", textColor: "white" },
          { label: "EU", width: "40%", fillClass: "tariff-fill", text: "20%", textColor: "white" }
        ]
      },
      {
        title: "US vs Global Performance",
        type: "comparison",
        bars: [
          { label: "Apr \u201925", usHeight: "24px", globalHeight: "32px", usVal: "\u22128%", globalVal: "\u22124%" },
          { label: "Jul \u201925", usHeight: "18px", globalHeight: "38px", usVal: "\u22124%", globalVal: "+2%" },
          { label: "Oct \u201925", usHeight: "42px", globalHeight: "52px", usVal: "+5%", globalVal: "+8%" },
          { label: "Jan \u201926", usHeight: "56px", globalHeight: "70px", usVal: "+10%", globalVal: "+14%" },
          { label: "Apr \u201926", usHeight: "70px", globalHeight: "90px", usVal: "+14%", globalVal: "+18%" }
        ]
      }
    ],
    legend: [
      { color: "var(--accent)", text: "MSCI USA +14%" },
      { color: "var(--gold)", text: "MSCI ACWI +18%" }
    ],
    sources: [
      { name: "Bloomberg", url: "https://www.bloomberg.com/news/newsletters/2026/03/30/trump-liberation-day-tariff-anniversary" },
      { name: "SCOTUS", url: "https://en.wikipedia.org/wiki/Liberation_Day_tariffs" },
      { name: "US CBP", url: "https://www.cbp.gov" },
      { name: "MSCI", url: "https://www.msci.com" }
    ]
  },

  footer: "Generated April 4, 2026 \u00b7 Data as of market close April 2 \u00b7 Not financial advice"
};
