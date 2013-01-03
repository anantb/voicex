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
