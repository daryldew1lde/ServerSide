# Generated by Django 5.0 on 2024-02-13 08:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='arriveeretouremploye',
            options={'ordering': ['-date', '-heure_arrive']},
        ),
        migrations.CreateModel(
            name='DetailsAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('heure', models.TimeField(blank=True, null=True)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details_access', to='webserver.employe')),
            ],
            options={
                'ordering': ['-date', 'heure'],
            },
        ),
    ]
