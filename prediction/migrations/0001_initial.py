# Generated by Django 4.1.4 on 2024-09-22 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Roadmap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='roadmaps/images/')),
                ('pdf', models.FileField(upload_to='roadmaps/pdfs/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
