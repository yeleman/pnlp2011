# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'MalariaReport'
        db.create_table('pnlp_core_malariareport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pnlp_core_malariareport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pnlp_core_malariareport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pnlp_core_malariareport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('u5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_distributed_bednets', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_distributed_bednets', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_anc1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_sp1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_sp2', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_act_children', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_act_youth', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_act_adult', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_artemether', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_quinine', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_serum', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_bednet', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_rdt', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_sp', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('pnlp_core', ['MalariaReport'])

        # Adding unique constraint on 'MalariaReport', fields ['period', 'entity', 'type']
        db.create_unique('pnlp_core_malariareport', ['period_id', 'entity_id', 'type'])

        # Adding M2M table for field sources on 'MalariaReport'
        db.create_table('pnlp_core_malariareport_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_malariareport', models.ForeignKey(orm['pnlp_core.malariareport'], null=False)),
            ('to_malariareport', models.ForeignKey(orm['pnlp_core.malariareport'], null=False))
        ))
        db.create_unique('pnlp_core_malariareport_sources', ['from_malariareport_id', 'to_malariareport_id'])

        # Adding model 'Alert'
        db.create_table('pnlp_core_alert', (
            ('alert_id', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('pnlp_core', ['Alert'])


    def backwards(self, orm):

        # Removing unique constraint on 'MalariaReport', fields ['period', 'entity', 'type']
        db.delete_unique('pnlp_core_malariareport', ['period_id', 'entity_id', 'type'])

        # Deleting model 'MalariaReport'
        db.delete_table('pnlp_core_malariareport')

        # Removing M2M table for field sources on 'MalariaReport'
        db.delete_table('pnlp_core_malariareport_sources')

        # Deleting model 'Alert'
        db.delete_table('pnlp_core_alert')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bolibana.access': {
            'Meta': {'unique_together': "(('role', 'content_type', 'object_id'),)", 'object_name': 'Access'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Role']"})
        },
        'bolibana.entity': {
            'Meta': {'object_name': 'Entity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['bolibana.Entity']"}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'to': "orm['bolibana.EntityType']"})
        },
        'bolibana.entitytype': {
            'Meta': {'object_name': 'EntityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'})
        },
        'bolibana.period': {
            'Meta': {'unique_together': "(('start_on', 'end_on', 'period_type'),)", 'object_name': 'Period'},
            'end_on': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period_type': ('django.db.models.fields.CharField', [], {'default': "'custom'", 'max_length': '15'}),
            'start_on': ('django.db.models.fields.DateTimeField', [], {})
        },
        'bolibana.permission': {
            'Meta': {'object_name': 'Permission'},
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'bolibana.provider': {
            'Meta': {'object_name': 'Provider'},
            'access': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolibana.Access']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone_number_extra': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'bolibana.role': {
            'Meta': {'object_name': 'Role'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolibana.Permission']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '15', 'primary_key': 'True', 'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pnlp_core.alert': {
            'Meta': {'object_name': 'Alert'},
            'alert_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'pnlp_core.malariareport': {
            'Meta': {'unique_together': "(('period', 'entity', 'type'),)", 'object_name': 'MalariaReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pnlp_core_malariareport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pnlp_core_malariareport_reports'", 'to': "orm['bolibana.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'o5_total_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_inpatient_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_malaria_inpatient': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_treated_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pnlp_core_malariareport_reports'", 'to': "orm['bolibana.Period']"}),
            'pw_total_anc1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_distributed_bednets': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_inpatient_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_malaria_inpatient': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_sp1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_sp2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_treated_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['pnlp_core.MalariaReport']", 'null': 'True', 'blank': 'True'}),
            'stockout_act_adult': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_act_children': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_act_youth': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_artemether': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_bednet': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_quinine': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_rdt': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_serum': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_sp': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_distributed_bednets': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_inpatient_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_malaria_inpatient': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_treated_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['pnlp_core']
