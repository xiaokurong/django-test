# Generated by Django 2.0 on 2019-06-20 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saltapi', '0003_auto_20190620_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='servergroup',
            name='remark',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
