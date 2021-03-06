# Generated by Django 2.0.2 on 2018-06-15 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_goods'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, '已付款'), (1, '待付款'), (2, '待评价')])),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Shoppingcar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
                ('realname', models.CharField(max_length=32)),
            ],
        ),
        migrations.DeleteModel(
            name='News',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
        migrations.AddField(
            model_name='goods',
            name='shangpintupian',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shoppingcar',
            name='goods',
            field=models.ForeignKey(on_delete=True, to='app.Goods'),
        ),
        migrations.AddField(
            model_name='shoppingcar',
            name='user',
            field=models.ForeignKey(on_delete=True, to='app.User'),
        ),
        migrations.AddField(
            model_name='order',
            name='goods',
            field=models.ForeignKey(on_delete=True, to='app.Goods'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=True, to='app.User'),
        ),
    ]
