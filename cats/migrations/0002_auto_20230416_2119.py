# Generated by Django 3.2 on 2023-04-16 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='color',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterModelTable(
            name='cat',
            table='cats',
        ),
    ]