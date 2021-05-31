# Generated by Django 3.2.3 on 2021-05-31 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manage_pokemons', '0010_auto_20210530_2349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pokemon',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='pokemon',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pokemons', to=settings.AUTH_USER_MODEL),
        ),
    ]
