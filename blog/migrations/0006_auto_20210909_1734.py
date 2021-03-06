# Generated by Django 3.2.6 on 2021-09-09 14:34

import blog.utilities
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to=blog.utilities.get_timestamp_path, verbose_name='Изображение'),
        ),
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=blog.utilities.get_timestamp_path, verbose_name='Изображение')),
                ('bb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Статьи')),
            ],
            options={
                'verbose_name': 'Дополнительная илюстрация',
                'verbose_name_plural': 'Дополнительные иллюстрации',
            },
        ),
    ]
