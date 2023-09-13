from django.shortcuts import render
from biblioteca.models import Usuario, Genero, Idioma, Biblioteca, Historial
from datetime import datetime

#-- nuevo  import--#
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from biblioteca.serializers import BibliotecaSerializer, UsuarioSerializer

# Create your views here.

#----------------------------------------------------------------#
def mostrarIndex(request):
    return render(request, 'index.html')

#----------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------funciones Eva4 Api Rest-------------------------------------#

def obtenerBibliotecas(request):
    bli = Biblioteca.objects.all()
    datos = { " bli " : list(bli.values('id','titulo','nombre','numero','literatura','idioma','codigo','genero','editorial'))}
    return JsonResponse(datos)

def obtenerUsuarios(request):
    usu = Usuario.objects.all()
    datos = {"usu" : list(usu.values('id', 'nombre_usuario','password_usuario'))}
    return JsonResponse(datos)

#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#

#Peticion get / post

@api_view(['GET', 'POST'])
def biblioteca_list(request):
    if request.method == 'GET':
        bli = Biblioteca.objects.all()
        ser = BibliotecaSerializer(bli, many=True)
        return Response(ser.data)
    
    if request.method == 'POST':
        ser = BibliotecaSerializer(data= request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET', 'POST'])
def usuario_list(request):
    if request.method == 'GET':
        usu = Usuario.objects.all()
        ser = UsuarioSerializer(usu, many=True)
        return Response(ser.data)
    
    if request.method == 'POST':
        ser = UsuarioSerializer(data= request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        

#---------------------------------------------------------------------------------------#

@api_view(['GET','PUT','DELETE'])
def biblioteca_detail(request,id):
    try:
        bli = Biblioteca.objects.get(id=id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        ser = BibliotecaSerializer(bli)
        return Response(ser.data)
    
    if request.method == 'PUT':
        ser = BibliotecaSerializer(bli, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        bli.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET','PUT','DELETE'])
def usuario_detail(request,id):
    try:
        usu = Usuario.objects.get(id=id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        ser = UsuarioSerializer(usu)
        return Response(ser.data)
    
    if request.method == 'PUT':
        ser = UsuarioSerializer(usu, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        usu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

##---------------------------------------------------------------##
##---------------------------------------------------------------##


def iniciarSesion(request):
    if request.method == "POST":
        nom = request.POST["txtusu"]
        pas = request.POST["txtpas"]

        comprobarLogin = Usuario.objects.filter(nombre_usuario=nom, password_usuario=pas).values()
        # comprueba estado de sesion true 
        if comprobarLogin:
            request.session["estadoSesion"] = True
            request.session["idUsuario"] = comprobarLogin[0]['id'] # obtengo el primer valor de comprobarLogin que seria el primer valor de usuario ( admin )
            request.session["nomUsuario"] = nom.upper() # asigna el valor del nombre de usuario en letras mayúsculas 

            datos = {
                'nomUsuario' : nom.upper()
            }

            # registro de historial al iniciar sesión
            descripcion = "Inicio de Sesión"   # al iniciar sesión entrego el mensaje 
            tabla = ""    # no especifica que tabla fue actualizada ya que se comprueba usuario, pero deja en blanco en historial
            fechayhora = datetime.now() # entrega el dato de la fecha y hora actual.
            usuario = request.session["idUsuario"] # entrego si fue usuario 0 = admin o 1 = operador, etc.
            his = Historial(   # guardo los datos en la tabla historial
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
            his.save()

            # pregunto si es Admin -> menu_admin, de lo contrario se dirige al usuario
            if nom.upper() == "ADMIN":
                return render(request, 'menu_administrador.html', datos) # envio aparte el nombre si es ADMIN / OPERADOR
            else:
                return render(request, 'menu_usuario.html', datos)
        else:
            datos = {'r2' : 'Problema con su Usuario y/o Contraseña'}
            return render(request, 'index.html', datos)  # manda mensaje de error y devuelve al index.html ( inicio de sesion )

    else:
        datos = {'r2' : 'Hay un error, no se puede acceder a tu solicitud'}
        return render(request, 'index.html, datos')
    
    ## return render(request, 'menu_administrador.html') ## la ubicación solo es para dejar marcada la funcion a utilizar por el momento


def cerrarSesion(request):  # Si cierra sesion crea un registro en historial, de lo contrario solo devuelve al index.html
    try:
        nom = request.session['nomUsuario']
        del request.session['nomUsuario']
        del request.session['estadoSesion']

        # registro de historial
        descripcion = "Cierre de Sesión"   # al iniciar sesión entrego el mensaje 
        tabla = ""    # no especifica que tabla fue actualizada ya que se comprueba usuario, pero deja en blanco en historial
        fechayhora = datetime.now() # entrega el dato de la fecha y hora actual.
        usuario = request.session["idUsuario"] # entrego si fue usuario 0 = admin o 1 = operador, etc.
        his = Historial(   # guardo los datos en la tabla historial
            descripcion_historial=descripcion,
            tabla_afectada_historial=tabla,
            fecha_hora_historial=fechayhora,
            usuario_id=usuario
        )
        his.save()

        return render(request, 'index.html')
    except:
        return render(request, 'index.html')

##---------------------------------------------------------------##
##------------------FUNCIONES DE ADMIN---------------------------##
##---------------------------------------------------------------##


def mostrarMenuAdmin(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper()=="ADMIN":
            datos = {
                'nomUsuario' : request.session["nomUsuario"]
            }
            return render(request, 'menu_administrador.html', datos)
        else:
            datos = {
                'r2' : 'No Tienes Privilegios para Acceder a la plantilla administrador'
            }
            return render(request, 'index.html', datos)
    else:
        datos = {
            'r2' : 'Debes Iniciar Sesión para Acceder al Menú de Administrador'
        }
        return render(request, 'index.html', datos)


    ##  return render(request, "menu_administrador.html")



##---------------------------------------------------------------##
##---------------------------------------------------------------##

def mostrarFormRegistroIdiomas(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":

            idio = Idioma.objects.all().values().order_by("lenguaje")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'idio' : idio 
            }
            return render(request, 'form_registro_idiomas.html', datos)
        else:

            datos = {
                'r' : 'No tienes Permisos para estar crear Registros'
            }
            return render(request, 'index.html', datos)
    else:
        datos = {
            'r' : 'Debes Iniciar Sesión para acceder'
        }
        return render(request, 'index.html', datos)


    ##  return render(request, 'form_registro_idiomas.html')



def mostrarFormRegistroGeneros(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":

            gene = Genero.objects.all().values().order_by("categoria")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'gene' : gene 
            }
            return render(request, 'form_registro_generos.html', datos)
        else:

            datos = {
                'r' : 'No tienes Permisos para estar crear Registros'
            }
            return render(request, 'index.html', datos)
    else:
        datos = {
            'r' : 'Debes Iniciar Sesión para acceder'
        }
        return render(request, 'index.html', datos)


    ##  return render(request, 'form_registro_generos.html')


##---------------------------------------------------------------##
##---------------------------------------------------------------##

def registrarIdioma(request):
    if request.method == "POST":
        nom = request.POST["txtidio"].upper()

        comprobarIdioma = Idioma.objects.filter(lenguaje=nom)
        if comprobarIdioma:

            idio = Idioma.objects.all().values().order_by("lenguaje")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'idio' : idio,
                'r2' : 'El Idioma ('+nom.upper()+') Ya Existe'
            }
            return render(request, 'form_registro_idiomas.html', datos)
        else:
            # registra el idioma
            idio = Idioma(lenguaje=nom)
            idio.save()

            # registro de historial
            descripcion = "Inserción realizada ("+nom.lower()+")"  
            tabla = "Idioma"    
            fechayhora = datetime.now() 
            usuario = request.session["idUsuario"] 
            his = Historial(   
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
            his.save()

            #se listan los idiomas
            idio = Idioma.objects.all().values().order_by("lenguaje")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'idio' : idio,
                'r' : 'Idioma ('+nom+') Agregado :D'
            }
            return render(request, 'form_registro_idiomas.html', datos)
    else:

        idio = Idioma.objects.all().values()

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'idio' : idio,
            'r2' : 'Debes oprimir "Registrar Idioma" si deseas registrarlo :('
        }
        return render(request, 'form_registro_idiomas.html', datos)
        
    ##  pass

def registrarGenero(request):
    if request.method == "POST":
        nom = request.POST["txtgene"].upper()

        comprobarGenero = Genero.objects.filter(categoria=nom)
        if comprobarGenero:

            gene = Genero.objects.all().values().order_by("categoria")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'gene' : gene,
                'r2' : 'El Genero Literario ('+nom.upper()+') Ya Existe'
            }
            return render(request, 'form_registro_generos.html', datos)
        else:
            # registra el genero
            gene = Genero(categoria=nom)
            gene.save()

            # registro de historial
            descripcion = "Inserción realizada ("+nom.lower()+")"   
            tabla = "Genero"    
            fechayhora = datetime.now() 
            usuario = request.session["idUsuario"] 
            his = Historial(  
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
            his.save()

            #se listan los idiomas
            gene = Genero.objects.all().values().order_by("categoria")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'gene' : gene,
                'r' : 'Genero Literario ('+nom+') Agregado :D'
            }
            return render(request, 'form_registro_generos.html', datos)
    else:

        gene = Genero.objects.all().values()

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'gene' : gene,
            'r2' : 'Debes oprimir "Registrar Genero" si deseas registrarlo :('
        }
        return render(request, 'form_registro_idiomas.html', datos)

    ##  pass

##---------------------------------------------------------------##
##---------------------------------------------------------------##

def mostrarFormModificarIdioma(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:

            encontrado = Idioma.objects.get(id=id)

            idio = Idioma.objects.all().values().order_by("lenguaje")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'encontrado' : encontrado,
                'idio' : idio
            }
            return render(request, 'form_modificar_idiomas.html', datos)
        
        else:

            datos = {
                'r' : 'Debes Iniciar Sesión para acceder'
            }
            return render(request, 'index.html', datos)
    
    except:
        
        idio = Idioma.objects.all().values().order_by("lenguaje")
        
        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'idio' : idio,
            'r2' : 'El ID ('+str(id)+') No Existe. No puedes actualizarlo.. Schrödinger'
        }
        return render(request, 'form_registro_idiomas.html', datos)


    ## pass

def mostrarFormModificarGenero(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:

            encontrado = Genero.objects.get(id=id)

            gene = Genero.objects.all().values().order_by("categoria")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'encontrado' : encontrado,
                'gene' : gene
            }
            return render(request, 'form_modificar_generos.html', datos)
        
        else:

            datos = {
                'r' : 'Debes Iniciar Sesión para acceder'
            }
            return render(request, 'index.html', datos)
    
    except:
        
        gene = Genero.objects.all().values().order_by("categoria")
        
        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'gene' : gene,
            'r2' : 'El ID ('+str(id)+') No Existe. No puedes actualizarlo.. Schrödinger'
        }
        return render(request, 'form_registro_generos.html', datos)


        ## pass

##---------------------------------------------------------------##
##---------------------------------------------------------------##

def actualizarIdioma(request, id):
    try:
        nom = request.POST['txtidio'].upper()

        idio = Idioma.objects.get(id=id)
        idio.lenguaje = nom
        idio.save()

        # registro de historial
        descripcion = "Modificación realizada ("+nom.lower()+")"  
        tabla = "Idioma"    
        fechayhora = datetime.now() 
        usuario = request.session["idUsuario"] 
        his = Historial(  
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
        his.save()

        idio = Idioma.objects.all().values().order_by("lenguaje")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'idio' : idio,
            'r' :"Felicidades Schrödinger, modificaste la anomalía"
        }

        return render(request, 'form_registro_idiomas.html', datos)
    except:
        
        idio = Idioma.objects.all().values().order_by("lenguaje")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'idio' : idio,
            'r2' : "El ID ("+str(id)+") No Existe. No puedes actualizarlo.. Schrödinger",
            
        }

        return render(request, 'form_registro_idiomas.html', datos)



def actualizarGenero(request, id):
    try:
        nom = request.POST['txtgene'].upper()

        gene = Genero.objects.get(id=id)
        gene.categoria = nom
        gene.save()

        # registro de historial
        descripcion = "Modificación realizada ("+nom.lower()+")"  
        tabla = "Genero"    
        fechayhora = datetime.now() 
        usuario = request.session["idUsuario"] 
        his = Historial(  
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
        his.save()

        gene = Genero.objects.all().values().order_by("categoria")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'gene' : gene,
            'r' :"Felicidades Schrödinger, modificaste la anomalía"
        }

        return render(request, 'form_registro_generos.html', datos)
    except:
        
        gene = Genero.objects.all().values().order_by("categoria")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'gene' : gene,
            'r2' : "El ID ("+str(id)+") No Existe. No puedes actualizarlo.. Schrödinger",
            
        }

        return render(request, 'form_registro_generos.html', datos)
    
    ## pass

