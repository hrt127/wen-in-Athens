"""tutorial.py - Playful Greeks education for newbies

Teaches options through absurd allegories, flirty innuendos, and 'up/down' games.
Makes learning feel like unlocking levels at an orgy rather than homework.
"""

# Greeks explained like you're slightly drunk at a symposium
GREEKS_GLOSSARY = {
    "delta": {
        "title": "Δ Delta: The Sensitivity Slut",
        "tldr": "How much your option moves when price goes UP or DOWN",
        "spicy": "Delta is how *exposed* your position is. Call delta = 0.7? Price up $1 → you're up $0.70. Like a good friend who shows up 70% of the time.",
        "game": "🎲 UP or DOWN? If BTC goes UP $1000, your 0.5 delta call gains $500. Simple.",
        "analogy": "Calls = betting price goes UP (delta ~0.5-1.0)\nPuts = betting price goes DOWN (delta ~-0.5 to -1.0)\nDelta = 0? You're NAKED—no directional bias.",
    },
    "gamma": {
        "title": "Γ Gamma: The Acceleration Queen",
        "tldr": "How fast delta changes. Delta's delta.",
        "spicy": "High gamma = your delta CHANGES FAST. Like going from flirty to FULLY NAKED in 3 drinks. Long gamma? You profit from big moves. Short gamma? You're the house—slow and steady.",
        "game": "🌋 Volatility play: High gamma ATM (at-the-money) = maximum action. Price moves? Your delta EXPLODES.",
        "analogy": "Long gamma = you WANT chaos (long straddles)\nShort gamma = you SELL chaos for premium (iron condors)",
    },
    "vega": {
        "title": "V Vega: The IV Dominatrix",
        "tldr": "Sensitivity to IMPLIED volatility (IV). The fear/greed gauge.",
        "spicy": "Long vega = you profit when markets get SPICY (IV up). Short vega = you collect rent when everyone calms down. Think: long vega before elections, short vega after.",
        "game": "📈 IV game: IV jumps from 60% → 80%? Your long vega position gets THICC.",
        "analogy": "High IV = expensive options (everyone's scared)\nLow IV = cheap options (market's bored)\nLong vega = betting on chaos\nShort vega = betting on calm",
    },
    "theta": {
        "title": "Θ Theta: Time's Ruthless Pimp",
        "tldr": "How much your option BLEEDS each day. Time decay.",
        "spicy": "Theta GANG: sell options, collect premium, watch them die slowly. Long theta = you're the landlord. Short theta = you're paying rent daily. Theta accelerates near expiry—that's when the REAL pain begins.",
        "game": "⏰ The countdown: 30 days to expiry? Theta = -$20/day. 3 days left? Theta = -$80/day. RIP.",
        "analogy": "Short options = theta GANG (collect decay)\nLong options = pay theta (you bleed)",
    },
}

# Tutorial challenges - gamified learning
TUTORIAL_CHALLENGES = [
    {
        "id": "delta_basics",
        "title": "🎲 Challenge 1: UP or DOWN?",
        "description": "You buy a CALL with delta = 0.6. BTC is at $90k. It goes UP to $91k. What happens?",
        "options": [
            {"text": "I make $600", "correct": True, "feedback": "YES! Delta 0.6 × $1000 move = $600 profit. You're learning!"},
            {"text": "I lose money", "correct": False, "feedback": "Nope! Calls profit when price goes UP. Delta tells you HOW MUCH."},
            {"text": "Nothing happens", "correct": False, "feedback": "Delta exists! When price moves, delta moves your PnL."},
        ],
        "reward": "Unlocked: Delta Awareness. You can now see through Plato's cave.",
    },
    {
        "id": "put_basics",
        "title": "🔻 Challenge 2: Covered or NAKED?",
        "description": "You buy a PUT (delta = -0.5). Price goes DOWN $1000. What happens?",
        "options": [
            {"text": "I make $500", "correct": True, "feedback": "CORRECT! Negative delta profits when price DROPS. You're getting the hang of this orgy."},
            {"text": "I lose $500", "correct": False, "feedback": "Backwards! Puts have NEGATIVE delta—they profit on DOWN moves."},
            {"text": "I make $1000", "correct": False, "feedback": "Close! But delta is 0.5, not 1.0. Half exposure = half profit."},
        ],
        "reward": "Unlocked: Directional Bias. The symposium nods approvingly.",
    },
    {
        "id": "theta_decay",
        "title": "⏰ Challenge 3: Time's a Bitch",
        "description": "You hold an option with theta = -$50/day. 10 days pass. Nothing else changes. What's your PnL?",
        "options": [
            {"text": "-$500 (I bleed)", "correct": True, "feedback": "YEP. Theta decay is relentless. This is why theta gang exists."},
            {"text": "+$500 (I profit)", "correct": False, "feedback": "You're LONG the option = you PAY theta. Short sellers collect it."},
            {"text": "$0 (no impact)", "correct": False, "feedback": "Theta never sleeps. Every day, your option loses value."},
        ],
        "reward": "Unlocked: Theta Awareness. You now fear time decay like a mortal should."},
    {
        "id": "vega_chaos",
        "title": "🌋 Challenge 4: When Markets Get SPICY",
        "description": "You're long vega (long a straddle). IV spikes from 60% to 100%. What happens?",
        "options": [
            {"text": "I profit BIG", "correct": True, "feedback": "HELL YES. Long vega = you profit when fear/greed explodes. This is the way."},
            {"text": "I lose money", "correct": False, "feedback": "You're long vega! IV going up = your positions get MORE valuable."},
            {"text": "Nothing changes", "correct": False, "feedback": "Vega is POWERFUL. IV changes move option prices significantly."},
        ],
        "reward": "Unlocked: Volatility Intuition. The Oracle whispers secrets to you.",
    },
]

