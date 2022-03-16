import json

from google.cloud import dialogflow
from environs import Env


def create_intent(project_id, display_name, training_phrases_parts, message_text):
    text = dialogflow.Intent.Message.Text(text=message_text)
    message = dialogflow.Intent.Message(text=text)
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def main():
    with open('questions.json', 'r')as file:
        questions = json.loads(file.read())
    env = Env()
    env.read_env('.env')
    project_id = env.str('PROJECT_ID')
    for intent_name, phrases in questions.items():
        training_phrases_parts = phrases['questions']
        message_text = [phrases['answer']]
        create_intent(project_id, intent_name,  training_phrases_parts, message_text,)


if __name__ == '__main__':
    main()