##---------------------------------------------------------------##
##---------------------------------------------------------------##

def eliminarIdioma(request, id):
    try:
        
        idio = Idioma.objects.get(id=id)
        nom = idio.lenguaje
        idio.delete()


        # se registra en la tabla historial.
        descripcion = "Eliminación realizada ("+nom.lower()+")"
        tabla = "Idioma"
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(  
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
        his.save()


        idio = Idioma.objects.all().values().order_by("lenguaje")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'idio':idio,
            'r' : "El idioma fue Eliminado Correctamente!!"
        }

        return render(request, "form_registro_idiomas.html", datos)

    except:

        idio = Idioma.objects.all().values().order_by("lenguaje")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'idio':idio,
            'r2' : "El ID ("+str(id)+") No Existe. Imposible Eliminar Idioma!!"
        }

        return render(request, 'form_registro_idiomas.html', datos)

    ##pass

def eliminarGenero(request, id):
    try:
        
        gene = Genero.objects.get(id=id)
        nom = gene.categoria
        gene.delete()


        # se registra en la tabla historial.
        descripcion = "Eliminación realizada ("+nom.lower()+")"
        tabla = "Genero"
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(  
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
        his.save()


        gene = Genero.objects.all().values().order_by("categoria")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'gene':gene,
            'r' : "El Genero Literario fue Eliminado Correctamente!!"
        }

        return render(request, "form_registro_generos.html", datos)

    except:

        gene = Genero.objects.all().values().order_by("categoria")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'gene':gene,
            'r2' : "El ID ("+str(id)+") No Existe. Imposible Eliminar Genero!!"
        }

        return render(request, 'form_registro_generos.html', datos)

    ## pass

