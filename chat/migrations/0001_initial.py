# Generated by Django 3.1.2 on 2020-10-17 07:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('is_public', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('admins', models.ManyToManyField(blank=True, related_name='admins_room', to=settings.AUTH_USER_MODEL)),
                ('join_requests', models.ManyToManyField(blank=True, related_name='join_requests_room', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, related_name='members_room', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('sent_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_messages', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(default=40, on_delete=django.db.models.deletion.CASCADE, related_name='room_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
