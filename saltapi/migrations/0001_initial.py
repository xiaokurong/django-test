# Generated by Django 2.0 on 2019-06-14 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OffenCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ServerGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='ServerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salt_name', models.CharField(max_length=25)),
                ('server_name', models.CharField(max_length=25, null=True)),
                ('cpu', models.CharField(max_length=50, null=True)),
                ('cpu_core', models.SmallIntegerField(null=True)),
                ('system', models.CharField(max_length=50, null=True)),
                ('ip_addr', models.GenericIPAddressField(null=True, protocol='ipv4')),
                ('ram', models.IntegerField(null=True)),
                ('disk', models.IntegerField(null=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('group_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='saltapi.ServerGroup')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=25)),
                ('user_cnname', models.CharField(max_length=25, null=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('user_pass', models.CharField(max_length=25)),
                ('user_email', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPriv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priv_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_priv_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='saltapi.UserPriv'),
        ),
    ]
