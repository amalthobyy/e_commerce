# Generated by Django 5.0.7 on 2024-09-04 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_ordermain_discount_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermain',
            name='final_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
