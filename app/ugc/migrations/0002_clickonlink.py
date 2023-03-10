# Generated by Django 4.1.6 on 2023-02-13 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickOnLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.TextField(verbose_name='IP address')),
                ('click_at', models.DateTimeField(verbose_name='Click at that datetime')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.link', verbose_name='Link')),
            ],
        ),
    ]
