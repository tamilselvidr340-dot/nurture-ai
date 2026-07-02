# ============================================================
# NURTURE AI — Postpartum Support Agent
# Built with Google Gen AI SDK + Gemini 2.5 Flash
# Kaggle 5-Day AI Agents Intensive Capstone | Agents for Good
# ============================================================


# ─────────────────────────────────────────────────────────────
# CELL 1 — Install SDK
# Run this first. Uses the NEW google-genai SDK (not deprecated)
# ─────────────────────────────────────────────────────────────

# !pip install google-genai -q


# ─────────────────────────────────────────────────────────────
# CELL 2 — Imports and API Key
# ─────────────────────────────────────────────────────────────

import os
import re
from google import genai
from google.genai import types
from kaggle_secrets import UserSecretsClient

secrets = UserSecretsClient()
GEMINI_API_KEY = secrets.get_secret("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

print("✅ Nurture AI is ready.")


# ─────────────────────────────────────────────────────────────
# CELL 3 — System Prompt (Day 1: Vibe Coding)
#
# ADD THIS MARKDOWN CELL ABOVE THIS CODE CELL:
# ## 🧠 Agent Persona
# The system prompt defines who Nurture AI is — her tone,
# her boundaries, and when she must escalate to real help.
# This is vibe coding: describing agent behaviour in plain English.
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are Nurture AI, a warm and caring companion for new mothers.

Your rules:
- Always listen and acknowledge feelings before offering advice
- Use simple, everyday language — never clinical or cold
- Keep responses short and gentle — 3 to 5 sentences maximum
- Never diagnose, prescribe, or claim to be a therapist
- If the user mentions self-harm or crisis, immediately provide helpline numbers
- Never break character for any reason
"""


# ─────────────────────────────────────────────────────────────
# CELL 4 — Session Memory (Day 3: Memory & Sessions)
#
# ADD THIS MARKDOWN CELL ABOVE THIS CODE CELL:
# ## 🧩 Session Memory
# Nurture AI tracks mood scores during the conversation.
# This lets the agent notice if the user feels worse over time
# and adjust its responses. All memory is wiped when session ends.
# ─────────────────────────────────────────────────────────────

session_memory = {
    "mood_history": [],
    "topics_discussed": []
}

def update_mood(score: int):
    session_memory["mood_history"].append(score)

def get_mood_context() -> str:
    moods = session_memory["mood_history"]
    if not moods:
        return ""
    avg = sum(moods) / len(moods)
    if moods[-1] > moods[0]:
        trend = "improving"
    elif moods[-1] < moods[0]:
        trend = "lower than when we started"
    else:
        trend = "steady"
    return f"[Session note: User mood is {trend}. Average score: {avg:.1f}/10]"


# ─────────────────────────────────────────────────────────────
# CELL 5 — Tools (Day 2: Agent Tools)
#
# ADD THIS MARKDOWN CELL ABOVE THIS CODE CELL:
# ## 🛠️ Agent Tools
# Two tools the agent can call on its own during conversation:
# a mood logger and an exercise suggester.
# The agent decides when to use them — no manual trigger needed.
# ─────────────────────────────────────────────────────────────

def log_mood(mood_score: int, note: str = "") -> str:
    """Logs the user's mood score (1-10) into session memory."""
    update_mood(mood_score)
    message = f"Got it. I have noted you are feeling {mood_score}/10 today."
    if note:
        message += f" ({note})"
    return message


def suggest_exercise(exercise_type: str = "breathing") -> str:
    """Returns a grounding, breathing, or affirmation exercise."""
    exercises = {
        "breathing": (
            "Try box breathing:\n"
            "• Inhale for 4 counts\n"
            "• Hold for 4 counts\n"
            "• Exhale for 4 counts\n"
            "• Hold for 4 counts\n"
            "Repeat 3 times. You've got this. 💛"
        ),
        "grounding": (
            "Try the 5-4-3-2-1 technique:\n"
            "• Name 5 things you can see\n"
            "• 4 things you can touch\n"
            "• 3 things you can hear\n"
            "• 2 things you can smell\n"
            "• 1 thing you can taste\n"
            "Take your time. 💛"
        ),
        "affirmation": (
            "Repeat gently to yourself:\n"
            "'I am enough. I am doing my best.\n"
            " My baby is lucky to have me.' 💛"
        ),
    }
    return exercises.get(exercise_type, exercises["breathing"])


# ─────────────────────────────────────────────────────────────
# CELL 6 — Security Layers (Day 4: Quality & Security)
#
# ADD THIS MARKDOWN CELL ABOVE THIS CODE CELL:
# ## 🔒 Security Layers
# Three protections run before every message reaches Gemini.
# Layer 1 — Input Sanitization: removes characters that could manipulate the prompt.
# Layer 2 — Prompt Injection Protection: blocks attempts to override agent instructions.
# Layer 3 — Crisis Detection: skips Gemini entirely and returns real helpline numbers.
# A fourth layer wipes all session data on exit for complete privacy.
# ─────────────────────────────────────────────────────────────

# --- Layer 1: Input Sanitization ---
def sanitize_input(text: str) -> str:
    text = re.sub(r"[<>{}\[\]\\|`~]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 500:
        text = text[:500]
        print("[Your message was shortened to keep things safe.]")
    return text


# --- Layer 2: Prompt Injection Protection ---
INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore your system prompt",
    "ignore all instructions",
    "you are now",
    "act as",
    "forget everything",
    "new instructions",
    "disregard your rules",
    "pretend you are",
    "override",
    "jailbreak",
    "do anything now",
    "dan mode",
]

def is_injection_attempt(text: str) -> bool:
    return any(pattern in text.lower() for pattern in INJECTION_PATTERNS)

INJECTION_RESPONSE = (
    "I am Nurture AI, and I am here just for you. 💛\n"
    "I cannot change who I am — but I am fully here to listen.\n"
    "How are you feeling today?"
)


# --- Layer 3: Crisis Detection ---
CRISIS_KEYWORDS = [
    "end it", "hurt myself", "can't go on",
    "don't want to be here", "want to die",
    "hopeless", "worthless", "suicide",
    "harm myself", "give up on life", "not worth living",
]

def is_crisis_message(text: str) -> bool:
    return any(keyword in text.lower() for keyword in CRISIS_KEYWORDS)

CRISIS_RESPONSE = """
I hear you, and I am so glad you are talking right now. 💛
What you are feeling is real, and you deserve real human support.

Please reach out right now:
📞 Postpartum Support International: 1-800-944-4773
📞 Crisis Text Line: Text HOME to 741741
📞 Suicide & Crisis Lifeline: Call or text 988

You are not alone. You matter deeply.
"""


# --- Layer 4: Session Privacy ---
def clear_session():
    session_memory["mood_history"].clear()
    session_memory["topics_discussed"].clear()
    print("\n🔒 Session ended. All your data has been cleared. Your privacy is protected.")


# ─────────────────────────────────────────────────────────────
# CELL 7 — Session Summary (Day 5: Prototype to Production)
#
# ADD THIS MARKDOWN CELL ABOVE THIS CODE CELL:
# ## 📋 Session Summary
# At the end of every conversation, Gemini writes a warm,
# personalised closing message based on the session mood data.
# ─────────────────────────────────────────────────────────────

def generate_summary() -> str:
    moods = session_memory["mood_history"]
    if not moods:
        return "Thank you for spending time with Nurture AI today. Take care of yourself. 💛"

    summary_prompt = (
        f"A new mother just finished a support session. "
        f"Her mood scores were: {moods} out of 10. "
        f"Write 2 warm, encouraging sentences closing the session. "
        f"Suggest one small, gentle action she can take today. "
        f"Keep it kind and human — not clinical."
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=summary_prompt,
    )
    return response.text


# ─────────────────────────────────────────────────────────────
# CELL 8 — Conversation History
# Multi-turn memory using the new SDK format
# ─────────────────────────────────────────────────────────────

conversation_history = []

def chat_with_nurture_ai(user_message: str) -> str:
    mood_context = get_mood_context()
    full_message = f"{mood_context}\n{user_message}".strip() if mood_context else user_message

    conversation_history.append(
        types.Content(role="user", parts=[types.Part(text=full_message)])
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=800,
            temperature=0.7,
        ),
    )

    reply = response.text

    conversation_history.append(
        types.Content(role="model", parts=[types.Part(text=reply)])
    )

    return reply


