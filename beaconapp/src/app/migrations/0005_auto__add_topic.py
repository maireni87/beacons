# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topic'
        db.create_table(u'app_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.CharField')(default='NGRAM', max_length=100)),
        ))
        db.send_create_signal(u'app', ['Topic'])

        # Adding M2M table for field reviews on 'Topic'
        m2m_table_name = db.shorten_name(u'app_topic_reviews')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('topic', models.ForeignKey(orm[u'app.topic'], null=False)),
            ('review', models.ForeignKey(orm[u'app.review'], null=False))
        ))
        db.create_unique(m2m_table_name, ['topic_id', 'review_id'])

        # Adding M2M table for field topics on 'Property'
        m2m_table_name = db.shorten_name(u'app_property_topics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('property', models.ForeignKey(orm[u'app.property'], null=False)),
            ('topic', models.ForeignKey(orm[u'app.topic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['property_id', 'topic_id'])


    def backwards(self, orm):
        # Deleting model 'Topic'
        db.delete_table(u'app_topic')

        # Removing M2M table for field reviews on 'Topic'
        db.delete_table(db.shorten_name(u'app_topic_reviews'))

        # Removing M2M table for field topics on 'Property'
        db.delete_table(db.shorten_name(u'app_property_topics'))


    models = {
        u'app.property': {
            'Meta': {'object_name': 'Property'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reviews': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Review']", 'null': 'True', 'symmetrical': 'False'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Topic']", 'null': 'True', 'symmetrical': 'False'})
        },
        u'app.review': {
            'Meta': {'object_name': 'Review'},
            'author': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '1000'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 23, 0, 0)'}),
            'grade': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        },
        u'app.topic': {
            'Meta': {'object_name': 'Topic'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'NGRAM'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reviews': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Review']", 'null': 'True', 'symmetrical': 'False'})
        }
    }

    complete_apps = ['app']