##---------------------------------------------------------------##
##---------------------------------------------------------------##


##------------------------------------------------------------------------------------------------------------------------------##

def mostrarListarHistorial(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() == "ADMIN":

            his = Historial.objects.select_related('usuario').all().order_by("-id")
            
            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'his' : his
            }

            return render(request, 'listar_historial.html', datos)
            
        else:

            datos = { 'r2' : 'No tienes la capacidad de comprender el dominio de administrador' }
            return render(request, 'index.html', datos)
            
    else:
        datos = { 'r2' : 'Necesitas ingresar sesión para acceder' }
        return render(request, 'index.html', datos)


   ## return render(request, 'listar_historial.html')

##------------------------------------------------------------------------------------------------------------------------------##


##---------------------------------------------------------------##
##------------------FUNCIONES DE USUARIO-------------------------##
##---------------------------------------------------------------##


def mostrarMenuUsuario(request):
    estadoSesion = request.session.get("estadoSesion")
    nomUsuario = request.session.get("nomUsuario")

    if estadoSesion is True:
        if nomUsuario.upper()!="ADMIN":
            datos = { 'nomUsuario' : request.session["nomUsuario"] }
            return render(request, 'menu_usuario.html', datos)
        else:
            datos = { 'r2' : 'No tienes la capacidad de comprender el dominio de un operador común' }
            return render(request, 'index.html', datos)
    else:
        datos = { 'r2' : 'Necesitas ingresar sesión para acceder' }
        return render(request, 'index.html', datos)
    
    ## return render(request, 'menu_usuario.html')

