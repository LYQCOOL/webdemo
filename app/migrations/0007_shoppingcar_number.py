# Generated by Django 2.0.2 on 2018-06-19 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180617_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcar',
            name='number',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]
