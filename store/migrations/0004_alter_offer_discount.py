# Generated by Django 3.2.16 on 2023-02-13 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_order_expected_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='discount',
            field=models.PositiveIntegerField(max_length=12),
        ),
    ]
