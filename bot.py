import os

from environs import Env





def main():
    env = Env()
    env.read_env('.env')
    tg_token = env('TG_TOKEN')
    print(tg_token)


if __name__ == '__main__':
    main()
