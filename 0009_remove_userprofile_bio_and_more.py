# Generated by Django 5.2 on 2025-05-08 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0008_rename_created_at_interestresult_timestamp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='other_graduation_stream',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
