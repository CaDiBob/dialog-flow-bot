from google.cloud import dialogflow


def get_answer_dialogflow(project_id, text, chat_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        project_id, session=chat_id,
    )
    text_input = dialogflow.TextInput(text=text, language_code='RU-ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return
    return response.query_result.fulfillment_text