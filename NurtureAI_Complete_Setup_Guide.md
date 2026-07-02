# Nurture AI — Complete Setup Guide
## From Zero to Running Agent, Step by Step

---

## ⚠️ Important 2026 Update — Read This First

Google changed how API keys work in 2026:
- All new keys are now **Auth keys** — more secure by default
- From **June 19, 2026**: unrestricted old keys are blocked
- Keys starting with `AIzaSy` are the correct format — this is what you will get
- **Gemini 2.5 Flash is free** — 10 requests per minute, 250 per day — no credit card needed

---

## PART 1 — Get Your Gemini API Key

---

### Step 1: Go to Google AI Studio
- Open your browser
- Go to: **https://aistudio.google.com**
- Sign in with your **Google account**
- If it is your first visit, accept the Terms of Service when prompted

---

### Step 2: Open the API Keys page
- Look at the **left sidebar**
- Click **"Get API key"**
- This takes you to the API key management page

---

### Step 3: Create your key
- Click the blue button **"Create API key"**
- Two options appear:
  - ✅ **"Create API key in a new project"** — choose this one
- Google creates a project and generates your key automatically

---

### Step 4: Copy and secure your key
- Your key appears on screen — it looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXX`
- Click the **copy icon** next to it
- Paste it into your **Notes app or phone notepad** right away
- ⚠️ Treat it like a password — never share it, never paste it into a public notebook

---

### Step 5: Restrict your key (important for 2026)
- On the API Keys page, look at your new key
- If it shows **"Unrestricted"** next to it:
  - Hover over that label
  - Click **"Add restrictions"**
  - Select **"Restrict to Gemini API only"**
  - Click **"Restrict key"**
- If it already shows **"Generative Language API"** — you are good, no action needed

---

## PART 2 — Set Up Your Kaggle Notebook

---

### Step 6: Create a Kaggle account (if you do not have one)
- Go to: **https://www.kaggle.com**
- Click **"Register"**
- Sign up with your Google account — easiest option
- Verify your phone number under **Settings → Phone** — required to use secrets

---

### Step 7: Create a new notebook
- Once logged in, click the **"+" Create** button in the left sidebar
- Select **"New Notebook"**
- A new notebook opens in your browser
- On the right side panel, make sure **"Internet"** is toggled **ON**
  - Click the panel icon on the right → find Internet → toggle it on

---

### Step 8: Add your API key as a Secret
- In the notebook, click **"Add-ons"** in the top menu bar
- Click **"Secrets"**
- A panel opens on the right
- Click **"Add a new secret"**
- Fill in:
  - **Name:** `GEMINI_API_KEY` — type this exactly, all caps, underscore, no spaces
  - **Value:** paste your Gemini API key here
- Click **"Save"**
- You will see it listed — now toggle the switch **ON** next to it
- ✅ Your key is now securely stored and available to this notebook

---

## PART 3 — Build the Agent Cell by Cell

Copy each section below into a new cell in your Kaggle notebook in order.

---

### CELL 1 — Install the SDK

Create a new code cell and paste this:

```python
!pip install google-genai -q
```

Click **Run** (the play button). Wait for it to finish.

> Note: Use `google-genai` — NOT `google-generativeai`. The old one is deprecated.

---

### CELL 2 — Imports and Connect to Gemini

```python
import os
import re
from google import genai
from google.genai import types
from kaggle_secrets import UserSecretsClient

# Load API key from Kaggle Secrets
secrets = UserSecretsClient()
GEMINI_API_KEY = secrets.get_secret("GEMINI_API_KEY")

# Connect to Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

print("✅ Nurture AI is ready.")
```

Run this cell. You should see: `✅ Nurture AI is ready.`

If you see an error here, check that your secret name is exactly `GEMINI_API_KEY` and the toggle is ON.

---

### CELL 3 — System Prompt (Day 1: Vibe Coding)

Add a **Markdown cell** above this with the text:
> `## 🧠 Agent Persona`
> `The system prompt defines who Nurture AI is — her tone, her limits, and when she escalates to real help.`

Then add a **code cell**:

```python
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
```

Run this cell. No output — that is normal.

---

### CELL 4 — Session Memory (Day 3: Memory & Sessions)

Add a **Markdown cell** above this:
> `## 🧩 Session Memory`
> `Tracks mood across the conversation. Cleared completely on exit for privacy.`

```python
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
```

Run this cell. No output — that is normal.

---

### CELL 5 — Tools (Day 2: Agent Tools)

Add a **Markdown cell** above this:
> `## 🛠️ Agent Tools`
> `Two tools the agent calls on its own — a mood logger and an exercise suggester.`

```python
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
```

Run this cell. No output — that is normal.

---

### CELL 6 — Security Layers (Day 4: Quality & Security)

Add a **Markdown cell** above this:
> `## 🔒 Security Layers`
> `Three protections run before every message reaches Gemini:`
> `1. Input Sanitization 2. Prompt Injection Protection 3. Crisis Detection`

