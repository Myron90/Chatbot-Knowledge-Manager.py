import json
from difflib import get_close_matches

from typing import List

"""
    Load the knowledge base from a JSON file.
    Args:
        file_path (str): Path to the JSON file containing the knowledge base.
    Returns:
        dict: The knowledge base loaded from the file.
    """
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

"""
    Save the knowledge base to a JSON file.
    Args:
        file_path (str): Path to the JSON file where the knowledge base should be saved.
        data (dict): The knowledge base to be saved.
    """
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

"""
    Find the closest matching question from the list of questions.
    Args:
        user_question (str): The question input by the user.
        questions (List[str]): List of questions to match against.
    Returns:
        str | None: The closest matching question if found, otherwise None.
    """
def find_best_match(user_question: str, questions: List[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

"""
    Retrieve the answer for a given question from the knowledge base.
    Args:
        question (str): The question for which to retrieve the answer.
        knowledge_base (dict): The knowledge base containing questions and answers.
    Returns:
        str | None: The answer to the question if found, otherwise None.
    """
def get_answer_for_questions(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

"""
    Update the answer for a given question in the knowledge base.
    Args:
        question (str): The question for which the answer needs to be updated.
        knowledge_base (dict): The knowledge base containing questions and answers.
    """
def change_answer(question: str, knowledge_base: dict) -> None:
    for qna in knowledge_base["questions"]:
        if qna["question"].lower() == question.lower():
            new_answer = input(f'Enter the new answer for "{question}" (or type "!skip" to keep the existing answer): ')
            if new_answer != "!skip":
                qna["answer"] = new_answer
                print("Answer updated successfully!")
            return

    print("Question not found in the knowledge base.")

"""
    Start the chatbot and handle user interactions.
    - Loads the knowledge base from 'knowledge_base.json'.
    - Engages in a loop where the user can ask questions or modify the knowledge base.
    - Adds new questions and answers to the knowledge base as needed.
    """
def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    exit_commands = {"quit", "exit"}

    while True:
        user_input: str = input('You: ').lower()

        if user_input in exit_commands:
            print("Goodbye")
            break

        if user_input == "change":
            print("Current Knowledge Base:")
            for qna in knowledge_base["questions"]:
                print(f"Question: {qna['question']}")
                print(f"Answer: {qna['answer']}")
                print()
            user_question = input("Enter the question you want to change the answer for: ")
            change_answer(user_question, knowledge_base)
            save_knowledge_base('knowledge_base.json', knowledge_base)

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_questions(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me ?')
            new_answer: str = input('Type the answer or "skip" to skip:')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')


if __name__ == '__main__':
    chat_bot()

#ChatBot Knowledge Base Manager is a Python-based tool designed to manage and enhance the knowledge base of a chatbot.
# It allows users to load, update, and save question-and-answer pairs in a JSON file.
# The chatbot can engage in interactive conversations, recognize and retrieve answers to known questions, and learn new responses dynamically.
# Ideal for developers looking to build and maintain a conversational AI with an easily updatable knowledge repository.