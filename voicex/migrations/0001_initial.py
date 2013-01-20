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
            ('reply_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replies', null=True, to=orm['voicex.Post'])),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('voicex', ['Post'])

        # Adding model 'Subscriber'
        db.create_table('subscribers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voicex.Account'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('voicex', ['Subscriber'])

        # Adding unique constraint on 'Subscriber', fields ['phone', 'account']
        db.create_unique('subscribers', ['phone', 'account_id'])

        # Adding model 'Account'
        db.create_table('accounts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('phone', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('voicex', ['Account'])

        # Adding model 'Delegate'
        db.create_table('delegates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voicex.Account'])),
        ))
        db.send_create_signal('voicex', ['Delegate'])

        # Adding model 'Following'
        db.create_table('following', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voicex.Tag'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('voicex', ['Following'])

        # Adding unique constraint on 'Following', fields ['phone', 'tag']
        db.create_unique('following', ['phone', 'tag_id'])

        # Adding model 'Tag'
        db.create_table('tags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('voicex', ['Tag'])


    def backwards(self, orm):
        # Removing unique constraint on 'Following', fields ['phone', 'tag']
        db.delete_unique('following', ['phone', 'tag_id'])

        # Removing unique constraint on 'Subscriber', fields ['phone', 'account']
        db.delete_unique('subscribers', ['phone', 'account_id'])

        # Deleting model 'Post'
        db.delete_table('posts')

        # Deleting model 'Subscriber'
        db.delete_table('subscribers')

        # Deleting model 'Account'
        db.delete_table('accounts')

        # Deleting model 'Delegate'
        db.delete_table('delegates')

        # Deleting model 'Following'
        db.delete_table('following')

        # Deleting model 'Tag'
        db.delete_table('tags')


    models = {
        'voicex.account': {
            'Meta': {'object_name': 'Account', 'db_table': "'accounts'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'voicex.delegate': {
            'Meta': {'object_name': 'Delegate', 'db_table': "'delegates'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['voicex.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'voicex.following': {
            'Meta': {'unique_together': "(('phone', 'tag'),)", 'object_name': 'Following', 'db_table': "'following'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['voicex.Tag']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'voicex.post': {
            'Meta': {'object_name': 'Post', 'db_table': "'posts'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'post': ('django.db.models.fields.TextField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'null': 'True', 'to': "orm['voicex.Post']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'voicex.subscriber': {
            'Meta': {'unique_together': "(('phone', 'account'),)", 'object_name': 'Subscriber', 'db_table': "'subscribers'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['voicex.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'voicex.tag': {
            'Meta': {'object_name': 'Tag', 'db_table': "'tags'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['voicex']