# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Property'
        db.create_table(u'app_property', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'app', ['Property'])

        # Adding M2M table for field reviews on 'Property'
        m2m_table_name = db.shorten_name(u'app_property_reviews')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('property', models.ForeignKey(orm[u'app.property'], null=False)),
            ('review', models.ForeignKey(orm[u'app.review'], null=False))
        ))
        db.create_unique(m2m_table_name, ['property_id', 'review_id'])

        # Adding model 'Review'
        db.create_table(u'app_review', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('grade', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'app', ['Review'])


    def backwards(self, orm):
        # Deleting model 'Property'
        db.delete_table(u'app_property')

        # Removing M2M table for field reviews on 'Property'
        db.delete_table(db.shorten_name(u'app_property_reviews'))

        # Deleting model 'Review'
        db.delete_table(u'app_review')


    models = {
        u'app.property': {
            'Meta': {'object_name': 'Property'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reviews': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Review']", 'null': 'True', 'symmetrical': 'False'})
        },
        u'app.review': {
            'Meta': {'object_name': 'Review'},
            'grade': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '5000'})
        }
    }

    complete_apps = ['app']