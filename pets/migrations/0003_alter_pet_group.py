# Generated by Django 4.1.7 on 2023-04-10 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
        ('pets', '0002_alter_pet_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='pets', to='groups.group'),
        ),
    ]
