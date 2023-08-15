# Generated by Django 3.1 on 2021-06-15 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0032_user_model'),
        ('ideas_bugs', '0006_auto_20210407_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bug',
            name='person',
        ),
        migrations.RemoveField(
            model_name='bugstatushistory',
            name='person',
        ),
        migrations.RemoveField(
            model_name='idea',
            name='person',
        ),
        migrations.RemoveField(
            model_name='ideastatushistory',
            name='person',
        ),
        migrations.AddField(
            model_name='bug',
            name='customer_person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='talent.person'),
        ),
        migrations.AddField(
            model_name='bugstatushistory',
            name='customer_person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='talent.person'),
        ),
        migrations.AddField(
            model_name='idea',
            name='customer_person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='talent.person'),
        ),
        migrations.AddField(
            model_name='ideastatushistory',
            name='customer_person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='talent.person'),
        ),
    ]
