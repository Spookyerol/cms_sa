# Generated by Django 3.2.5 on 2022-01-24 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0005_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CRM.user'),
        ),
    ]
