import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from environs import Env
from dialog_flow import get_answer_dialogflow, get_answer_for_vk


def get_message(event, vk_api, project_id):
    text = event.text
    chat_id = event.user_id
    answer = get_answer_dialogflow(project_id, text, chat_id)

    if not answer.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer.query_result.fulfillment_text,
            random_id=get_random_id()
        )


def main():
    env = Env()
    env.read_env('.env')
    vk_token = env('VK_TOKEN')
    project_id = env('PROJECT_ID')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            get_message(event, vk_api, project_id)


if __name__ == "__main__":
    main()
