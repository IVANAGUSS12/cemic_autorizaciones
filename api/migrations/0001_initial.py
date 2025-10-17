from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.SlugField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('slug', models.SlugField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('specialty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.specialty')),
            ],
            options={'ordering': ['name'], 'unique_together': {('name', 'specialty')}},
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=160)),
                ('dni', models.CharField(blank=True, default='', max_length=32)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('telefono', models.CharField(blank=True, default='', max_length=64)),
                ('cobertura', models.CharField(blank=True, default='', max_length=120)),
                ('medico', models.CharField(blank=True, default='', max_length=160)),
                ('observaciones', models.TextField(blank=True, default='')),
                ('fecha_cx', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('Pendiente','Pendiente'),('Solicitado','Solicitado'),('Rechazado por cobertura','Rechazado por cobertura'),('Autorizado','Autorizado'),('Autorizado material pendiente','Autorizado material pendiente')], default='Pendiente', max_length=48)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bucket_path', models.CharField(blank=True, default='', max_length=300)),
                ('folder_url', models.URLField(blank=True, default='')),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.sector')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('orden','orden'),('dni','dni'),('credencial','credencial'),('materiales','materiales'),('otro','otro')], default='otro', max_length=24)),
                ('file', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('external_url', models.URLField(blank=True, default='')),
                ('name', models.CharField(blank=True, default='', max_length=140)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='api.patient')),
            ],
        )
    ]
