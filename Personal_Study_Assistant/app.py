import datetime
import json
from typing import List, Dict

# Scheduler agent
def schedular_agent(topics: List[str], deadline: str) -> List[Dict]:
    try:
        deadline_date = datetime.datetime.strptime(deadline, "%d-%m-%Y").date()
    except ValueError:
        raise ValueError("Invalid date format. Please use DD-MM-YYYY format.")

    today = datetime.date.today()
    days_remaining = (deadline_date - today).days
    if days_remaining <= 0:
        raise ValueError("Deadline must be a future date.")

    study_days = max(1, days_remaining // len(topics))
    study_plan = []
    current_day = today

    for topic in topics:
        end_day = current_day + datetime.timedelta(days=study_days - 1)
        study_plan.append({
            "topic": topic,
            "start_date": str(current_day),
            "end_date": str(end_day)
        })
        current_day = end_day + datetime.timedelta(days=1)

    return study_plan

# Research agent
def research_agent(topic: str) -> List[str]:
    return [
        f"What is {topic}? - https://www.wikipedia.org/wiki/{topic.replace(' ', '_')}",
        f"YouTube intro to {topic} - https://www.youtube.com/results?search_query=introduction+to+{topic.replace(' ', '+')}",
        f"Benefits and Risks of {topic} - https://medium.com/tag/{topic.replace(' ', '-')}",
        f"Research papers on {topic} - https://scholar.google.com/scholar?q={topic.replace(' ', '+')}"
    ]

# Summarizer agent
def summerizer_agent(snippets: List[str]) -> str:
    return " | ".join(snippets)

# Main assistant runner
def run_study_assistant():
    topics_input = input("Enter your study topics separated by commas: ")
    deadline = input("Enter your study deadline (DD-MM-YYYY): ")
    topics = [t.strip() for t in topics_input.split(",") if t.strip()]

    if not topics:
        print("No valid topics were entered.")
        return

    try:
        study_plan = schedular_agent(topics, deadline)
    except Exception as e:
        print(f"Error: {e}")
        return

    full_output = []

    for item in study_plan:
        topic = item["topic"]
        print(f"\nResearching: {topic}")
        research = research_agent(topic)
        summary = summerizer_agent(research)

        item_output = {
            "topic": topic,
            "start_date": item["start_date"],
            "end_date": item["end_date"],
            "summary": summary
        }
        full_output.append(item_output)
        print(f"Summary for {topic}:\n{summary}")

    with open("study_assistant_output.json", "w") as f:
        json.dump(full_output, f, indent=4)
    print("\nStudy plan and summaries have been saved to 'study_assistant_output.json'.")

if __name__ == "__main__":
    run_study_assistant()
