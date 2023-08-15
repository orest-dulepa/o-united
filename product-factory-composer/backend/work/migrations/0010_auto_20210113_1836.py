# Generated by Django 3.1 on 2021-01-13 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0009_tag_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiative',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='depend_on',
            field=models.ManyToManyField(blank=True, null=True, related_name='_task_depend_on_+', to='work.Task'),
        ),
    ]