# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class Historical(models.Model):
    sid = models.OneToOneField('Stocks', models.DO_NOTHING, db_column='sid', primary_key=True)
    dat = models.DateField()
    open_value = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    close_value = models.FloatField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historical'
        unique_together = (('sid', 'dat'),)


class RealTime(models.Model):
    sid = models.OneToOneField('Stocks', models.DO_NOTHING, db_column='sid', primary_key=True)
    dat = models.DateField()
    tim = models.TimeField()
    open_value = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    close_value = models.FloatField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'real_time'
        unique_together = (('sid', 'dat', 'tim'),)


class Stocks(models.Model):
    sid = models.IntegerField(primary_key=True)
    ticker = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocks'


class Thresholds(models.Model):
    ticker = models.CharField(primary_key=True, max_length=10)
    username = models.CharField(max_length=20)
    price = models.FloatField(blank=True, null=True)
    threshold = models.FloatField(blank=True, null=True)
    satisfied = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'thresholds'
        unique_together = (('ticker', 'username'),)

