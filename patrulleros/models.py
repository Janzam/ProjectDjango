from django.db import models
from crum import get_current_user
# Create your models here.

class Patrullero(models.Model):
    placa = models.CharField(max_length=20)
    unidad = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    conductor = models.CharField(max_length=100)
    latitud_actual = models.DecimalField(max_digits=9, decimal_places=6)
    longitud_actual = models.DecimalField(max_digits=9, decimal_places=6)
    ultimo_reporte = models.DateTimeField(blank=True, null=True)
    telefono_contacto = models.CharField(max_length=20, blank=True)
    estado_actual = models.CharField(
        max_length=20,
        choices=[
            ('disponible', 'Disponible'),
            ('en_mision', 'En misión'),
            ('fuera_servicio', 'Fuera de servicio')
        ],
        default='disponible'
    )

    creadopor = models.CharField(max_length=100, blank=True, null=True, editable=False)
    creadodate = models.DateTimeField(auto_now_add=True,null=True)
    editadopor = models.CharField(max_length=100, blank=True, null=True, editable=False)
    editadodate = models.DateTimeField(auto_now=True,null=True)
    eliminadopor = models.CharField(max_length=100, blank=True, null=True, editable=False)
    eliminadodate = models.DateTimeField(blank=True, null=True, editable=False)
    activo = models.BooleanField(default=True, verbose_name="Estado")

    class Meta:
        verbose_name = 'Patrullero'
        verbose_name_plural = 'Patrulleros'
        ordering = ['placa']

    def __str__(self):
        return self.placa

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        try:
            user = get_current_user()
            if self._state.adding:  # si estamos creando registro
                self.creadopor = user.username
            else:
                self.editadopor = user.username
        except:
            pass

        models.Model.save(self)

class AsignacionRespuesta(models.Model):
    ESTADO = (
        ('NUEVO', 'Nuevo'),
        ('EN_CURSO', 'En Curso'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    )

    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO)
    patrullero = models.ForeignKey(Patrullero, on_delete=models.PROTECT)
    reporte = models.ForeignKey('reportes.Reporte', on_delete=models.PROTECT)

    creadopor = models.CharField(max_length=100, blank=True, null=True, editable=False)
    creadodate = models.DateTimeField(auto_now_add=True,null=True)
    editadopor = models.CharField(max_length=100, blank=True, null=True, editable=False)
    editadodate = models.DateTimeField(auto_now=True,null=True)
    eliminadopor = models.CharField(max_length=100, blank=True, null=True, editable=False)
    eliminadodate = models.DateTimeField(blank=True, null=True, editable=False)
    activo = models.BooleanField(default=True, verbose_name="Estado")

    class Meta:
        verbose_name = 'Asignación de Respuesta'
        verbose_name_plural = 'Asignaciones de Respuesta'
        ordering = ['fecha_asignacion']

    def __str__(self):
        return f"{self.patrullero} - {self.reporte}"

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        try:
            user = get_current_user()
            if self._state.adding:  # si estamos creando registro
                self.creadopor = user.username
            else:
                self.editadopor = user.username
        except:
            pass

        models.Model.save(self)