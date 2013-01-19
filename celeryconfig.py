CELERY_IMPORTS=("voicex.tasks",)
CELERY_RESULT_BACKEND = "amqp"
BROKER_URL = "amqp://voicex:voicex@localhost:5672//voicex"
