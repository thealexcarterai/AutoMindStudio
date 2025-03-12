import ollama
import json
from datetime import datetime

# Load config
with open("config.json") as f:
    config = json.load(f)

def get_latest_topic():
    """Fetches the latest topic from the scraped topics file."""
    try:
        with open("inputs/topics.txt", "r") as f:
            topics = f.read().splitlines()
        if topics:
            return topics[0]  # Pick the first topic from the list
        else:
            return "Latest AI advancements"  # Fallback topic
    except FileNotFoundError:
        return "Latest AI advancements"  # If file not found, use default topic

def generate_script(topic, duration="auto"):
    current_year = datetime.now().year  # ✅ Uses the current year, not 2026
    prompt = f"""
    Create {duration}-minute video script about: {topic}
    Target year: {current_year}
    Include:
    - 3 key insights
    - 2 controversial angles
    - 1 future prediction
    - 3 fair use clip suggestions (CC-BY licensed)
    Format: Markdown with timestamps
    """

    print("🔍 Sending prompt to AI:\n", prompt)  # DEBUG PRINT

    try:
        response = ollama.chat(model=config['llm_model'], messages=[{"role": "user", "content": prompt}])
        print("⚙️ AI Response:", response)  # DEBUG PRINT
        return response['message']['content']
    except Exception as e:
        print("❌ ERROR:", e)
        return None

if __name__ == "__main__":
    topic = get_latest_topic()  # ✅ Fetches latest topic
    print("🚀 Running Content Generator for topic:", topic)
    script = generate_script(topic, "5")  # Test with a 5-minute video

    if script:
        print("\n📜 Final Script Output:\n", script)
    else:
        print("❌ No script was generated.")