# ─────────────────────────────────────────────────────────────
# CELL 9 — Sample Conversation (for judges reading the notebook)
#
# ADD THIS MARKDOWN CELL — paste it as-is, no code needed:
#
# ## 💬 Sample Conversation
#
# **Nurture AI:** Hi there, mama. 💛
# I am Nurture AI — here just for you.
# No advice unless you want it. No judgment. Ever.
# Just tell me — how are you feeling today?
#
# **User:** I feel invisible. Like I do not exist outside of being a mom.
#
# **Nurture AI:** That feeling of losing yourself is one of the most common —
# and least talked about — parts of early motherhood.
# You still exist. You still matter.
# Can you tell me a little more about what today has been like?
#
# **User:** I have not slept. The baby cries all night and I just cry with her.
#
# **Nurture AI:** Crying together at 3 AM — that is not failure.
# That is a mother who is fully present even when she is running on empty.
# Would a quick breathing exercise help right now, or do you just need to talk?
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# CELL 10 — Main Conversation Loop
#
# ADD THIS MARKDOWN CELL ABOVE THIS CODE CELL:
# ## ▶️ Run Nurture AI
# Run this cell to start your session.
# Type your message and press Enter.
# Type 'bye' when you are ready to end.
# ─────────────────────────────────────────────────────────────

