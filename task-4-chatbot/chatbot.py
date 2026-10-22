import json
import re

# ---------- 1. Load the FAQ data ----------
with open("sample_faq.json", "r") as f:
    data = json.load(f)

greetings = data["greetings"]
faqs = data["faqs"]

# ---------- 2. Clean user input ----------
def clean(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    return text

# ---------- 3. Check for a greeting ----------
def is_greeting(text):
    for g in greetings:
        if re.search(r"\b" + re.escape(g) + r"\b", text):
            return True
    return False

# ---------- 4. Check for an FAQ match ----------
def find_faq(text):
    words = set(text.split())
    best_faq = None
    best_score = 0

    for faq in faqs:
        question_words = set(clean(faq["question"]).split())
        score = len(words & question_words)  # how many words overlap
        if score > best_score:
            best_score = score
            best_faq = faq

    # Need at least 2 words in common to be confident
    if best_score >= 2:
        return best_faq
    return None

# ---------- 5. Main chat loop ----------
print("=" * 50)
print("  💬 Support Chatbot  (type 'exit' to quit)")
print("=" * 50)

greeted = False  # remember if we already said hello

while True:
    user = input("\nYou: ").strip()

    if not user:
        continue

    # Exit commands
    if user.lower() in ["bye", "exit", "quit"]:
        print("Bot: Goodbye! 👋")
        break

    text = clean(user)
    reply_parts = []

    # Check greeting
    if is_greeting(text):
        if not greeted:
            reply_parts.append("Hello! 👋 Welcome. How can I help you?")
            greeted = True
        else:
            reply_parts.append("Hi again!")

    # Check FAQ
    faq = find_faq(text)
    if faq:
        reply_parts.append(faq["answer"])

    # If nothing matched → fallback
    if not reply_parts:
        reply_parts.append("Sorry, I didn't understand that. Try asking about hours, projects, or certificates.")

    print("Bot: " + " ".join(reply_parts))