# Generated by Django 3.0.8 on 2020-09-02 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boardapp', '0002_auto_20200902_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardmodel',
            name='readtext',
            field=models.CharField(blank=True, default='testuser', max_length=200, null=True),
        ),
    ]