##---------------------------------------------------------------##
##---------------------------------------------------------------##

## aca tomaremos los dos datos de la tabla Genero y Idioma 
def mostrarFormRegistrar(request): 
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() != "ADMIN":

            opcionesIdioma = Idioma.objects.all().values().order_by("lenguaje")
            opcionesGenero = Genero.objects.all().values().order_by("categoria")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'opcionesIdioma' : opcionesIdioma,
                'opcionesGenero' : opcionesGenero
            }
            return render(request, 'form_registrar.html', datos)
        else:
            
            datos = {
                'r2' : 'No tienes el Divino derecho de acceder a este Formulario.'
            }
            return render(request, 'index.html', datos)
    else:

        datos = {
            'r2' : 'Necesitas ingresar sesión para acceder'
        }
        return render(request, 'index.html', datos)
             
    


    ## return render(request, 'form_registrar.html')



def registrarBiblioteca(request): ## toma datos de registrarPintura, con una mezcla de la funcion de eva 2 de insertarBiblioteca
    if request.method == "POST":
        tit = request.POST['txttit'].upper()
        nom = request.POST['txtnom']
        num = request.POST['numpag']
        lit = request.POST['oplit']
        idi = request.POST['cboidi']   ## Orden según la bd  idioma_id va alfinal
        cod = request.POST['numcod']
        gen = request.POST['cbogen']   ## y según la bd genero_id va primero
        edi = request.POST['txtdes']

        comprobarIdioma = Biblioteca.objects.filter(titulo=tit)
        if comprobarIdioma:

            opcionesIdioma = Idioma.objects.all().values().order_by("lenguaje")
            opcionesGenero = Genero.objects.all().values().order_by("categoria")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'opcionesIdioma' : opcionesIdioma,
                'opcionesGenero' : opcionesGenero,
                'r2' : ' El Titulo del libro ('+tit.upper()+') ya existe. Registralo con otro nombre '
            }
            return render(request, 'form_registrar.html', datos)
        else:

            # registro datos
            bli = Biblioteca(
                titulo = tit,
                nombre = nom,
                numero = num,
                literatura = lit,
                codigo = cod,
                editorial = edi,
                genero_id = gen,    ##nombre de bd FK
                idioma_id = idi
            )
            bli.save()

            # Registro en Historial
            descripcion = "Libro ("+tit.lower()+") Registrado "
            tabla = "Biblioteca"
            fechayhora = datetime.now()
            usuario = request.session["idUsuario"]
            his = Historial(  
                    descripcion_historial=descripcion,
                    tabla_afectada_historial=tabla,
                    fecha_hora_historial=fechayhora,
                    usuario_id=usuario
                )
            his.save()

            # Se listan ambos campos 1 y 2
            opcionesIdioma = Idioma.objects.all().values().order_by("lenguaje")
            opcionesGenero = Genero.objects.all().values().order_by("categoria")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'opcionesIdioma' : opcionesIdioma,
                'opcionesGenero' : opcionesGenero,
                'r' : 'El Libro ('+tit+') Agregado a la Lista'
            }
            return render(request, 'form_registrar.html', datos)
    else:

        opcionesIdioma = Idioma.objects.all().values().order_by("lenguaje")
        opcionesGenero = Genero.objects.all().values().order_by("categoria")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'opcionesIdioma' : opcionesIdioma,
            'opcionesGenero' : opcionesGenero,
            'r2' : 'Debias Oprimir el Botón de "Registrar" ._.'
        }
        return render(request, 'form_registrar.html', datos)

    ## pass

