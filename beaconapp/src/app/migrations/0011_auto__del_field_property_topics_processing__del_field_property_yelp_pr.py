# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Property.topics_processing'
        db.delete_column(u'app_property', 'topics_processing')

        # Deleting field 'Property.yelp_processing'
        db.delete_column(u'app_property', 'yelp_processing')


    def backwards(self, orm):
        # Adding field 'Property.topics_processing'
        db.add_column(u'app_property', 'topics_processing',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Property.yelp_processing'
        db.add_column(u'app_property', 'yelp_processing',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'app.property': {
            'Meta': {'object_name': 'Property'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reviews': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Review']", 'null': 'True', 'symmetrical': 'False'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Topic']", 'null': 'True', 'symmetrical': 'False'}),
            'topics_analyzed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'yelp_scraped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'yelp_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'app.review': {
            'Meta': {'object_name': 'Review'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 10, 15, 0, 0)'}),
            'grade': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        },
        u'app.scrapedtextprovider': {
            'Meta': {'object_name': 'ScrapedTextProvider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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