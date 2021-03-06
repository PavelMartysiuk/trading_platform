# Generated by Django 2.2.2 on 2020-09-07 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('buy', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('sell', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Currency')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_quantity', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('order_type', models.PositiveSmallIntegerField(choices=[('price', 'PRICE'), ('quntity', 'QUANTITY')])),
                ('transaction_type', models.PositiveSmallIntegerField(choices=[(0, 'limit'), (1, 'market')])),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Item')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('reversed_quantity', models.IntegerField()),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Item')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'inventory',
                'unique_together': {('user', 'item')},
            },
        ),
    ]
