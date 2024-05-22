# inventory/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SubWarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('warehouse', models.ForeignKey(on_delete=models.CASCADE, to='inventory.Warehouse')),
            ],
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='subwarehouse',
            field=models.ForeignKey(null=True, on_delete=models.CASCADE, to='inventory.SubWarehouse'),
        ),
        migrations.AddField(
            model_name='inventoryitem',
            name='warehouse',
            field=models.ForeignKey(null=True, on_delete=models.CASCADE, to='inventory.Warehouse'),
        ),
    ]
