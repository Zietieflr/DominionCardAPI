# Generated by Django 3.0 on 2019-12-18 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=128, null=True)),
                ('card_name', models.CharField(max_length=64, null=True)),
                ('set_num', models.IntegerField(null=True)),
                ('set_name', models.CharField(max_length=32, null=True)),
                ('type', models.CharField(max_length=64, null=True)),
                ('cost', models.CharField(max_length=4, null=True)),
                ('card_text', models.TextField(max_length=1024, null=True)),
            ],
        ),
    ]