# Beginner-friendly tooltips
TOOLTIPS = {
    "underlying": "The actual price of BTC (or whatever you're trading). Like... the person you're flirting with.",
    "strike": "The price where your option 'activates'. Call @ 90k strike? You want price ABOVE 90k. Put @ 90k? You want price BELOW 90k.",
    "expiry": "When your option DIES. After this, it's worthless. Like Cinderella at midnight.",
    "volatility": "How WILD the market is. High vol = big swings. Low vol = boring. Volatility is basically market horniness.",
    "call": "Betting price goes UP. Bulls use these. Delta is positive (0 to 1).",
    "put": "Betting price goes DOWN. Bears use these. Delta is negative (-1 to 0).",
    "straddle": "Buy a call AND a put (same strike). You profit if price MOVES BIGLY in EITHER direction. You're betting on chaos.",
    "strangle": "Like a straddle but strikes are DIFFERENT (cheaper). Still betting on big moves.",
    "iron_condor": "Selling options on BOTH sides. You profit if price STAYS in range. Theta gang's favorite.",
    "covered_call": "You own BTC, sell a call. Collect premium, but cap your upside. Conservative play.",
    "protective_put": "You own BTC, buy a put. Insurance against crash. Costs premium but protects downside.",
}

def get_tutorial_step(step_id: str):
    """Get a specific tutorial challenge by ID."""
    for challenge in TUTORIAL_CHALLENGES:
        if challenge['id'] == step_id:
            return challenge
    return None

def get_greek_explanation(greek_name: str) -> dict:
    """Get detailed explanation for a specific Greek."""
    return GREEKS_GLOSSARY.get(greek_name.lower(), {})

def get_tooltip(term: str) -> str:
    """Get beginner-friendly tooltip for a term."""
    return TOOLTIPS.get(term.lower(), "No explanation available. Ask Socrates, he might know.")

def generate_welcome_message() -> str:
    """Generate welcome message for first-time users."""
    return """🏛️ **Welcome to the Temple of Greeks, Initiate!**

You've entered an ancient cult where options traders worship at the altar of **Delta**, sacrifice goats to **Theta**, and engage in **Vega**-fueled orgies.

**Don't know what any of that means?** Perfect. You're about to learn through:
- 🎲 UP/DOWN games
- 🔥 Absurd philosopher commentary  
- 💎 Actual profit/loss simulation

**The Rules:**
1. Try trades, get judged by drunk philosophers
2. Earn **favor** for good decisions
3. Climb cult ranks (goal: Supreme Hedger of the Orgy)
4. Share your wins/losses to Farcaster

**Start simple:** Pick a strategy → Adjust parameters → Hit "Analyze Trade"

The philosophers will roast you accordingly. 😏
"""

def get_strategy_explainer(strategy: str) -> str:
    """Get flirty, beginner-friendly strategy explanation."""
    explainers = {
        "call": "📞 **CALL = Price goes UP** \nYou're bullish. If BTC moons, you profit. If it crashes? You lose your premium. Simple.",
        "put": "📉 **PUT = Price goes DOWN** \nYou're bearish. If BTC dumps, you profit. If it pumps? You lose your premium.",
        "straddle": "🎢 **STRADDLE = CHAOS TRADE** \nBuy call + put (same strike). You profit if price MOVES BIGLY in EITHER direction. You're literally betting 'something wild happens'.",
        "strangle": "🤹 **STRANGLE = Cheaper Chaos** \nLike straddle but strikes are different. Cheaper entry, need bigger move to profit.",
        "iron_condor": "🦅 **IRON CONDOR = Range Prison** \nSell options above & below current price. You profit if price STAYS in range. Theta gang's bread & butter.",
        "covered_call": "🛡️ **COVERED CALL = Landlord Mode** \nYou own BTC, sell a call against it. Collect rent (premium), but cap your upside if price moons.",
        "protective_put": "🚨 **PROTECTIVE PUT = Insurance** \nYou own BTC, buy a put. If BTC crashes, the put saves you. Costs premium but you sleep well.",
    }
    return explainers.get(strategy, "Strategy not found. Try asking Diogenes, he might mock you into understanding.")
