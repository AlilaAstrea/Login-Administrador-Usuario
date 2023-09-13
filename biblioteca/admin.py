from django.contrib import admin

# Register your models here.

from biblioteca.models import Usuario, Idioma, Genero, Biblioteca, Historial

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_usuario', 'password_usuario']

class IdiomaAdmin(admin.ModelAdmin):
    list_display = ['id', 'lenguaje']

class GeneroAdmin(admin.ModelAdmin):
    list_display = ['id', 'categoria']

class BibliotecaAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo','nombre','numero','literatura','idioma','codigo','genero','editorial']

class HistorialAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'descripcion_historial', 'tabla_afectada_historial', 'fecha_hora_historial']



admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Idioma, IdiomaAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Biblioteca, BibliotecaAdmin)
admin.site.register(Historial, HistorialAdmin)


