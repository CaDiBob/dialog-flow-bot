import os
import logging

from environs import Env


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger('bot')



def main():
    env = Env()
    env.read_env('.env')
    tg_token = env('TG_TOKEN')
    print(tg_token)


if __name__ == '__main__':
    main()
