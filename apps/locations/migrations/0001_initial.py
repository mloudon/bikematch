# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Location'
        db.create_table('locations_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('accuracy', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('time_zone', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('automatic', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('locations', ['Location'])

    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table('locations_location')

    models = {
        'locations.location': {
            'Meta': {'object_name': 'Location'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'automatic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'time_zone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['locations']
