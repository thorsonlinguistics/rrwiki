# Generated by Django 3.0.6 on 2020-12-09 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strata', '0004_auto_20201208_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='character',
            name='race',
            field=models.CharField(blank=True, default='Dwarf', max_length=100),
        ),
    ]
