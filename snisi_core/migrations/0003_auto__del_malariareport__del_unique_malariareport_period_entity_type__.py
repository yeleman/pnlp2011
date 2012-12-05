# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'MalariaReport', fields ['period', 'entity', 'type']
        db.delete_unique('snisi_core_malariareport', ['period_id', 'entity_id', 'type'])

        # Deleting model 'MalariaReport'
        db.delete_table('snisi_core_malariareport')

        # Removing M2M table for field sources on 'MalariaReport'
        db.delete_table('snisi_core_malariareport_sources')

        # Deleting model 'Alert'
        db.delete_table('snisi_core_alert')

        # Adding model 'EpidemiologyReport'
        db.create_table('snisi_core_epidemiologyreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_epidemiologyreport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_epidemiologyreport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_epidemiologyreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('acute_flaccid_paralysis_case', self.gf('django.db.models.fields.IntegerField')()),
            ('acute_flaccid_paralysis_death', self.gf('django.db.models.fields.IntegerField')()),
            ('influenza_a_h1n1_case', self.gf('django.db.models.fields.IntegerField')()),
            ('influenza_a_h1n1_death', self.gf('django.db.models.fields.IntegerField')()),
            ('cholera_case', self.gf('django.db.models.fields.IntegerField')()),
            ('cholera_death', self.gf('django.db.models.fields.IntegerField')()),
            ('red_diarrhea_case', self.gf('django.db.models.fields.IntegerField')()),
            ('red_diarrhea_death', self.gf('django.db.models.fields.IntegerField')()),
            ('measles_case', self.gf('django.db.models.fields.IntegerField')()),
            ('measles_death', self.gf('django.db.models.fields.IntegerField')()),
            ('yellow_fever_case', self.gf('django.db.models.fields.IntegerField')()),
            ('yellow_fever_death', self.gf('django.db.models.fields.IntegerField')()),
            ('neonatal_tetanus_case', self.gf('django.db.models.fields.IntegerField')()),
            ('neonatal_tetanus_death', self.gf('django.db.models.fields.IntegerField')()),
            ('meningitis_case', self.gf('django.db.models.fields.IntegerField')()),
            ('meningitis_death', self.gf('django.db.models.fields.IntegerField')()),
            ('rabies_case', self.gf('django.db.models.fields.IntegerField')()),
            ('rabies_death', self.gf('django.db.models.fields.IntegerField')()),
            ('acute_measles_diarrhea_case', self.gf('django.db.models.fields.IntegerField')()),
            ('acute_measles_diarrhea_death', self.gf('django.db.models.fields.IntegerField')()),
            ('other_notifiable_disease_case', self.gf('django.db.models.fields.IntegerField')()),
            ('other_notifiable_disease_death', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('snisi_core', ['EpidemiologyReport'])

        # Adding model 'ChildrenMortalityReport'
        db.create_table('snisi_core_childrenmortalityreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_childrenmortalityreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reporting_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children_reported_in', to=orm['bolibana.Entity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('dob_auto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dod', self.gf('django.db.models.fields.DateField')()),
            ('death_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children_dead_in', to=orm['bolibana.Entity'])),
            ('death_place', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('cause_of_death', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('snisi_core', ['ChildrenMortalityReport'])

        # Adding model 'UEntity'
        db.create_table('snisi_core_uentity', (
            ('entity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bolibana.Entity'], unique=True, primary_key=True)),
            ('is_unfpa', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_credos', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('snisi_core', ['UEntity'])

        # Adding model 'MaternalMortalityReport'
        db.create_table('snisi_core_maternalmortalityreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_maternalmortalityreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reporting_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='maternal_reported_in', to=orm['bolibana.Entity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('dob_auto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dod', self.gf('django.db.models.fields.DateField')()),
            ('death_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='maternal_dead_in', to=orm['bolibana.Entity'])),
            ('living_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('dead_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pregnant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pregnancy_weeks', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('pregnancy_related_death', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cause_of_death', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('snisi_core', ['MaternalMortalityReport'])

        # Adding model 'ProvidedServicesReport'
        db.create_table('snisi_core_providedservicesreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_providedservicesreport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_providedservicesreport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_providedservicesreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('iud', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injectable', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('oral_pills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condom', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condom', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('emergency_contraception', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('new_client', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('returning_client', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_u25', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_o25', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_first_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_ams_ticket', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_provider_ticket', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_short_term', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_long_term', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('client_hiv_counselling', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('client_hiv_tested', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('client_hiv_positive', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removal', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('total_hiv_test', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('snisi_core', ['ProvidedServicesReport'])

        # Adding M2M table for field sources on 'ProvidedServicesReport'
        db.create_table('snisi_core_providedservicesreport_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_providedservicesreport', models.ForeignKey(orm['snisi_core.providedservicesreport'], null=False)),
            ('to_providedservicesreport', models.ForeignKey(orm['snisi_core.providedservicesreport'], null=False))
        ))
        db.create_unique('snisi_core_providedservicesreport_sources', ['from_providedservicesreport_id', 'to_providedservicesreport_id'])

        # Adding unique constraint on 'ProvidedServicesReport', fields ['period', 'entity', 'type']
        db.create_unique('snisi_core_providedservicesreport', ['period_id', 'entity_id', 'type'])

        # Adding model 'BirthReport'
        db.create_table('snisi_core_birthreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_birthreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reporting_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='birth_reported_in', to=orm['bolibana.Entity'])),
            ('family_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('surname_mother', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('surname_child', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('dob_auto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('born_alive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('birth_location', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('snisi_core', ['BirthReport'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ProvidedServicesReport', fields ['period', 'entity', 'type']
        db.delete_unique('snisi_core_providedservicesreport', ['period_id', 'entity_id', 'type'])

        # Adding model 'MalariaReport'
        db.create_table('snisi_core_malariareport', (
            ('pw_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_act_youth', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('u5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_malariareport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_malariareport_reports', to=orm['bolibana.Entity'])),
            ('stockout_act_adult', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('u5_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_quinine', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('u5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_malariareport_reports', to=orm['bolibana.Provider'])),
            ('stockout_bednet', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('pw_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_sp', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('o5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_distributed_bednets', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_act_children', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('o5_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_distributed_bednets', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True, blank=True)),
            ('stockout_artemether', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('stockout_rdt', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pw_total_sp2', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_sp1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_anc1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_serum', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('o5_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('o5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('snisi_core', ['MalariaReport'])

        # Adding M2M table for field sources on 'MalariaReport'
        db.create_table('snisi_core_malariareport_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_malariareport', models.ForeignKey(orm['snisi_core.malariareport'], null=False)),
            ('to_malariareport', models.ForeignKey(orm['snisi_core.malariareport'], null=False))
        ))
        db.create_unique('snisi_core_malariareport_sources', ['from_malariareport_id', 'to_malariareport_id'])

        # Adding unique constraint on 'MalariaReport', fields ['period', 'entity', 'type']
        db.create_unique('snisi_core_malariareport', ['period_id', 'entity_id', 'type'])

        # Adding model 'Alert'
        db.create_table('snisi_core_alert', (
            ('alert_id', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('snisi_core', ['Alert'])

        # Deleting model 'EpidemiologyReport'
        db.delete_table('snisi_core_epidemiologyreport')

        # Deleting model 'ChildrenMortalityReport'
        db.delete_table('snisi_core_childrenmortalityreport')

        # Deleting model 'UEntity'
        db.delete_table('snisi_core_uentity')

        # Deleting model 'MaternalMortalityReport'
        db.delete_table('snisi_core_maternalmortalityreport')

        # Deleting model 'ProvidedServicesReport'
        db.delete_table('snisi_core_providedservicesreport')

        # Removing M2M table for field sources on 'ProvidedServicesReport'
        db.delete_table('snisi_core_providedservicesreport_sources')

        # Deleting model 'BirthReport'
        db.delete_table('snisi_core_birthreport')


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
            'pwhash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'bolibana.role': {
            'Meta': {'object_name': 'Role'},
            'level': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
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
        'snisi_core.birthreport': {
            'Meta': {'object_name': 'BirthReport'},
            'birth_location': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'born_alive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_birthreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'dob_auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'birth_reported_in'", 'to': "orm['bolibana.Entity']"}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'surname_child': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'surname_mother': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'snisi_core.childrenmortalityreport': {
            'Meta': {'object_name': 'ChildrenMortalityReport'},
            'cause_of_death': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_childrenmortalityreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'death_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children_dead_in'", 'to': "orm['bolibana.Entity']"}),
            'death_place': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'dob_auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dod': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children_reported_in'", 'to': "orm['bolibana.Entity']"}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        'snisi_core.epidemiologyreport': {
            'Meta': {'object_name': 'EpidemiologyReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'acute_flaccid_paralysis_case': ('django.db.models.fields.IntegerField', [], {}),
            'acute_flaccid_paralysis_death': ('django.db.models.fields.IntegerField', [], {}),
            'acute_measles_diarrhea_case': ('django.db.models.fields.IntegerField', [], {}),
            'acute_measles_diarrhea_death': ('django.db.models.fields.IntegerField', [], {}),
            'cholera_case': ('django.db.models.fields.IntegerField', [], {}),
            'cholera_death': ('django.db.models.fields.IntegerField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_epidemiologyreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_epidemiologyreport_reports'", 'to': "orm['bolibana.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'influenza_a_h1n1_case': ('django.db.models.fields.IntegerField', [], {}),
            'influenza_a_h1n1_death': ('django.db.models.fields.IntegerField', [], {}),
            'measles_case': ('django.db.models.fields.IntegerField', [], {}),
            'measles_death': ('django.db.models.fields.IntegerField', [], {}),
            'meningitis_case': ('django.db.models.fields.IntegerField', [], {}),
            'meningitis_death': ('django.db.models.fields.IntegerField', [], {}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'neonatal_tetanus_case': ('django.db.models.fields.IntegerField', [], {}),
            'neonatal_tetanus_death': ('django.db.models.fields.IntegerField', [], {}),
            'other_notifiable_disease_case': ('django.db.models.fields.IntegerField', [], {}),
            'other_notifiable_disease_death': ('django.db.models.fields.IntegerField', [], {}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_epidemiologyreport_reports'", 'to': "orm['bolibana.Period']"}),
            'rabies_case': ('django.db.models.fields.IntegerField', [], {}),
            'rabies_death': ('django.db.models.fields.IntegerField', [], {}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'red_diarrhea_case': ('django.db.models.fields.IntegerField', [], {}),
            'red_diarrhea_death': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'yellow_fever_case': ('django.db.models.fields.IntegerField', [], {}),
            'yellow_fever_death': ('django.db.models.fields.IntegerField', [], {})
        },
        'snisi_core.maternalmortalityreport': {
            'Meta': {'object_name': 'MaternalMortalityReport'},
            'cause_of_death': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_maternalmortalityreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dead_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'death_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maternal_dead_in'", 'to': "orm['bolibana.Entity']"}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'dob_auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dod': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'living_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pregnancy_related_death': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pregnancy_weeks': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pregnant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maternal_reported_in'", 'to': "orm['bolibana.Entity']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        },
        'snisi_core.providedservicesreport': {
            'Meta': {'unique_together': "(('period', 'entity', 'type'),)", 'object_name': 'ProvidedServicesReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'client_hiv_counselling': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'client_hiv_positive': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'client_hiv_tested': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_providedservicesreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'emergency_contraception': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_providedservicesreport_reports'", 'to': "orm['bolibana.Entity']"}),
            'female_condom': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implant': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injectable': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condom': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'new_client': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'oral_pills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_providedservicesreport_reports'", 'to': "orm['bolibana.Period']"}),
            'pf_first_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_ams_ticket': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_long_term': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_o25': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_provider_ticket': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_short_term': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_u25': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'returning_client': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['snisi_core.ProvidedServicesReport']", 'null': 'True', 'blank': 'True'}),
            'total_hiv_test': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'snisi_core.uentity': {
            'Meta': {'object_name': 'UEntity', '_ormbases': ['bolibana.Entity']},
            'entity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bolibana.Entity']", 'unique': 'True', 'primary_key': 'True'}),
            'is_credos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_unfpa': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['snisi_core']
