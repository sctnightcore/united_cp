# Generated by Django 2.0.5 on 2018-05-04 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('unitedcp', '0003_auto_20170630_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPHighPeak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_users', models.IntegerField()),
                ('peak_date', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'cp_highest_peak',
            },
        ),
        migrations.CreateModel(
            name='PromoCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=128)),
                ('reward', models.IntegerField()),
                ('amount', models.IntegerField()),
            ],
            options={
                'db_table': 'cp_promo_codes',
            },
        ),
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'User Cart',
                'db_table': 'cp_user_cart',
            },
        ),
        migrations.AlterField(
            model_name='shop',
            name='item_bundle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='unitedcp.ShopBundles', verbose_name='Is bundle'),
        ),
        migrations.AddField(
            model_name='usercart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='unitedcp.Shop'),
        ),
        migrations.AddField(
            model_name='usercart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
