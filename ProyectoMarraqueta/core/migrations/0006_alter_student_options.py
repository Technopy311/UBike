# Generated by Django 5.0.3 on 2024-04-25 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_academic_connection_alter_external_connection_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="student",
            options={
                "verbose_name": "Estudiante",
                "verbose_name_plural": "Estudiantes",
            },
        ),
    ]