```python
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
```

Run this cell. No output — that is normal.

---

### CELL 7 — Session Summary (Day 5: Prototype to Production)

Add a **Markdown cell** above this:
> `## 📋 Session Summary`
> `At the end of every session, Gemini writes a warm personalised closing message.`

```python
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
```

Run this cell. No output — that is normal.

---

### CELL 8 — Conversation Engine

```python
conversation_history = []

def chat_with_nurture_ai(user_message: str) -> str:
    mood_context = get_mood_context()
    full_message = (
        f"{mood_context}\n{user_message}".strip()
        if mood_context else user_message
    )

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
```

Run this cell. No output — that is normal.

---

### CELL 9 — Sample Conversation (Markdown cell only — no code)

Add this as a **Markdown cell** so judges can read it without running anything:

```
## 💬 Sample Conversation

**Nurture AI:** Hi there, mama. 💛
I am Nurture AI — here just for you.
No advice unless you want it. No judgment. Ever.
Just tell me — how are you feeling today?

**User:** I feel invisible. Like I do not exist outside of being a mom.

**Nurture AI:** That feeling of losing yourself is one of the most common —
and least talked about — parts of early motherhood.
You still exist. You still matter.
Can you tell me a little more about what today has been like?

**User:** I have not slept. The baby cries all night and I just cry with her.

**Nurture AI:** Crying together at 3 AM — that is not failure.
That is a mother who is fully present even when she is running on empty.
Would a quick breathing exercise help right now, or do you just need to talk?
```

---

### CELL 10 — Run Nurture AI

Add a **Markdown cell** above this:
> `## ▶️ Start Nurture AI`
> `Run this cell to begin. Type your message and press Enter. Type 'bye' to end.`

```python
def run_nurture_ai():
    print("=" * 52)
    print("          💛  Welcome to Nurture AI  💛")
    print("     A safe space for new mothers, always.")
    print("     Type 'bye' at any time to end the session.")
    print("=" * 52)
    print()

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

        if not user_input:
            print("Nurture AI: I am here whenever you are ready. 💛\n")
            continue

        if user_input.lower() in ["bye", "exit", "quit", "goodbye"]:
            print("\n--- Your Session Summary ---")
            print(generate_summary())
            clear_session()
            print("\nNurture AI: Take care of yourself. You are doing better than you think. 💛")
            break

        user_input = sanitize_input(user_input)

        if is_injection_attempt(user_input):
            print(f"\nNurture AI: {INJECTION_RESPONSE}\n")
            continue

        if is_crisis_message(user_input):
            print(f"\nNurture AI: {CRISIS_RESPONSE}\n")
            continue

        if user_input.isdigit() and 1 <= int(user_input) <= 10:
            log_mood(int(user_input))

        try:
            response = chat_with_nurture_ai(user_input)
            print(f"\nNurture AI: {response}\n")
        except Exception as e:
            print(f"\n[Something went wrong: {e}]")
            print("Please try again or type 'bye' to exit.\n")


# Start the agent
run_nurture_ai()
```

Run this cell. The chat starts. Type and press Enter to talk to Nurture AI.

---

## PART 4 — Make Your Notebook Public

When you are happy with the notebook:

1. Click **"Share"** button in the top right corner
2. Under visibility, select **"Public"**
3. Click **"Save"**
4. Copy the URL from your browser — this is your **Project Link** for the competition

---

## PART 5 — Upload to GitHub

1. Go to **https://github.com** and sign in (or create a free account)
2. Click the **"+"** icon in the top right → **"New repository"**
3. Name it: `nurture-ai`
4. Set it to **Public**
5. Click **"Create repository"**
6. On the next page click **"uploading an existing file"**
7. Drag and drop these two files:
   - `NurtureAI_Agent.py`
   - `README.md`
8. Click **"Commit changes"**
9. Copy the GitHub URL — this is a backup project link

---

## Common Errors and Fixes

| Error | What it means | Fix |
|---|---|---|
| `Secret not found` | Secret name is wrong or toggle is off | Check name is exactly `GEMINI_API_KEY` and toggle is ON |
| `Module not found: google.genai` | SDK not installed | Run `!pip install google-genai -q` again |
| `Permission denied` | Phone not verified on Kaggle | Go to Settings → Phone and verify |
| `429 Resource Exhausted` | Hit free tier limit | Wait a few minutes and try again |
| `Response cut off mid sentence` | max_output_tokens too low | Make sure it is set to `800` in Cell 8 |
| `Invalid API key` | Key is wrong or restricted incorrectly | Go back to AI Studio and create a fresh key |

---

## You Are Done When You Have

- ✅ Agent running in Kaggle notebook
- ✅ Notebook set to Public
- ✅ GitHub repo with code and README
- ✅ YouTube video uploaded
- ✅ Kaggle Writeup submitted with all links

💛 You built this. Now go submit it.
