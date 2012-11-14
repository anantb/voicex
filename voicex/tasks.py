from celery.decorators import task
from transport.voicex import VoiceXTransport
from transport import config
import time

@task(name='voicex.tasks.delayed_sms')
def delayed_sms(phone_num, msg, delay):
	time.sleep(delay)
	v = VoiceXTransport(transport=config.GV, auth= config.GV_VOICEX_AUTH)
	v.sms(phone_num, msg)
