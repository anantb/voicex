from celery.task import task

@task
def print_msg(msg):
	print msg
