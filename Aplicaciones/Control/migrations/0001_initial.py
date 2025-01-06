# Generated by Django 5.1.3 on 2025-01-05 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('matricula', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('estudiante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Control.estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarea', models.CharField(max_length=100)),
                ('nota', models.DecimalField(decimal_places=2, max_digits=5)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Control.clase')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Control.estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('presente', models.BooleanField(default=False)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Control.clase')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Control.estudiante')),
            ],
            options={
                'unique_together': {('estudiante', 'clase', 'fecha')},
            },
        ),
    ]
