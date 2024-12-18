# Generated by Django 4.2.17 on 2024-12-18 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('photo_small', models.BinaryField(blank=True, null=True)),
                ('photo_medium', models.BinaryField(blank=True, null=True)),
                ('photo_large', models.BinaryField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab4_sql_app.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab4_sql_app.product')),
            ],
        ),
    ]
