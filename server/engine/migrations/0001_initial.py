# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table('posts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('post', self.gf('django.db.models.fields.TextField')()),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('reply_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replies', null=True, to=orm['engine.Post'])),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('engine', ['Post'])

        # Adding model 'Follow_Tag'
        db.create_table('follow_tags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('follow_list', self.gf('django.db.models.fields.TextField')()),
            ('parent_tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['engine.Follow_Tag'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('engine', ['Follow_Tag'])
        
        db.execute("""
			ALTER TABLE posts ADD COLUMN post_tsv tsvector;
			CREATE TRIGGER post_tsvector_update BEFORE INSERT OR UPDATE ON posts 
			FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(post_tsv, 'pg_catalog.english', post);
			CREATE INDEX post_index ON posts USING gin(post_tsv);
			UPDATE posts SET post_tsv=to_tsvector(post);
		""")  


    def backwards(self, orm):
        # Deleting model 'Post'
        db.delete_table('posts')

        # Deleting model 'Follow_Tag'
        db.delete_table('follow_tags')


    models = {
        'engine.follow_tag': {
            'Meta': {'object_name': 'Follow_Tag', 'db_table': "'follow_tags'"},
            'follow_list': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['engine.Follow_Tag']"}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'engine.post': {
            'Meta': {'object_name': 'Post', 'db_table': "'posts'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'post': ('django.db.models.fields.TextField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'null': 'True', 'to': "orm['engine.Post']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['engine']