##---------------------------------------------------------------##
##---------------------------------------------------------------##


def mostrarListado(request):
    estadoSesion = request.session.get("estadoSesion")
    if estadoSesion is True:
        if request.session["nomUsuario"].upper() != "ADMIN":
            # Acá con solo poner un valor como 'idioma' ya está bien y toma todos los datos, pero eeh
            # Queria asegurarme con la peticion a la bd del select_related
            bli = Biblioteca.objects.select_related('idioma','genero').all().order_by("id")

            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'bli' : bli
            }

            return render(request, 'listado.html', datos)
        else:

            datos = {
                'r2' : 'No tienes el Divino derecho de acceder a este Formulario.'
            }
            return render(request, 'index.html', datos)
    else:

        datos = {
            'r2' : 'Necesitas ingresar sesión para acceder'
        }
        return render(request, 'index.html', datos)


    ## return render(request, 'listado.html')



##---------------------------------------------------------------##
##---------------------------------------------------------------##


def mostrarFormActualizar(request, id):
    try:
        estadoSesion = request.session.get("estadoSesion")
        if estadoSesion is True:

            encontrado = Biblioteca.objects.get(id=id)

            opcionesIdioma = Idioma.objects.all().values().order_by("lenguaje")
            opcionesGenero = Genero.objects.all().values().order_by("categoria")



            datos = {
                'nomUsuario' : request.session["nomUsuario"],
                'encontrado' : encontrado,
                'opcionesIdioma' : opcionesIdioma,
                'opcionesGenero' : opcionesGenero
            }
            return render(request, 'form_actualizar.html', datos)
        else:

            datos = {
                'r2' : 'Necesitas ingresar sesión para acceder'
            }
            return render(request, 'index.html', datos)

    except:
        opcionesIdioma = Idioma.objects.all().values().order_by("lenguaje")
        opcionesGenero = Genero.objects.all().values().order_by("categoria")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'opcionesIdioma' : opcionesIdioma,
            'opcionesGenero' : opcionesGenero,
            'r2' : 'El ID  No Existe. Imposible Actualizar tál Libro'
        }
        return render(request, 'form_registrar.html', datos) ## listado.html toma los datos mal,
         ## si intentas escribir un id que no existe al momento de actualizar lleva acá. Se ve desprolijo en listado.html



    ## pass



