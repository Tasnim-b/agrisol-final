# Generated by Django 5.2 on 2025-04-23 19:58

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actionneur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('ventilateur', 'Ventilateur'), ('humidificateur', 'Humidificateur'), ('pompe', 'Pompe')], max_length=20)),
                ('nomActionneur', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Agriculteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mot_de_passe', models.CharField(max_length=255)),
                ('telephone', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Capteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('temperature', 'Température'), ('humidite', 'Humidité'), ('ph', 'pH'), ('co2', 'CO2'), ('niveau_eau', "Niveau d'eau"), ('lumiere', 'Lumière')], max_length=20)),
                ('nomCapteur', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Intervalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min', models.FloatField()),
                ('max', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Culture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomCulture', models.CharField(max_length=255)),
                ('date_creation', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('mesures_en_temps_reel', models.JSONField(default=dict)),
                ('actionneurs', models.ManyToManyField(to='dashboard.actionneur')),
                ('agriculteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.agriculteur')),
                ('capteurs', models.ManyToManyField(to='dashboard.capteur')),
            ],
        ),
        migrations.CreateModel(
            name='Mesure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('valeurs', models.JSONField()),
                ('culture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.culture')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Alerte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_parametre', models.CharField(max_length=50)),
                ('valeur', models.FloatField()),
                ('seuil_min', models.FloatField(blank=True, null=True)),
                ('seuil_max', models.FloatField(blank=True, null=True)),
                ('message', models.CharField(max_length=255)),
                ('niveau', models.CharField(choices=[('faible', 'Faible'), ('modéré', 'Modéré'), ('critique', 'Critique')], default='modéré', max_length=20)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('mesure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.mesure')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Plante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('co2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='co2_plante', to='dashboard.intervalle')),
                ('humidite', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='humidite_plante', to='dashboard.intervalle')),
                ('lumiere', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lumiere_plante', to='dashboard.intervalle')),
                ('niveau_eau', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='niveau_eau_plante', to='dashboard.intervalle')),
                ('ph', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ph_plante', to='dashboard.intervalle')),
                ('temperature', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='temperature_plante', to='dashboard.intervalle')),
            ],
        ),
        migrations.AddField(
            model_name='culture',
            name='plante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.plante'),
        ),
        migrations.AddIndex(
            model_name='mesure',
            index=models.Index(fields=['culture', 'timestamp'], name='dashboard_m_culture_9da06c_idx'),
        ),
        migrations.AddIndex(
            model_name='alerte',
            index=models.Index(fields=['type_parametre', 'niveau'], name='dashboard_a_type_pa_13fd02_idx'),
        ),
    ]
