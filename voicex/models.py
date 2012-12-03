"""
Copyright (c) 2012 Anant Bhardwaj, Trisha Kothari

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from django.db import models

'''
VoiceX Models

@author: Anant Bhardwaj, Trisha Kothari
@date: Oct 8, 2012
'''

class Post(models.Model):
	id = models.AutoField(primary_key=True)
	phone = models.CharField(max_length=20)
	post = models.TextField()
	zip_code = models.CharField(max_length=20)
	reply_to = models.ForeignKey('self', blank=False, null=True, related_name="replies")
	public = models.BooleanField()
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name
	
	class Meta:
		db_table = "posts"
		app_label = 'voicex'


class Following(models.Model):
	id = models.AutoField(primary_key=True)
	phone = models.CharField(max_length=20)
	account = models.ForeignKey('Account')
	timestamp = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "following"
		app_label = 'voicex'
		unique_together = ('phone', 'account',)



class Account(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20, unique=True)
	phone = models.CharField(max_length=20, unique=True)
	password = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "accounts"
		app_label = 'voicex'



class Delegate(models.Model):
	id = models.AutoField(primary_key=True)
	phone = models.CharField(max_length=20, unique=True)
	account = models.ForeignKey('Account')
	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "delegates"
		app_label = 'voicex'
