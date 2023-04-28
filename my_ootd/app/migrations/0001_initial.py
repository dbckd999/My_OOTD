# Generated by Django 4.1.7 on 2023-04-28 13:24

import app.models
import colorfield.fields
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SevUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nickname', models.CharField(default='init_nick', max_length=20, verbose_name='nickname')),
                ('is_male', models.BooleanField(verbose_name='isMale')),
                ('phone', models.CharField(max_length=11, validators=[app.models.validate_phone_number], verbose_name='phone')),
                ('skin_color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserClothes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, null=True)),
                ('cloth_name', models.CharField(max_length=50)),
                ('cloth_var', models.CharField(max_length=30)),
                ('cloth_col_1', models.CharField(max_length=30)),
                ('cloth_col_2', models.CharField(max_length=30)),
                ('cloth_img', models.ImageField(blank=True, null=True, upload_to=app.models.UserClothes.upload_cloth_img)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sevuser')),
            ],
        ),
    ]
