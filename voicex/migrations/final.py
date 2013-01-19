"""
Copyright (c) 2012 Anant Bhardwaj

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


import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

'''
Triggers for building search indexes

@author: Anant Bhardwaj
@date: Oct 8, 2012
'''

class Migration(SchemaMigration):

    	def forwards(self, orm):
		db.execute("""
                        ALTER TABLE posts ADD COLUMN post_tsv tsvector;
                        CREATE TRIGGER post_tsvector_update BEFORE INSERT OR UPDATE ON posts 
                        FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(post_tsv, 'pg_catalog.english', post);
                        CREATE INDEX post_index ON posts USING gin(post_tsv);
                        UPDATE posts SET post_tsv=to_tsvector(post);
                	""")

	def backwards(self, orm):
        	pass