def actualizarBiblioteca(request, id):
    try:
        tit = request.POST['txttit'].upper()
        nom = request.POST['txtnom']
        num = request.POST['numpag']
        lit = request.POST['oplit']
        idi = request.POST['cboidi']   ## Orden según la bd  idioma_id va alfinal
        cod = request.POST['numcod']
        gen = request.POST['cbogen']   ## y según la bd genero_id va primero
        edi = request.POST['txtdes']

        bli = Biblioteca.objects.get(id=id)

        bli.titulo = tit
        bli.nombre = nom
        bli.numero = num
        bli.literatura = lit
        bli.idioma_id = idi
        bli.codigo = cod
        bli.genero_id = gen
        bli.editorial = edi
        bli.save()

        # Historial
        descripcion = "Modificación realizada ("+tit.lower()+")"
        tabla = "Biblioteca"
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(  
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
        his.save()

        bli = Biblioteca.objects.select_related('idioma').all().order_by("titulo")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'bli' : bli,
            'r' : 'Libros Actualizados a su gusto :D.. quisquilloso'
        }
        return render(request, 'listado.html', datos)

    except:

        opcionesIdioma = Idioma.objects.all().values().order_by("lenguaje")
        opcionesGenero = Genero.objects.all().values().order_by("categoria")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'opcionesIdioma' : opcionesIdioma,
            'opcionesGenero' : opcionesGenero,
            'r2' : "El ID ("+str(id)+") No Existe. Imposible Actualizar tál Libro"
        }
        return render(request, 'form_registrar.html', datos)



    
    ## pass
##---------------------------------------------------------------##
##---------------------------------------------------------------##


def eliminarBiblioteca(request, id):
    try:
        bli = Biblioteca.objects.get(id=id)
        nom = bli.titulo
        bli.delete()

        # Historial
        descripcion = "Se Eliminó ("+nom.lower()+") :c "
        tabla = "Biblioteca"
        fechayhora = datetime.now()
        usuario = request.session["idUsuario"]
        his = Historial(  
                descripcion_historial=descripcion,
                tabla_afectada_historial=tabla,
                fecha_hora_historial=fechayhora,
                usuario_id=usuario
            )
        his.save()

        bli = Biblioteca.objects.select_related("idioma").all().order_by("titulo")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'bli' : bli,
            'r' : "El Libro ('"+nom+"') Fue Eliminado Como a deseado."
        }
        return render(request, "listado.html", datos)

    except:

        bli = Biblioteca.objects.select_related("idioma").all().order_by("titulo")

        datos = {
            'nomUsuario' : request.session["nomUsuario"],
            'bli' : bli,
            'r2' : "El ID ("+str(id)+") No Existe. Imposible Eliminar tál Libro"
        }
        return render(request, 'listado.html', datos)

   ## pass


