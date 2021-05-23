# Generated by Django 3.1.6 on 2021-03-04 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20210303_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='grade',
            field=models.CharField(choices=[('ZNO', 'ЗНО'), ('11', '11'), ('10', '10'), ('9', '9'), ('8', '8'), ('7', '7'), ('6', '6'), ('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')], default='ZNO', max_length=15),
        ),
        migrations.AlterField(
            model_name='course',
            name='type_grade',
            field=models.CharField(choices=[('ZNO', 'ЗНО'), ('in-depth', 'Поглиблене вивчення'), ('standart', 'Рівень стандарту')], default='ZNO', max_length=15),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='grade',
            field=models.CharField(choices=[('ZNO', 'ЗНО'), ('11', '11'), ('10', '10'), ('9', '9'), ('8', '8'), ('7', '7'), ('6', '6'), ('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')], default='ZNO', max_length=15),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='type_grade',
            field=models.CharField(choices=[('ZNO', 'ЗНО'), ('in-depth', 'Поглиблене вивчення'), ('standart', 'Рівень стандарту')], default='ZNO', max_length=15),
        ),
        migrations.AlterField(
            model_name='topic',
            name='grade',
            field=models.CharField(choices=[('ZNO', 'ЗНО'), ('11', '11'), ('10', '10'), ('9', '9'), ('8', '8'), ('7', '7'), ('6', '6'), ('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')], default='ZNO', max_length=15),
        ),
        migrations.AlterField(
            model_name='topic',
            name='type_grade',
            field=models.CharField(choices=[('ZNO', 'ЗНО'), ('in-depth', 'Поглиблене вивчення'), ('standart', 'Рівень стандарту')], default='ZNO', max_length=15),
        ),
    ]
