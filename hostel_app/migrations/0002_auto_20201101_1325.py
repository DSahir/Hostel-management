# Generated by Django 2.2.6 on 2020-11-01 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostel_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='branch',
        ),
        migrations.AddField(
            model_name='hostel',
            name='b_phone_no',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='hostel',
            name='totroom',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mess',
            name='mess_name',
            field=models.CharField(default='COEP-Mess', max_length=25),
        ),
        migrations.AddField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='student',
            name='hostel_b',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hostel_app.Hostel'),
        ),
        migrations.AddField(
            model_name='student',
            name='own_vehicle',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default=None, max_length=1),
        ),
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.OneToOneField(max_length=7, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='vehicle',
            fields=[
                ('vehicleno', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('licence', models.BigIntegerField(null=True)),
                ('h_id', models.ForeignKey(max_length=7, on_delete=django.db.models.deletion.CASCADE, to='hostel_app.Student')),
            ],
        ),
        migrations.CreateModel(
            name='CollegeInfo',
            fields=[
                ('mis', models.CharField(db_column='MIS', max_length=7, primary_key=True, serialize=False, unique=True)),
                ('email', models.CharField(db_column='EMAIL', max_length=50, null=True)),
                ('phone_no', models.BigIntegerField(db_column='PHONE_NO', null=True)),
                ('batchof', models.CharField(db_column='BATCH_OF', max_length=4)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hostel_app.Branch')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='personal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hostel_app.CollegeInfo'),
        ),
    ]
