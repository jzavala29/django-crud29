from django.db import models
from django.db.models import Sum, Count
# Create your models here.

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Clase(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre

class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Asistencia(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha = models.DateField()
    presente = models.BooleanField(default=False)

    class Meta:
        unique_together = ('estudiante', 'clase', 'fecha')

    def __str__(self):
        return f"Asistencia de {self.estudiante} el {self.fecha}"

class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    tarea = models.CharField(max_length=100)
    nota = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Calificación de {self.estudiante} en {self.clase}: {self.nota}"

class Reporte(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    calificaciones = models.ManyToManyField(Calificacion, related_name='reportes')
    promedio = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    estado = models.CharField(max_length=20, default="Reprueba")
    
    
    class Meta:
        unique_together = ('estudiante', 'clase')
    
    def calcular_promedio(self):
        calificaciones_data = self.calificaciones.aggregate(
            total_notas=Sum('nota'),
            total_calificaciones=Count('id')
        )
        
        total_notas = calificaciones_data['total_notas'] or 0.0
        total_calificaciones = calificaciones_data['total_calificaciones'] or 0
        
        if total_calificaciones > 0:
            self.promedio = round(total_notas / total_calificaciones, 2)
            self.estado = "Aprueba" if self.promedio >= 7 else "Reprueba"
    
    def __str__(self):
        return f"Reporte de {self.estudiante} en {self.clase} - Promedio: {self.promedio} ({self.estado})"




