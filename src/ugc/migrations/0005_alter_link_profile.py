# Generated by Django 4.1.6 on 2023-02-08 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0004_remove_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.profile', verbose_name='Profile'),
        ),
    ]