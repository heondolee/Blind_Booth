# Generated by Django 4.2 on 2023-05-03 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blind', '0005_alter_timebox_timemin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timebox',
            name='man',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='man_timebox_set', to='blind.person'),
        ),
        migrations.AlterField(
            model_name='timebox',
            name='woman',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='woman_timebox_set', to='blind.person'),
        ),
    ]