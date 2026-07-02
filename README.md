# 💛 Nurture AI

> A postpartum support agent for new mothers — built with Google Gemini because every mother deserves someone to talk to.

---

## What is Nurture AI?

Nurture AI is a conversational AI agent that supports new mothers through one of life's most vulnerable transitions.

It listens without judgment, explains postpartum symptoms in plain language, suggests gentle coping exercises, and connects mothers to real help when they need it most.

Built as part of **Kaggle's 5-Day AI Agents Intensive Vibe Coding Course with Google** — submitted under the **Agents for Good** track.

---

## Why I Built This

The night my baby turned three weeks old, I sat alone at 2 AM — exhausted, overwhelmed, and unsure if what I was feeling was normal.

I did not call anyone. I just sat there.

Nurture AI is the resource I wish I had that night.

---

## Features

| Feature | Description |
|---|---|
| 💬 Empathetic conversation | Warm, human responses — never clinical |
| 📊 Mood tracking | Tracks how the user feels across the session |
| 🧘 Exercise tools | Breathing, grounding, and affirmation exercises |
| 🔒 Privacy first | All session data wiped on exit — nothing stored |
| 🛡️ Prompt injection protection | Blocks attempts to hijack the agent |
| ✂️ Input sanitization | Cleans user input before it reaches Gemini |
| 🆘 Crisis detection | Bypasses AI and returns helpline numbers if needed |
| 📋 Session summary | Personalised closing message at end of session |

---

## How It Aligns to the Course

| Course Day | Concept | Nurture AI Feature |
|---|---|---|
| Day 1 | Agents & Vibe Coding | System prompt defining agent persona |
| Day 2 | Tools & Interoperability | Mood logger + exercise suggester |
| Day 3 | Context, Memory & Sessions | Session mood tracking + context injection |
| Day 4 | Quality & Security | Sanitization + injection protection + crisis layer + privacy |
| Day 5 | Prototype to Production | Session summary + clean notebook structure |

---

## Tech Stack

- **Model:** Google Gemini 2.5 Flash
- **SDK:** `google-genai` (Google Gen AI Python SDK — latest)
- **Environment:** Kaggle Python Notebook
- **Language:** Python 3

---

## How to Run

### Step 1 — Get a Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click **Get API Key** → **Create API Key**
3. Copy your key

### Step 2 — Add it to Kaggle Secrets
1. Open your Kaggle notebook
2. Click **Add-ons** in the top menu → **Secrets**
3. Click **Add a new secret**
4. Name: `GEMINI_API_KEY` — Value: paste your key
5. Toggle it **ON** in the notebook

### Step 3 — Install the SDK
Run this in the first cell:
```python
!pip install google-genai -q
```

### Step 4 — Run all cells
Click **Run All** and scroll to the bottom.
The chat starts automatically. Type your message and press Enter.
Type `bye` to end the session.

---

## Sample Conversation

```
Nurture AI: Hi there, mama. 💛
I am Nurture AI — here just for you.
No advice unless you want it. No judgment. Ever.
Just tell me — how are you feeling today?

You: I feel invisible. Like I do not exist outside of being a mom.

Nurture AI: That feeling of losing yourself is one of the most common —
and least talked about — parts of early motherhood.
You still exist. You still matter.
Can you tell me a little more about what today has been like?

You: I have not slept. The baby cries all night and I just cry with her.

Nurture AI: Crying together at 3 AM — that is not failure.
That is a mother who is fully present even when she is running on empty.
Would a quick breathing exercise help right now, or do you just need to talk?
```

---

## Security Design

Nurture AI is built for sensitive conversations. Three layers of security run before every message reaches Gemini:

1. **Input Sanitization** — removes characters that could manipulate the AI prompt
2. **Prompt Injection Protection** — blocks attempts to override agent instructions
3. **Crisis Detection** — skips Gemini entirely and returns crisis helpline numbers

A fourth layer clears all session memory on exit. Nothing is saved. Nothing persists.

---

## Crisis Resources

If you or someone you know needs immediate help:

- 📞 **Postpartum Support International:** 1-800-944-4773
- 📞 **Crisis Text Line:** Text HOME to 741741
- 📞 **Suicide & Crisis Lifeline:** Call or text 988

---

## About the Builder

New mother. Salesforce Triple Star Ranger with 400+ Trailhead badges. Agentforce Innovator. Background in Commerce, Library Science, Psychology, Human Resource Management, and Criminology. Microsoft AI Skills Fest Recruit badge. 2,100+ day Duolingo streak. 1,300+ day Apple Books reading streak.

---

## Disclaimer

Nurture AI is not a medical tool. It does not diagnose, treat, or replace professional mental health care. It is a first point of contact — a compassionate, available companion that points toward real help when it is needed.

---

*Built with 💛 for the Kaggle 5-Day AI Agents Intensive Capstone 2026*
