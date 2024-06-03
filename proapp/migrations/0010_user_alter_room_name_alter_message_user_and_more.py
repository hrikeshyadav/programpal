# Generated by Django 5.0.3 on 2024-05-29 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proapp', '0009_alter_message_user_alter_room_host_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('bio', models.TextField(null=True)),
                ('avatar', models.ImageField(default='avatar.svg', null=True, upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proapp.user'),
        ),
        migrations.AlterField(
            model_name='room',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='proapp.user'),
        ),
        migrations.AlterField(
            model_name='room',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', to='proapp.user'),
        ),
    ]
