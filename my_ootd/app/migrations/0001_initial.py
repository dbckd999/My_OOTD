# Generated by Django 3.2.15 on 2023-04-05 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('sign_up_date', models.DateTimeField(verbose_name='sing up date')),
                ('nickname', models.CharField(max_length=30)),
            ],
        ),
    ]
