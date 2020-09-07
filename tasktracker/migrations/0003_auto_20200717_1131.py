# Generated by Django 3.0.5 on 2020-07-17 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasktracker', '0002_auto_20200707_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('organizationid', models.CharField(max_length=70, primary_key=True, serialize=False)),
                ('organizationame', models.CharField(max_length=70, unique=True)),
                ('organizationmail', models.CharField(default='', max_length=70)),
                ('organizationlocation', models.CharField(default='', max_length=70)),
                ('organizationpin', models.CharField(default='', max_length=70)),
                ('organizationlogo', models.CharField(default='', max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('projectid', models.CharField(default='', max_length=70, primary_key=True, serialize=False)),
                ('projectname', models.CharField(default='', max_length=70, unique=True)),
                ('projectmail', models.CharField(default='', max_length=70)),
                ('projectlocation', models.CharField(default='', max_length=70)),
                ('projectpin', models.CharField(default='', max_length=70)),
                ('projectlogo', models.CharField(default='', max_length=70)),
                ('projecttype', models.CharField(default='', max_length=70)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AddField(
            model_name='user',
            name='medicalstatus',
            field=models.CharField(default='', max_length=70),
        ),
        migrations.AlterField(
            model_name='user',
            name='userid',
            field=models.CharField(max_length=70, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=70, unique=True),
        ),
        migrations.CreateModel(
            name='UserOrganizationProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='', max_length=70)),
                ('approvalstatus', models.CharField(default='', max_length=70)),
                ('organizationid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasktracker.Organization')),
                ('projectid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasktracker.Project')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasktracker.User')),
            ],
        ),
    ]