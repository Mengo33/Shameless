# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 18:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('link', models.CharField(max_length=100)),
                ('due_date', models.DateField()),
                ('replies_num', models.IntegerField(default=1)),
                ('replies_left', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_text', models.TextField(max_length=1000)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
                ('posted_at', models.DateField(blank=True, null=True)),
                ('reply_link', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Created'), (2, 'Checking'), (3, 'Rejected'), (4, 'Approved'), (5, 'Posted'), (6, 'Discarded')], default=1)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='campaigns.Campaign')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignUser',
            fields=[
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='campaigns.ProfileUser')),
            ],
        ),
        migrations.CreateModel(
            name='WriterUser',
            fields=[
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='campaigns.ProfileUser')),
            ],
        ),
        migrations.AddField(
            model_name='reply',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.WriterUser'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.CampaignUser'),
        ),
    ]
