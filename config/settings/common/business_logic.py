import environ

env = environ.Env()

env.read_env()

OPENAI_MAX_TOKENS = 2000
OPENAI_MODEL = "gpt-3.5-turbo"
