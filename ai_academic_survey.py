import csv
import statistics
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

RESPONSES_FILE = "survey_responses.csv"
RESULTS_FILE = "survey_results.csv"

DEMOGRAPHIC_QUESTIONS = [
    {"text": "What is your name? (Optional): ", "required": False},
    {"text": "What is your age?: ", "required": True},
    {"text": "What is your gender? (Male/Female/Other): ", "required": True},
    {"text": "What is your year level? (1st, 2nd, 3rd, 4th): ", "required": True, "valid_values": ["1st", "2nd", "3rd", "4th"]}
]

SURVEY_QUESTIONS = {
    "Academic Performance": [
        "AI tools have improved my academic grades.",
        "AI tools help me understand complex topics more easily.",
        "AI tools help me complete assignments faster.",
        "AI tools enhance the quality of my academic work.",
        "AI tools make exam preparation easier.",
        "AI tools assist me in solving difficult problems.",
        "AI tools increase my efficiency in doing academic tasks.",
        "AI tools have contributed positively to my overall academic standing."
    ],
    "Class Engagement": [
        "AI tools help me participate more actively in class discussions.",
        "AI tools give me confidence to answer during recitations.",
        "AI tools improve my contributions during group projects.",
        "AI tools assist me in preparing for class presentations.",
        "AI tools encourage me to ask more questions to my instructors.",
        "AI tools improve my collaboration with classmates.",
        "AI tools help me communicate my ideas better during class activities."
    ],
    "Personal Opinions on AI": [
        "AI tools make learning more enjoyable.",
        "AI tools should be integrated into formal education systems.",
        "The use of AI tools should have clear ethical guidelines.",
        "Over-reliance on AI tools can negatively affect critical thinking skills.",
        "AI tools help develop new skills that are important for the future.",
        "AI tools should be limited during exams and quizzes.",
        "AI tools are essential for modern students' success.",
        "I believe AI tools will continue to shape the future of education."
    ]
}

LIKERT_SCALE = ["1 - Strongly Disagree", "2 - Disagree", "3 - Agree", "4 - Strongly Agree"]

def save_responses(data):
    try:
        file_exists = False
        with open(RESPONSES_FILE, "r") as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(RESPONSES_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            headers = ["Name", "Age", "Gender", "Year Level", "Timestamp"]
            for section, questions in SURVEY_QUESTIONS.items():
                headers.extend([f"{section}: {q}" for q in questions])
            writer.writerow(headers)
        writer.writerow(data)

def validate_input(prompt, valid_values=None, required=True):
    while True:
        response = input(prompt).strip()
        if not response and not required:
            return None
        if valid_values and response not in valid_values:
            print(f"Invalid input. Please choose from {valid_values}.")
        else:
            return response

def normalize_input(response):
    if isinstance(response, str):
        return response.strip().capitalize()
    return response

def conduct_survey():
    print("\nWelcome to the AI Tools and Academic Performance Survey!")
    demographic_data = []
    for question in DEMOGRAPHIC_QUESTIONS:
        if question.get("valid_values"):
            response = validate_input(
                question["text"], valid_values=question["valid_values"], required=question["required"]
            )
        else:
            response = validate_input(question["text"], required=question["required"])
        demographic_data.append(normalize_input(response))

    survey_answers = []
    for section, questions in SURVEY_QUESTIONS.items():
        print(f"\n=== {section} Section ===")
        for question in questions:
            print(f"\n{question}")
            for option in LIKERT_SCALE:
                print(option)
            answer = validate_input("Your answer (1-4): ", ["1", "2", "3", "4"])
            survey_answers.append(int(answer))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_responses(demographic_data + [timestamp] + survey_answers)
    print("\nThank you! Your responses have been recorded.\n")

def show_graphs(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Age"].astype(float), kde=True, color="skyblue")
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 4))
    df["Gender"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90, colors=["#ff9999", "#66b3ff"])
    plt.title("Gender Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 4))
    df["Year Level"].value_counts().plot(kind="bar", color="lightgreen")
    plt.title("Year Level Distribution")
    plt.xlabel("Year Level")
    plt.ylabel("Count")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def analyze_results():
    try:
        df = pd.read_csv(RESPONSES_FILE)
        print(f"\nTotal Participants: {len(df)}")

        df.dropna(how='all', inplace=True)

        section_means = {}
        results = []
        index = 0

        for section, questions in SURVEY_QUESTIONS.items():
            scores = df.iloc[:, 5 + index:5 + index + len(questions)].fillna(0).astype(float).astype(int)
            section_avg = round(scores.mean().mean(), 2)
            section_means[section] = section_avg

            for col in scores.columns:
                question_text = col.split(": ")[-1]
                vals = scores[col]
                results.append([
                    question_text,
                    round(vals.mean(), 2),
                    round(vals.median(), 2),
                    round(vals.mode()[0], 2) if not vals.mode().empty else "No unique mode",
                    int(vals.min()),
                    int(vals.max()),
                    f"{round((vals >= 3).sum() / len(vals) * 100, 2)}%"
                ])
            index += len(questions)

        result_df = pd.DataFrame(results, columns=["Question", "Mean", "Median", "Mode", "Min", "Max", "Agreement"])
        result_df.to_csv(RESULTS_FILE, index=False)

        print("\nSection Averages:")
        for section, avg in section_means.items():
            print(f"{section}: {avg}")

        overall = round(statistics.mean(section_means.values()), 2)
        print(f"\nOverall Mean: {overall}")

        print("\nInterpretation:")
        print("The data shows that AI tools positively influence student performance and engagement.")

        if validate_input("\nWould you like to view graphs about the respondents? (yes/no): ", ["yes", "no"]) == "yes":
            show_graphs(df)

    except FileNotFoundError:
        print("\nNo data found. Please run the survey first.")
    except Exception as e:
        print(f"\nError during analysis: {e}")

def print_credits():
    print("\n--- Researcher Credits ---")
    print("Research Title: The Effectiveness of AI Tools in Improving the Academic Performance of Computer Science Students")
    print("- Joseph Nathaniel Hizon: Full Stack Developer, Data Handler")
    print("- Shane Haidee Duran: Survey Designer, Research Writer")
    print("- Mark Anthony Boac: Debugger, Team Leader")
    print("- Joshua Piga: Data Analyst, Visualizer")

def main():
    while True:
        print("\n--- AI Tools and Academic Performance Survey ---")
        print("1. Conduct a new survey")
        print("2. See the Research Results")
        print("3. View researcher credits")
        print("4. Exit")
        choice = validate_input("Choose an option (1-4): ", ["1", "2", "3", "4"])

        if choice == "1":
            conduct_survey()
        elif choice == "2":
            analyze_results()
        elif choice == "3":
            print_credits()
        elif choice == "4":
            print("\nThank you! Goodbye.")
            break

if __name__ == "__main__":
    main()