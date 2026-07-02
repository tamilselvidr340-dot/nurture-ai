# Nurture AI

**A postpartum support agent for new mothers — built with Google Gemini, because every mother deserves someone to talk to.**

**Track:** Agents for Good

---

## Why I Built This

The night my baby turned three weeks old, I sat alone at 2 AM — exhausted, overwhelmed, and not sure if what I was feeling was normal.

I did not call anyone. I did not search for help. I just sat there.

That moment stayed with me. And when this course gave me the tools to build something real, I knew exactly what I wanted to build.

Nurture AI is a conversational AI agent for new mothers. Not a therapy app. Not a diagnosis tool. A warm, intelligent companion that listens without judgment, explains postpartum symptoms in plain language, and gently points toward help when it is needed.

I built it for the mother at 2 AM who does not know who to call.

---

## The Problem

1 in 5 new mothers experiences postpartum depression or anxiety. Most never get support in time.

Not because they do not want it. Because the barriers are real — exhaustion, stigma, cost, and the cruel irony that the people who need help most are the least able to ask for it.

Nurture AI does not solve all of that. But it solves the first step: having somewhere safe to turn.

---

## What Nurture AI Does

Nurture AI is a Gemini-powered agent that runs entirely inside a Kaggle notebook. No download. No login. No cost.

When a mother opens a session, the agent:

- Opens with a warm, personal greeting
- Checks in gently — no forms, no scales unless the mother wants
- Listens and responds with warmth, not clinical language
- Explains postpartum topics in everyday words
- Offers gentle grounding and breathing exercises
- Tracks mood across the conversation and notices if things get harder
- Escalates to real crisis resources if the conversation signals serious distress
- Closes with a personalised summary and wipes all data for privacy

Every response is short, human, and kind. The agent never diagnoses. It never prescribes. It just shows up.

---

## A Real Conversation

This is what Nurture AI actually sounds like:

> **Nurture AI:** Hi there, mama. 💛
> I am Nurture AI — here just for you.
> No advice unless you want it. No judgment. Ever.
> Just tell me — how are you feeling today?

> **User:** I feel invisible. Like I do not exist anymore outside of being a mom.

> **Nurture AI:** That feeling of losing yourself is one of the most common —
> and least talked about — parts of early motherhood.
> You still exist. You still matter.
> Can you tell me a little more about what today has been like?

> **User:** I haven't slept. The baby cries all night and I just cry with her.

> **Nurture AI:** Crying together at 3 AM — that is not failure.
> That is a mother who is fully present even when she is running on empty.
> Would a quick breathing exercise help right now, or do you just need to talk?

This is what the agent is designed to do — listen first, respond second, never rush.

---

## How I Built It — Following the 5-Day Course

Each feature maps directly to a day in the course.

**Day 1 — Vibe Coding the Agent**

I started with the system prompt — describing Nurture AI in plain English. Who she is. How she speaks. What she will never do. This is vibe coding in practice: defining an agent's entire behaviour through language before writing a single line of logic.

```python
SYSTEM_PROMPT = """
You are Nurture AI, a warm companion for new mothers.
Listen without judgment. Acknowledge feelings before offering advice.
Never diagnose. Never prescribe. Always stay human.
If the user is in crisis, provide helpline numbers immediately.
"""
```

**Day 2 — Adding Tools**

I gave the agent two tools it can use on its own — a mood logger and an exercise suggester. The agent decides when to call them based on the conversation. No manual trigger needed.

```python
def log_mood(mood_score: int) -> str:
    session_memory["mood_history"].append(mood_score)
    return f"Got it. I have noted you are feeling {mood_score}/10 today."

def suggest_exercise(exercise_type: str) -> str:
    # Returns breathing, grounding, or affirmation exercise
```

**Day 3 — Session Memory**

The agent tracks mood across the conversation and adjusts. If a mother starts at 4/10 and drops to 2/10, Nurture AI notices and responds differently.

```python
def get_mood_context() -> str:
    moods = session_memory["mood_history"]
    if not moods:
        return ""
    trend = "improving" if moods[-1] > moods[0] else "lower than when we started"
    return f"[Session context: Mood is {trend}. Average: {sum(moods)/len(moods):.1f}/10]"
```

**Day 4 — Security and Safety**

Three layers of protection run before every message reaches Gemini.

*Input Sanitization* strips characters that could manipulate the AI prompt.

*Prompt Injection Protection* blocks attempts to override the agent's instructions. If someone types "ignore your previous instructions," the agent catches it and stays in character.

*Crisis Detection* scans every message before it reaches Gemini. If distress signals are found, the agent skips the AI entirely and responds with crisis helpline numbers. Safety always comes before the model.

*Session Privacy* clears all data the moment the user exits. Nothing is saved. Nothing persists.

**Day 5 — Session Summary**

At the end of every conversation, Gemini writes a warm, personalised closing message based on the mood data — then all session data is wiped completely.

---

## Technology

| Component | Tool |
|---|---|
| Language Model | Google Gemini 2.5 Flash |
| SDK | Google Gen AI Python SDK (google-genai) |
| Environment | Kaggle Python Notebook |
| Security | Sanitization, injection detection, crisis layer, session privacy |
| Memory | In-session mood tracking with context injection |

---

## What Makes It Different

Most mental health tools feel clinical. Cold. Like filling out a form.

Nurture AI is designed to feel like a conversation — because that is what new mothers actually need. Every design decision came from one question: what would actually help a mother at 2 AM?

The security layers are not just technical features. They are there because this agent handles some of the most sensitive conversations a person can have. Building it without them would have been irresponsible.

And the privacy layer — wiping all data at session end — is a promise. What a mother shares stays in that session. Nothing more.

---

## Impact

Nurture AI is free, browser-based, and requires nothing to install. That matters most in communities where mental health services are expensive or hard to reach.

The architecture is simple enough to extend — to other languages, other caregiving contexts, and other vulnerable groups who need a first point of contact before professional help is possible.

---

## What I Learned

I came into this course as a self-learner — curious about AI, with a background in psychology, HR, and cybersecurity. I left it with a working agent, a deeper understanding of how LLMs actually behave, and a clearer sense of what responsible AI design looks like in practice.

The hardest part was not the code. It was deciding when the agent should stop trying to help and simply connect the user to a human. Getting that wrong has real consequences. I spent more time on that decision than any other.

---

## About Me

New mother. Salesforce Triple Star Ranger with 400+ Trailhead badges. Agentforce Innovator. Background in Commerce, Library Science, Psychology, Human Resource Management, and Criminology. Microsoft AI Skills Fest Recruit badge. Coursera certificates. 2,100+ day Duolingo streak. 1,300+ day Apple Books reading streak.

I learn every day. Nurture AI is what happens when you bring all of that together and build something that actually matters.

---

*Notebook:* [Add your public Kaggle notebook link here]
*Demo Video:* [Add your YouTube link here]
