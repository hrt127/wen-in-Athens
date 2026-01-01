"""chorus.py - Absurd philosopher commentary engine for the Temple of Greeks"""
import random

PHILOSOPHERS = [
    "Diogenes, naked in the marketplace",
    "Socrates, slightly drunk on hemlock wine",
    "Heraclitus, hoarding volatility like firewood",
    "Plato, long gamma in the cave of shadows",
    "Aristotle, overfitting reality with his syllogisms",
    "Pythagoras, counting beans instead of delta",
    "Epicurus, hedging his pleasures",
    "Zeno, forever approaching the strike price",
]

BULLISH_LINES = [
    "The polis chants 'number go up', yet you write calls. Truly, you hate the gods.",
    "Only a coward hedges when Zeus himself is levering beta.",
    "To buy puts when Apollo rides his chariot upward is to spit in Dionysus's wine.",
    "Even the Oracle of Delphi whispers: 'Moon soon, fool.'",
    "The bulls sacrifice at altars of leverage. You bring them... a hedge? Pathetic.",
    "Momentum flows like the wine at symposia, yet you stand sober with your iron condor.",
]

BEARISH_LINES = [
    "To be short vol in a storm is to build temples on quicksand.",
    "Even Sisyphus would not roll this trade uphill.",
    "The bears gather in shadows, sharpening their claws. Your calls will feed them.",
    "When Hades himself opens the gates, only puts will save your mortal soul.",
    "The IV spike comes like a thief in the night. Your naked position trembles.",
    "To sell puts into the abyss is to wrestle with Cerberus—and lose.",
]

NEUTRAL_LINES = [
    "Delta at zero, meaning at zero; perfection achieved through paralysis.",
    "In Athens, only fools are certain. You, at least, are delta-neutral.",
    "The iron condor soars neither high nor low—like your aspirations.",
    "To profit from decay is to embrace the void. Theta gang salutes you, reluctantly.",
    "Neither bull nor bear, you are the sacred goat of mediocrity.",
    "Range-bound markets reward the patient. Or bore them to death. Same outcome.",
]

HEDGE_LINES = [
    "Hedge if you must, but remember: no one erects statues for risk managers.",
    "You sacrifice premium as if it were goats; the gods remain unimpressed.",
    "Every hedge is a prayer to cowardice. The symposium mocks you.",
    "To hedge is to admit mortality. The immortals laugh at your spreads.",
    "Protection costs drachmas. Glory costs everything. Choose wisely.",
    "Your collar is tighter than a philosopher's rope belt. Breathe, mortal.",
]

VOL_CRUSH_LINES = [
    "The IV collapses like a failed democracy. Your long options weep.",
    "Vega, once mighty, now whimpers like a beaten dog in the agora.",
    "Post-earnings, the vol gods take back their gifts. You are left holding air.",
]

VOL_SPIKE_LINES = [
    "The volatility explosion arrives! Even the statues tremble!",
    "IV surges like the ocean during Poseidon's tantrum. Ride it or drown.",
    "Fear spreads through the marketplace. Vol sellers flee to their caves.",
]

def absurd_comment(score: float, strategy: str, view: str, iv: float = 0.6) -> str:
    """Generate an absurd philosopher comment based on trade context.
    
    Args:
        score: Decision quality score (0-1)
        strategy: Trading strategy name
        view: User's market view (bullish/bearish/neutral/hedge)
        iv: Implied volatility level (0-2)
    
    Returns:
        Formatted markdown string with philosopher commentary
    """
    speaker = random.choice(PHILOSOPHERS)
    
    # Select base pool based on view
    if view == "bullish":
        pool = BULLISH_LINES
    elif view == "bearish":
        pool = BEARISH_LINES
    elif view == "hedge":
        pool = HEDGE_LINES
    else:
        pool = NEUTRAL_LINES
    
    base = random.choice(pool)
    
    # Add vol-based commentary occasionally
    if random.random() > 0.7:
        if iv > 0.8:
            base += " " + random.choice(VOL_SPIKE_LINES)
        elif iv < 0.3:
            base += " " + random.choice(VOL_CRUSH_LINES)
    
    # Add score-based twist
    if score > 0.75:
        twist = " The symposium roars approval; even the statues nod."
    elif score < 0.35:
        twist = " The agora falls silent. Someone coughs. A goat laughs."
    else:
        twist = " The oracle shrugs; fate is bored but intrigued."
    
    return f"*{speaker} whispers:* \"{base}{twist}\""

def market_mood_text(iv: float, sentiment: str) -> str:
    """Generate atmospheric text based on market conditions.
    
    Args:
        iv: Implied volatility level
        sentiment: Market sentiment (bullish/bearish/neutral)
    
    Returns:
        Atmospheric text describing the temple's mood
    """
    mood_texts = []
    
    # IV-based atmosphere
    if iv > 0.8:
        mood_texts.append("The temple vibrates with wild IV; even the statues are jittery.")
    elif iv > 0.6:
        mood_texts.append("Moderate chaos reigns. The priests of vol collect their tithes.")
    elif iv < 0.3:
        mood_texts.append("The air is still. The options priests yawn; vol is asleep.")
    else:
        mood_texts.append("Calm pervades the marketplace. Perhaps too calm.")
    
    # Sentiment-based chants
    if sentiment == 'bullish':
        mood_texts.append("The chorus chants: 'Bulls to Olympus, bears to Tartarus!'")
    elif sentiment == 'bearish':
        mood_texts.append("Rumors in the agora: a crash banquet is being prepared.")
    else:
        mood_texts.append("The crowd mills about, uncertain, waiting for omens.")
    
    return " ".join(mood_texts)

def cult_rank(score: int) -> str:
    """Determine cult rank based on cumulative score.
    
    Args:
        score: Cumulative favor score
    
    Returns:
        Rank title string
    """
    if score < 0:
        return "Exiled Bean Farmer"
    elif score < 20:
        return "Initiate of Implied Vol"
    elif score < 50:
        return "Keeper of Gamma Goblets"
    elif score < 100:
        return "Priest of Perpetual Theta"
    elif score < 200:
        return "Archon of the Straddle"
    elif score < 350:
        return "Vega Whisperer of the Sacred Spreads"
    else:
        return "Supreme Hedger of the Orgy"

def streak_reward(streak: int) -> str:
    """Generate reward message for streaks.
    
    Args:
        streak: Current win streak
    
    Returns:
        Reward message or empty string
    """
    if streak == 3:
        return "🎉 Rite complete: Your streak of 3 has granted you a seat at the symposium!"
    elif streak == 5:
        return "🔥 The gods notice! 5 rites in succession! You are offered diluted wine!"
    elif streak == 10:
        return "⚡ LEGENDARY! 10 consecutive rites! The Oracle herself invites you to the inner temple!"
    elif streak == 20:
        return "🏛️ MYTHICAL! 20 rites! Your name is carved into the marble! (In very small letters.)"
    return ""
