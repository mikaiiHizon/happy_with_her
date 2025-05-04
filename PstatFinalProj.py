import csv
import os
import statistics
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tabulate import tabulate
import numpy as np
from scipy.stats import t

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESPONSES_FILE = os.path.join(BASE_DIR, "SurveyResponses.csv")
RESULTS_FILE = os.path.join(BASE_DIR, "SurveyResults.csv")

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
    """Save survey responses to a CSV file."""
    try:
        file_exists = os.path.isfile(RESPONSES_FILE)
        with open(RESPONSES_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                headers = ["Name", "Age", "Gender", "Year Level", "Timestamp"]
                for section, questions in SURVEY_QUESTIONS.items():
                    headers.extend([f"{section}: {q}" for q in questions])
                writer.writerow(headers)
            writer.writerow(data)
    except Exception as e:
        print(f"Error saving responses: {e}")

def validate_input(prompt, valid_values=None, required=True):
    """Validate user input."""
    while True:
        response = input(prompt).strip()
        if not response and not required:
            return None
        if valid_values and response not in valid_values:
            print(f"Invalid input. Please choose from {valid_values}.")
        else:
            return response

def normalize_input(response):
    """Normalize input (e.g., capitalize strings)."""
    if isinstance(response, str):
        return response.strip().capitalize()
    return response

def conduct_survey():
    """Conduct a new survey."""
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

def confidence_interval(data, confidence=0.95):
    """Calculate the confidence interval for the mean."""
    n = len(data)
    mean = np.mean(data)
    std_err = np.std(data, ddof=1) / np.sqrt(n)
    margin_of_error = t.ppf((1 + confidence) / 2, n - 1) * std_err
    return mean - margin_of_error, mean + margin_of_error

def stratified_analysis(df, stratify_by):
    """Perform stratified analysis based on a demographic column (e.g., Gender or Year Level)."""
    print(f"\n--- Stratified Analysis by {stratify_by} ---")
    groups = df.groupby(stratify_by)
    for group, data in groups:
        print(f"\nGroup: {group}")
        for section, questions in SURVEY_QUESTIONS.items():
            scores = data.iloc[:, 5:5 + len(questions)].astype(float)
            print(f"{section} - Mean: {scores.mean().mean():.2f}, Std Dev: {scores.std().mean():.2f}, Variance: {scores.var().mean():.2f}")

def show_graphs(df):
    """Visualize data with graphs, including a bell curve."""
    # Age Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Age"].astype(float), kde=True, color="skyblue")
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Gender Distribution
    plt.figure(figsize=(6, 4))
    df["Gender"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90, colors=["#ff9999", "#66b3ff"])
    plt.title("Gender Distribution")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

    # Year Level Distribution
    plt.figure(figsize=(6, 4))
    df["Year Level"].value_counts().plot(kind="bar", color="lightgreen")
    plt.title("Year Level Distribution")
    plt.xlabel("Year Level")
    plt.ylabel("Count")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    # Bell Curve for Survey Scores
    plt.figure(figsize=(10, 6))
    survey_scores = df.iloc[:, 5:].astype(float).values.flatten()
    survey_scores = survey_scores[np.isfinite(survey_scores)]
    sns.histplot(survey_scores, kde=True, color="purple", bins=20)
    plt.title("Survey Scores Distribution with Bell Curve")
    plt.xlabel("Scores")
    plt.ylabel("Density")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Box Plot for Survey Sections
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df.iloc[:, 5:], palette="Set3")
    plt.title("Box Plot of Survey Scores")
    plt.xlabel("Survey Questions")
    plt.ylabel("Scores")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def analyze_results():
    """Analyze survey results and display statistics."""
    try:
        df = pd.read_csv(RESPONSES_FILE)
        print(f"\nTotal Participants: {len(df)}")
        df.dropna(how='all', inplace=True)

        section_means = {}
        results = []
        index = 0

        for section, questions in SURVEY_QUESTIONS.items():
            scores = df.iloc[:, 5 + index:5 + index + len(questions)].fillna(0).astype(float)
            section_avg = round(scores.mean().mean(), 2)
            section_std = round(scores.std().mean(), 2)
            section_var = round(scores.var().mean(), 2)
            ci_lower, ci_upper = confidence_interval(scores.values.flatten())
            section_means[section] = {
                "mean": section_avg,
                "std_dev": section_std,
                "variance": section_var,
                "confidence_interval": (round(ci_lower, 2), round(ci_upper, 2))
            }

            for col in scores.columns:
                question_text = col.split(": ")[-1]
                vals = scores[col]
                results.append([
                    question_text,
                    round(vals.mean(), 2),
                    round(vals.median(), 2),
                    round(vals.std(), 2),
                    round(vals.var(), 2),
                    f"{round((vals >= 3).sum() / len(vals) * 100, 2)}%"
                ])
            index += len(questions)

        result_df = pd.DataFrame(results, columns=["Question", "Mean", "Median", "Std Dev", "Variance", "Agreement"])
        print("\n--- Survey Results Table ---")
        print(tabulate(result_df, headers="keys", tablefmt="grid"))
        result_df.to_csv(RESULTS_FILE, index=False)

        print("\nSection Statistics:")
        for section, stats in section_means.items():
            print(f"{section} - Mean: {stats['mean']}, Std Dev: {stats['std_dev']}, Variance: {stats['variance']}, "
                  f"95% CI: {stats['confidence_interval']}")

        overall_mean = round(statistics.mean([stats["mean"] for stats in section_means.values()]), 2)
        print(f"\nOverall Mean: {overall_mean}")

        print("\nConclusion:")
        if overall_mean >= 3:
            print("The overall results indicate strong agreement that AI tools positively impact academic performance and engagement.")
        else:
            print("The overall results show mixed opinions on the effectiveness of AI tools in education.")

        if validate_input("\nWould you like to view graphs about the respondents? (yes/no): ", ["yes", "no"]) == "yes":
            show_graphs(df)

        if validate_input("\nWould you like to perform stratified analysis? (yes/no): ", ["yes", "no"]) == "yes":
            stratify_by = validate_input("Stratify by (Gender/Year Level): ", ["Gender", "Year Level"])
            stratified_analysis(df, stratify_by)

    except FileNotFoundError:
        print("\nNo data found. Please run the survey first.")
    except Exception as e:
        print(f"\nError during analysis: {e}")

def print_credits():
    """Display researcher credits."""
    print("\n--- Researcher Credits ---")
    print("Research Title: The Effectiveness of AI Tools in Improving the Academic Performance of Computer Science Students")
    print("- Joseph Nathaniel Hizon: Full Stack Developer, Data Handler")
    print("- Shane Haidee Duran: Survey Designer, Research Writer")
    print("- Mark Anthony Boac: Debugger, Team Leader")
    print("- Joshua Piga: Data Analyst, Visualizer")

def main():
    """Main program loop."""
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