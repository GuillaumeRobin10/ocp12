# Generated by Django 3.2.8 on 2021-10-21 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EpicEventscrm', '0002_alter_client_date_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrat',
            name='date_signature',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contrat',
            name='date_updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
