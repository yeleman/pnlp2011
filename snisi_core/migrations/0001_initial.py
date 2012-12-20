# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MalariaReport'
        db.create_table('snisi_core_malariareport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_malariareport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_malariareport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_malariareport_reports', to=orm['bolibana.Provider'])),
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
        db.send_create_signal('snisi_core', ['MalariaReport'])

        # Adding unique constraint on 'MalariaReport', fields ['period', 'entity', 'type']
        db.create_unique('snisi_core_malariareport', ['period_id', 'entity_id', 'type'])

        # Adding M2M table for field sources on 'MalariaReport'
        db.create_table('snisi_core_malariareport_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_malariareport', models.ForeignKey(orm['snisi_core.malariareport'], null=False)),
            ('to_malariareport', models.ForeignKey(orm['snisi_core.malariareport'], null=False))
        ))
        db.create_unique('snisi_core_malariareport_sources', ['from_malariareport_id', 'to_malariareport_id'])

        # Adding model 'AggregatedMalariaReport'
        db.create_table('snisi_core_aggregatedmalariareport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedmalariareport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedmalariareport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedmalariareport_reports', to=orm['bolibana.Provider'])),
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
            ('stockout_act_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_act_youth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_act_adult', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_artemether', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_quinine', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_serum', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_bednet', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_rdt', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_sp', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('nb_prompt', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('snisi_core', ['AggregatedMalariaReport'])

        # Adding unique constraint on 'AggregatedMalariaReport', fields ['period', 'entity', 'type']
        db.create_unique('snisi_core_aggregatedmalariareport', ['period_id', 'entity_id', 'type'])

        # Adding M2M table for field indiv_sources on 'AggregatedMalariaReport'
        db.create_table('snisi_core_aggregatedmalariareport_indiv_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggregatedmalariareport', models.ForeignKey(orm['snisi_core.aggregatedmalariareport'], null=False)),
            ('malariareport', models.ForeignKey(orm['snisi_core.malariareport'], null=False))
        ))
        db.create_unique('snisi_core_aggregatedmalariareport_indiv_sources', ['aggregatedmalariareport_id', 'malariareport_id'])

        # Adding M2M table for field agg_sources on 'AggregatedMalariaReport'
        db.create_table('snisi_core_aggregatedmalariareport_agg_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggregatedmalariareport', models.ForeignKey(orm['snisi_core.aggregatedmalariareport'], null=False)),
            ('to_aggregatedmalariareport', models.ForeignKey(orm['snisi_core.aggregatedmalariareport'], null=False))
        ))
        db.create_unique('snisi_core_aggregatedmalariareport_agg_sources', ['from_aggregatedmalariareport_id', 'to_aggregatedmalariareport_id'])

        # Adding model 'Alert'
        db.create_table('snisi_core_alert', (
            ('alert_id', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('snisi_core', ['Alert'])

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
        ))
        db.send_create_signal('snisi_core', ['MaternalMortalityReport'])

        # Adding model 'AggregatedMaternalMortalityReport'
        db.create_table('snisi_core_aggregatedmaternalmortalityreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedmaternalmortalityreport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedmaternalmortalityreport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedmaternalmortalityreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('age_under_15', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_18', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_20', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_25', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_30', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_35', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_40', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_45', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_50', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_over_50', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('have_living_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('have_one_living_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('have_two_living_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('have_two_plus_living_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('have_dead_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('have_one_dead_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('have_two_dead_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('have_two_plus_dead_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_1week', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_2weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_3weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_4weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_5weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_6weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_7weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_8weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_9weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_10weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_11weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_12weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_13weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_14weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_15weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_16weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_17weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_18weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_19weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_20weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_21weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_22weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_23weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_24weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_25weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_26weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_27weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_28weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_29weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_30weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_31weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_32weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_33weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_34weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_35weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_36weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_37weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_38weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_39weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_40weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnant_40weeks_plus', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_pregnancy_related', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_bleeding', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_fever', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_htn', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_diarrhea', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_crisis', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_miscarriage', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_abortion', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_other', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('snisi_core', ['AggregatedMaternalMortalityReport'])

        # Adding M2M table for field indiv_sources on 'AggregatedMaternalMortalityReport'
        db.create_table('snisi_core_aggregatedmaternalmortalityreport_indiv_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggregatedmaternalmortalityreport', models.ForeignKey(orm['snisi_core.aggregatedmaternalmortalityreport'], null=False)),
            ('maternalmortalityreport', models.ForeignKey(orm['snisi_core.maternalmortalityreport'], null=False))
        ))
        db.create_unique('snisi_core_aggregatedmaternalmortalityreport_indiv_sources', ['aggregatedmaternalmortalityreport_id', 'maternalmortalityreport_id'])

        # Adding M2M table for field agg_sources on 'AggregatedMaternalMortalityReport'
        db.create_table('snisi_core_aggregatedmaternalmortalityreport_agg_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggregatedmaternalmortalityreport', models.ForeignKey(orm['snisi_core.aggregatedmaternalmortalityreport'], null=False)),
            ('to_aggregatedmaternalmortalityreport', models.ForeignKey(orm['snisi_core.aggregatedmaternalmortalityreport'], null=False))
        ))
        db.create_unique('snisi_core_aggregatedmaternalmortalityreport_agg_sources', ['from_aggregatedmaternalmortalityreport_id', 'to_aggregatedmaternalmortalityreport_id'])

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
        ))
        db.send_create_signal('snisi_core', ['ChildrenMortalityReport'])

        # Adding model 'AggregatedChildrenMortalityReport'
        db.create_table('snisi_core_aggregatedchildrenmortalityreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedchildrenmortalityreport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedchildrenmortalityreport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedchildrenmortalityreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sex_male', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('sexe_female', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_1w', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_2weeks', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_1month', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_3month', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_6month', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_9month', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_2', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_3', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_4', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('age_under_5', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('death_home', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('death_center', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('death_other', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_fever', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_diarrhea', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_dyspnea', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_anemia', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_rash', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_cough', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_vomiting', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_nuchal_rigidity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_red_eye', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_eat_refusal', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cause_death_other', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('snisi_core', ['AggregatedChildrenMortalityReport'])

        # Adding M2M table for field indiv_sources on 'AggregatedChildrenMortalityReport'
        db.create_table('snisi_core_aggregatedchildrenmortalityreport_indiv_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggregatedchildrenmortalityreport', models.ForeignKey(orm['snisi_core.aggregatedchildrenmortalityreport'], null=False)),
            ('childrenmortalityreport', models.ForeignKey(orm['snisi_core.childrenmortalityreport'], null=False))
        ))
        db.create_unique('snisi_core_aggregatedchildrenmortalityreport_indiv_sources', ['aggregatedchildrenmortalityreport_id', 'childrenmortalityreport_id'])

        # Adding M2M table for field agg_sources on 'AggregatedChildrenMortalityReport'
        db.create_table('snisi_core_aggregatedchildrenmortalityreport_agg_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggregatedchildrenmortalityreport', models.ForeignKey(orm['snisi_core.aggregatedchildrenmortalityreport'], null=False)),
            ('to_aggregatedchildrenmortalityreport', models.ForeignKey(orm['snisi_core.aggregatedchildrenmortalityreport'], null=False))
        ))
        db.create_unique('snisi_core_aggregatedchildrenmortalityreport_agg_sources', ['from_aggregatedchildrenmortalityreport_id', 'to_aggregatedchildrenmortalityreport_id'])

        # Adding model 'RHCommoditiesReport'
        db.create_table('snisi_core_rhcommoditiesreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_rhcommoditiesreport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_rhcommoditiesreport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_rhcommoditiesreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('family_planning', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delivery_services', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('male_condom', self.gf('django.db.models.fields.IntegerField')()),
            ('female_condom', self.gf('django.db.models.fields.IntegerField')()),
            ('oral_pills', self.gf('django.db.models.fields.IntegerField')()),
            ('injectable', self.gf('django.db.models.fields.IntegerField')()),
            ('iud', self.gf('django.db.models.fields.IntegerField')()),
            ('implants', self.gf('django.db.models.fields.IntegerField')()),
            ('female_sterilization', self.gf('django.db.models.fields.IntegerField')()),
            ('male_sterilization', self.gf('django.db.models.fields.IntegerField')()),
            ('amoxicillin_ij', self.gf('django.db.models.fields.IntegerField')()),
            ('amoxicillin_cap_gel', self.gf('django.db.models.fields.IntegerField')()),
            ('amoxicillin_suspension', self.gf('django.db.models.fields.IntegerField')()),
            ('azithromycine_tab', self.gf('django.db.models.fields.IntegerField')()),
            ('azithromycine_suspension', self.gf('django.db.models.fields.IntegerField')()),
            ('benzathine_penicillin', self.gf('django.db.models.fields.IntegerField')()),
            ('cefexime', self.gf('django.db.models.fields.IntegerField')()),
            ('clotrimazole', self.gf('django.db.models.fields.IntegerField')()),
            ('ergometrine_tab', self.gf('django.db.models.fields.IntegerField')()),
            ('ergometrine_vials', self.gf('django.db.models.fields.IntegerField')()),
            ('iron', self.gf('django.db.models.fields.IntegerField')()),
            ('folate', self.gf('django.db.models.fields.IntegerField')()),
            ('iron_folate', self.gf('django.db.models.fields.IntegerField')()),
            ('magnesium_sulfate', self.gf('django.db.models.fields.IntegerField')()),
            ('metronidazole', self.gf('django.db.models.fields.IntegerField')()),
            ('oxytocine', self.gf('django.db.models.fields.IntegerField')()),
            ('ceftriaxone_500', self.gf('django.db.models.fields.IntegerField')()),
            ('ceftriaxone_1000', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('snisi_core', ['RHCommoditiesReport'])

        # Adding unique constraint on 'RHCommoditiesReport', fields ['period', 'entity', 'type']
        db.create_unique('snisi_core_rhcommoditiesreport', ['period_id', 'entity_id', 'type'])

        # Adding model 'AggregatedRHCommoditiesReport'
        db.create_table('snisi_core_aggregatedrhcommoditiesreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedrhcommoditiesreport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedrhcommoditiesreport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snisi_core_aggregatedrhcommoditiesreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('family_planning_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('delivery_services_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condom_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condom_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condom_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condom_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('oral_pills_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('oral_pills_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injectable_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injectable_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_sterilization_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_sterilization_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_sterilization_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_sterilization_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amoxicillin_ij_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amoxicillin_ij_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amoxicillin_cap_gel_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amoxicillin_cap_gel_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amoxicillin_suspension_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amoxicillin_suspension_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('azithromycine_tab_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('azithromycine_tab_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('azithromycine_suspension_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('azithromycine_suspension_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('benzathine_penicillin_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('benzathine_penicillin_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cefexime_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cefexime_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('clotrimazole_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('clotrimazole_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ergometrine_tab_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ergometrine_tab_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ergometrine_vials_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ergometrine_vials_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iron_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iron_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('folate_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('folate_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iron_folate_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iron_folate_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('magnesium_sulfate_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('magnesium_sulfate_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('metronidazole_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('metronidazole_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('oxytocine_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('oxytocine_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ceftriaxone_500_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ceftriaxone_500_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ceftriaxone_1000_provided', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ceftriaxone_1000_available', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('nb_prompt', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('snisi_core', ['AggregatedRHCommoditiesReport'])

        # Adding unique constraint on 'AggregatedRHCommoditiesReport', fields ['period', 'entity', 'type']
        db.create_unique('snisi_core_aggregatedrhcommoditiesreport', ['period_id', 'entity_id', 'type'])

        # Adding M2M table for field indiv_sources on 'AggregatedRHCommoditiesReport'
        db.create_table('snisi_core_aggregatedrhcommoditiesreport_indiv_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggregatedrhcommoditiesreport', models.ForeignKey(orm['snisi_core.aggregatedrhcommoditiesreport'], null=False)),
            ('rhcommoditiesreport', models.ForeignKey(orm['snisi_core.rhcommoditiesreport'], null=False))
        ))
        db.create_unique('snisi_core_aggregatedrhcommoditiesreport_indiv_sources', ['aggregatedrhcommoditiesreport_id', 'rhcommoditiesreport_id'])

        # Adding M2M table for field agg_sources on 'AggregatedRHCommoditiesReport'
        db.create_table('snisi_core_aggregatedrhcommoditiesreport_agg_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggregatedrhcommoditiesreport', models.ForeignKey(orm['snisi_core.aggregatedrhcommoditiesreport'], null=False)),
            ('to_aggregatedrhcommoditiesreport', models.ForeignKey(orm['snisi_core.aggregatedrhcommoditiesreport'], null=False))
        ))
        db.create_unique('snisi_core_aggregatedrhcommoditiesreport_agg_sources', ['from_aggregatedrhcommoditiesreport_id', 'to_aggregatedrhcommoditiesreport_id'])

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

        # Adding M2M table for field sources on 'EpidemiologyReport'
        db.create_table('snisi_core_epidemiologyreport_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_epidemiologyreport', models.ForeignKey(orm['snisi_core.epidemiologyreport'], null=False)),
            ('to_epidemiologyreport', models.ForeignKey(orm['snisi_core.epidemiologyreport'], null=False))
        ))
        db.create_unique('snisi_core_epidemiologyreport_sources', ['from_epidemiologyreport_id', 'to_epidemiologyreport_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'AggregatedRHCommoditiesReport', fields ['period', 'entity', 'type']
        db.delete_unique('snisi_core_aggregatedrhcommoditiesreport', ['period_id', 'entity_id', 'type'])

        # Removing unique constraint on 'RHCommoditiesReport', fields ['period', 'entity', 'type']
        db.delete_unique('snisi_core_rhcommoditiesreport', ['period_id', 'entity_id', 'type'])

        # Removing unique constraint on 'AggregatedMalariaReport', fields ['period', 'entity', 'type']
        db.delete_unique('snisi_core_aggregatedmalariareport', ['period_id', 'entity_id', 'type'])

        # Removing unique constraint on 'MalariaReport', fields ['period', 'entity', 'type']
        db.delete_unique('snisi_core_malariareport', ['period_id', 'entity_id', 'type'])

        # Deleting model 'MalariaReport'
        db.delete_table('snisi_core_malariareport')

        # Removing M2M table for field sources on 'MalariaReport'
        db.delete_table('snisi_core_malariareport_sources')

        # Deleting model 'AggregatedMalariaReport'
        db.delete_table('snisi_core_aggregatedmalariareport')

        # Removing M2M table for field indiv_sources on 'AggregatedMalariaReport'
        db.delete_table('snisi_core_aggregatedmalariareport_indiv_sources')

        # Removing M2M table for field agg_sources on 'AggregatedMalariaReport'
        db.delete_table('snisi_core_aggregatedmalariareport_agg_sources')

        # Deleting model 'Alert'
        db.delete_table('snisi_core_alert')

        # Deleting model 'MaternalMortalityReport'
        db.delete_table('snisi_core_maternalmortalityreport')

        # Deleting model 'AggregatedMaternalMortalityReport'
        db.delete_table('snisi_core_aggregatedmaternalmortalityreport')

        # Removing M2M table for field indiv_sources on 'AggregatedMaternalMortalityReport'
        db.delete_table('snisi_core_aggregatedmaternalmortalityreport_indiv_sources')

        # Removing M2M table for field agg_sources on 'AggregatedMaternalMortalityReport'
        db.delete_table('snisi_core_aggregatedmaternalmortalityreport_agg_sources')

        # Deleting model 'ChildrenMortalityReport'
        db.delete_table('snisi_core_childrenmortalityreport')

        # Deleting model 'AggregatedChildrenMortalityReport'
        db.delete_table('snisi_core_aggregatedchildrenmortalityreport')

        # Removing M2M table for field indiv_sources on 'AggregatedChildrenMortalityReport'
        db.delete_table('snisi_core_aggregatedchildrenmortalityreport_indiv_sources')

        # Removing M2M table for field agg_sources on 'AggregatedChildrenMortalityReport'
        db.delete_table('snisi_core_aggregatedchildrenmortalityreport_agg_sources')

        # Deleting model 'RHCommoditiesReport'
        db.delete_table('snisi_core_rhcommoditiesreport')

        # Deleting model 'AggregatedRHCommoditiesReport'
        db.delete_table('snisi_core_aggregatedrhcommoditiesreport')

        # Removing M2M table for field indiv_sources on 'AggregatedRHCommoditiesReport'
        db.delete_table('snisi_core_aggregatedrhcommoditiesreport_indiv_sources')

        # Removing M2M table for field agg_sources on 'AggregatedRHCommoditiesReport'
        db.delete_table('snisi_core_aggregatedrhcommoditiesreport_agg_sources')

        # Deleting model 'EpidemiologyReport'
        db.delete_table('snisi_core_epidemiologyreport')

        # Removing M2M table for field sources on 'EpidemiologyReport'
        db.delete_table('snisi_core_epidemiologyreport_sources')


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
        'snisi_core.aggregatedchildrenmortalityreport': {
            'Meta': {'object_name': 'AggregatedChildrenMortalityReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'age_under_1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_1month': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_1w': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_2weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_3': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_3month': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_4': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_5': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_6month': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_9month': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'aggregated_agg_children_mortality_reports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['snisi_core.AggregatedChildrenMortalityReport']"}),
            'cause_death_anemia': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_cough': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_diarrhea': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_dyspnea': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_eat_refusal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_fever': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_nuchal_rigidity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_other': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_rash': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_red_eye': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_death_vomiting': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedchildrenmortalityreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'death_center': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'death_home': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'death_other': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedchildrenmortalityreport_reports'", 'to': "orm['bolibana.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'indiv_agg_children_mortality_reports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['snisi_core.ChildrenMortalityReport']"}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedchildrenmortalityreport_reports'", 'to': "orm['bolibana.Period']"}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'sex_male': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sexe_female': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'snisi_core.aggregatedmalariareport': {
            'Meta': {'unique_together': "(('period', 'entity', 'type'),)", 'object_name': 'AggregatedMalariaReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'aggregated_agg_malaria_reports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['snisi_core.AggregatedMalariaReport']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedmalariareport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedmalariareport_reports'", 'to': "orm['bolibana.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'indiv_agg_malaria_reports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['snisi_core.MalariaReport']"}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nb_prompt': ('django.db.models.fields.PositiveIntegerField', [], {}),
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
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedmalariareport_reports'", 'to': "orm['bolibana.Period']"}),
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
            'stockout_act_adult': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_act_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_act_youth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_artemether': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_bednet': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_quinine': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_rdt': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_serum': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_sp': ('django.db.models.fields.PositiveIntegerField', [], {}),
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
        },
        'snisi_core.aggregatedmaternalmortalityreport': {
            'Meta': {'object_name': 'AggregatedMaternalMortalityReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'age_over_50': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_15': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_18': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_20': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_25': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_30': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_35': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_40': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_45': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'age_under_50': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'aggregated_agg_maternal_mortality_reports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['snisi_core.AggregatedMaternalMortalityReport']"}),
            'cause_abortion': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_bleeding': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_crisis': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_diarrhea': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_fever': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_htn': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_miscarriage': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cause_other': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedmaternalmortalityreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedmaternalmortalityreport_reports'", 'to': "orm['bolibana.Entity']"}),
            'have_dead_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'have_living_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'have_one_dead_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'have_one_living_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'have_two_dead_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'have_two_living_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'have_two_plus_dead_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'have_two_plus_living_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'indiv_agg_maternal_mortality_reports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['snisi_core.MaternalMortalityReport']"}),
            'is_pregnancy_related': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_10weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_11weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_12weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_13weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_14weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_15weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_16weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_17weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_18weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_19weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_1week': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_20weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_21weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_22weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_23weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_24weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_25weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_26weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_27weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_28weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_29weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_2weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_30weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_31weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_32weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_33weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_34weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_35weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_36weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_37weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_38weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_39weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_3weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_40weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_40weeks_plus': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_4weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_5weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_6weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_7weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_8weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'is_pregnant_9weeks': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedmaternalmortalityreport_reports'", 'to': "orm['bolibana.Period']"}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'snisi_core.aggregatedrhcommoditiesreport': {
            'Meta': {'unique_together': "(('period', 'entity', 'type'),)", 'object_name': 'AggregatedRHCommoditiesReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'aggregated_agg_rhcommodities_reports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['snisi_core.AggregatedRHCommoditiesReport']"}),
            'amoxicillin_cap_gel_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'amoxicillin_cap_gel_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'amoxicillin_ij_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'amoxicillin_ij_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'amoxicillin_suspension_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'amoxicillin_suspension_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'azithromycine_suspension_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'azithromycine_suspension_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'azithromycine_tab_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'azithromycine_tab_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'benzathine_penicillin_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'benzathine_penicillin_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cefexime_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cefexime_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ceftriaxone_1000_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ceftriaxone_1000_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ceftriaxone_500_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ceftriaxone_500_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'clotrimazole_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'clotrimazole_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedrhcommoditiesreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_services_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedrhcommoditiesreport_reports'", 'to': "orm['bolibana.Entity']"}),
            'ergometrine_tab_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ergometrine_tab_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ergometrine_vials_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ergometrine_vials_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'family_planning_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condom_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condom_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_sterilization_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_sterilization_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'folate_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'folate_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implants_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'indiv_agg_rhcommodities_reports'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['snisi_core.RHCommoditiesReport']"}),
            'injectable_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injectable_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iron_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iron_folate_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iron_folate_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iron_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'magnesium_sulfate_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'magnesium_sulfate_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condom_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condom_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_sterilization_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_sterilization_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'metronidazole_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'metronidazole_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nb_prompt': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'oral_pills_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'oral_pills_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'oxytocine_available': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'oxytocine_provided': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_aggregatedrhcommoditiesreport_reports'", 'to': "orm['bolibana.Period']"}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'snisi_core.alert': {
            'Meta': {'object_name': 'Alert'},
            'alert_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'})
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
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['snisi_core.EpidemiologyReport']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'yellow_fever_case': ('django.db.models.fields.IntegerField', [], {}),
            'yellow_fever_death': ('django.db.models.fields.IntegerField', [], {})
        },
        'snisi_core.malariareport': {
            'Meta': {'unique_together': "(('period', 'entity', 'type'),)", 'object_name': 'MalariaReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_malariareport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_malariareport_reports'", 'to': "orm['bolibana.Entity']"}),
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
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_malariareport_reports'", 'to': "orm['bolibana.Period']"}),
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
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['snisi_core.MalariaReport']", 'null': 'True', 'blank': 'True'}),
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
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maternal_reported_in'", 'to': "orm['bolibana.Entity']"})
        },
        'snisi_core.rhcommoditiesreport': {
            'Meta': {'unique_together': "(('period', 'entity', 'type'),)", 'object_name': 'RHCommoditiesReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'amoxicillin_cap_gel': ('django.db.models.fields.IntegerField', [], {}),
            'amoxicillin_ij': ('django.db.models.fields.IntegerField', [], {}),
            'amoxicillin_suspension': ('django.db.models.fields.IntegerField', [], {}),
            'azithromycine_suspension': ('django.db.models.fields.IntegerField', [], {}),
            'azithromycine_tab': ('django.db.models.fields.IntegerField', [], {}),
            'benzathine_penicillin': ('django.db.models.fields.IntegerField', [], {}),
            'cefexime': ('django.db.models.fields.IntegerField', [], {}),
            'ceftriaxone_1000': ('django.db.models.fields.IntegerField', [], {}),
            'ceftriaxone_500': ('django.db.models.fields.IntegerField', [], {}),
            'clotrimazole': ('django.db.models.fields.IntegerField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_rhcommoditiesreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_services': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_rhcommoditiesreport_reports'", 'to': "orm['bolibana.Entity']"}),
            'ergometrine_tab': ('django.db.models.fields.IntegerField', [], {}),
            'ergometrine_vials': ('django.db.models.fields.IntegerField', [], {}),
            'family_planning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'female_condom': ('django.db.models.fields.IntegerField', [], {}),
            'female_sterilization': ('django.db.models.fields.IntegerField', [], {}),
            'folate': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implants': ('django.db.models.fields.IntegerField', [], {}),
            'injectable': ('django.db.models.fields.IntegerField', [], {}),
            'iron': ('django.db.models.fields.IntegerField', [], {}),
            'iron_folate': ('django.db.models.fields.IntegerField', [], {}),
            'iud': ('django.db.models.fields.IntegerField', [], {}),
            'magnesium_sulfate': ('django.db.models.fields.IntegerField', [], {}),
            'male_condom': ('django.db.models.fields.IntegerField', [], {}),
            'male_sterilization': ('django.db.models.fields.IntegerField', [], {}),
            'metronidazole': ('django.db.models.fields.IntegerField', [], {}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'oral_pills': ('django.db.models.fields.IntegerField', [], {}),
            'oxytocine': ('django.db.models.fields.IntegerField', [], {}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snisi_core_rhcommoditiesreport_reports'", 'to': "orm['bolibana.Period']"}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['snisi_core']