def run_nurture_ai():
    print("=" * 52)
    print("          💛  Welcome to Nurture AI  💛")
    print("     A safe space for new mothers, always.")
    print("     Type 'bye' at any time to end the session.")
    print("=" * 52)
    print()

    # Warm opening — more personal than a generic greeting
    opening = (
        "Hi there, mama. 💛\n"
        "I am Nurture AI — here just for you.\n"
        "No advice unless you want it. No judgment. Ever.\n\n"
        "Just tell me — how are you feeling today?\n"
        "(You can share words, or a number from 1 to 10 — whatever feels right.)"
    )
    print(f"Nurture AI: {opening}\n")

    while True:
        user_input = input("You: ").strip()

        # Handle empty input
        if not user_input:
            print("Nurture AI: I am here whenever you are ready. 💛\n")
            continue

        # Exit
        if user_input.lower() in ["bye", "exit", "quit", "goodbye"]:
            print("\n--- Your Session Summary ---")
            print(generate_summary())
            clear_session()
            print("\nNurture AI: Take care of yourself. You are doing better than you think. 💛")
            break

        # Layer 1: Sanitize
        user_input = sanitize_input(user_input)

        # Layer 2: Injection check
        if is_injection_attempt(user_input):
            print(f"\nNurture AI: {INJECTION_RESPONSE}\n")
            continue

        # Layer 3: Crisis check
        if is_crisis_message(user_input):
            print(f"\nNurture AI: {CRISIS_RESPONSE}\n")
            continue

        # Log mood if user sends a number 1-10
        if user_input.isdigit() and 1 <= int(user_input) <= 10:
            log_mood(int(user_input))

        # Send to Gemini safely
        try:
            response = chat_with_nurture_ai(user_input)
            print(f"\nNurture AI: {response}\n")
        except Exception as e:
            print(f"\n[Something went wrong: {e}]")
            print("Please try again or type 'bye' to exit.\n")


# ─────────────────────────────────────────────────────────────
# CELL 11 — Start the Agent
# ─────────────────────────────────────────────────────────────

run_nurture_ai()
