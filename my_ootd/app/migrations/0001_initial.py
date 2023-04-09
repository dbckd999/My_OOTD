# Generated by Django 4.1.7 on 2023-04-09 10:36

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
            name='UserClothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cloth_name', models.CharField(max_length=50)),
                ('cloth_var', models.CharField(max_length=30)),
                ('cloth_col_1', models.CharField(max_length=30)),
                ('cloth_col_2', models.CharField(max_length=30)),
                ('user_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
