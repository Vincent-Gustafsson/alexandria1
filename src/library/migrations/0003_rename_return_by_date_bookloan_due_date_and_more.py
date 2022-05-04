# Generated by Django 4.0.3 on 2022-04-07 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_bookloan_return_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookloan',
            old_name='return_by_date',
            new_name='due_date',
        ),
        migrations.AlterField(
            model_name='bookloan',
            name='return_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]