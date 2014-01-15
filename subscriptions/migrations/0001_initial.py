# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('subscriptions_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('subscriptions', ['Group'])

        # Adding model 'CoopUser'
        db.create_table('subscriptions_coopuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscriptions.Group'])),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('wesid', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=30)),
        ))
        db.send_create_signal('subscriptions', ['CoopUser'])

        # Adding model 'Coop'
        db.create_table('subscriptions_coop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('subscriptions', ['Coop'])

        # Adding model 'Subscription'
        db.create_table('subscriptions_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shares', self.gf('django.db.models.fields.IntegerField')()),
            ('coopuser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscriptions.CoopUser'])),
            ('coop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscriptions.Coop'])),
        ))
        db.send_create_signal('subscriptions', ['Subscription'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table('subscriptions_group')

        # Deleting model 'CoopUser'
        db.delete_table('subscriptions_coopuser')

        # Deleting model 'Coop'
        db.delete_table('subscriptions_coop')

        # Deleting model 'Subscription'
        db.delete_table('subscriptions_subscription')


    models = {
        'subscriptions.coop': {
            'Meta': {'object_name': 'Coop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'subscriptions.coopuser': {
            'Meta': {'object_name': 'CoopUser'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '30'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subscriptions.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'wesid': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'subscriptions.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'subscriptions.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'coop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subscriptions.Coop']"}),
            'coopuser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['subscriptions.CoopUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shares': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['subscriptions']