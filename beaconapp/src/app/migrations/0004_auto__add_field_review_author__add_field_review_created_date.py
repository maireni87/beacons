# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Review.author'
        db.add_column(u'app_review', 'author',
                      self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=1000),
                      keep_default=False)

        # Adding field 'Review.created_date'
        db.add_column(u'app_review', 'created_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 22, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Review.author'
        db.delete_column(u'app_review', 'author')

        # Deleting field 'Review.created_date'
        db.delete_column(u'app_review', 'created_date')


    models = {
        u'app.property': {
            'Meta': {'object_name': 'Property'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reviews': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Review']", 'null': 'True', 'symmetrical': 'False'})
        },
        u'app.review': {
            'Meta': {'object_name': 'Review'},
            'author': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '1000'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 22, 0, 0)'}),
            'grade': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        }
    }

    complete_apps = ['app']