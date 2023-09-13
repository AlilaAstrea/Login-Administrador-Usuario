from django.db import models

# Create your models here.


class Usuario(models.Model):
    nombre_usuario = models.TextField(max_length=15)
    password_usuario = models.TextField(max_length=15)
    
    def __str__(self):
        return str(self.nombre_usuario)
    
##--------------------------------------------------------------------##

class Idioma(models.Model):                                           ## Combo1
    lenguaje = models.TextField(max_length=50)

    def __str__(self):
        return str(self.lenguaje)
    

class Genero(models.Model):                                           ## Combo2
    categoria = models.TextField(max_length=50)

    def __str__(self):
        return str(self.categoria)

##--------------------------------------------------------------------##

class Biblioteca(models.Model):
    titulo = models.TextField(max_length=50)
    nombre = models.TextField(max_length=50)
    numero = models.IntegerField(null=False)
    literatura = models.TextField(max_length=20)
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)
    codigo = models.IntegerField(null=False)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    editorial = models.TextField(max_length=100)

    def __str__(self):
        return str(self.titulo) + " - " + str(self.nombre) + " - " + str(self.numero) + " - " + str(self.literatura) + " - " + str(self.idioma) + " - " + str(self.codigo) + " - " + str(self.genero) + " - " + str(self.editorial)

    

##--------------------------------------------------------------------##

class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion_historial = models.TextField(max_length=200)
    tabla_afectada_historial = models.TextField(max_length=50)
    fecha_hora_historial = models.DateTimeField()

