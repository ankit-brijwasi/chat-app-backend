# Generated by Django 3.1.2 on 2020-10-17 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(default=40, on_delete=django.db.models.deletion.CASCADE, related_name='room_messages', to='chat.room'),
        ),
    ]
