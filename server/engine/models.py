from django.db import models

class Post(models.Model):
	id = models.AutoField(primary_key=True)
	phone = models.CharField(max_length=20)
	post = models.TextField()
	zip_code = models.CharField(max_length=20)
	timestamp = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name


class Reply(models.Model):
	id = models.AutoField(primary_key=True)
	phone = models.CharField(max_length=20)
	reply = models.TextField()
	zip_code = models.CharField(max_length=20)
	post = models.ForeignKey('Post')
	timestamp = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name

class Reply_All(models.Model):
	id = models.AutoField(primary_key=True)
	phone = models.CharField(max_length=20)
	reply = models.TextField()
	zip_code = models.CharField(max_length=20)
	post = models.ForeignKey('Post')
	timestamp = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name


class Follow_Tag(models.Model):
	id = models.AutoField(primary_key=True)
	tag = models.CharField(max_length=20)
	follow_list = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name
