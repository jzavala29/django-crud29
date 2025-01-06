from django.http import HttpResponse
from django.shortcuts import redirect, render
#importando el modelo estudiante
from.models import Estudiante,Clase,Docente,Asistencia,Calificacion,Reporte
#importando la libreria para mensajes de confirmacion 
from django.contrib import messages 
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist  # Asegúrate de importar esto

from django.http import JsonResponse
from django.db import transaction


'''Funcion para presentar en pantalla (renderizar)
    el codigo html del template inicio.html:
'''
#Presentando en pantalla el formulario Inicio 
def inicio(request):
    return render(request,'inicio.html')
#Presentando en pantalla el formulario de ESTUDIANTE 
def nuevoEstudiante(request):
    return render(request,'nuevoEstudiante.html')
#Presentando en pantalla el formulario de una Nueva Clase 
def nuevaClase(request):
    # Obtener todos los estudiantes para poblar el select en el formulario
    estudiantes = Estudiante.objects.all()
    # Renderizar la plantilla y pasar los estudiantes al contexto
    return render(request, 'nuevaClase.html', {'estudiantes': estudiantes})
# Mostrar formulario para agregar un nuevo docente
def nuevoDocente(request):
    return render(request, 'nuevoDocente.html')
# Mostrar formulario para registrar asistencia
def nuevaAsistencia(request):
    estudiantes = Estudiante.objects.all()
    clases = Clase.objects.all()
    return render(request, 'nuevaAsistencia.html', {'estudiantes': estudiantes, 'clases': clases})
# Mostrar formulario para registrar calificación
def nuevaCalificacion(request):
    estudiantes = Estudiante.objects.all()
    clases = Clase.objects.all()
    return render(request, 'nuevaCalificacion.html', {'estudiantes': estudiantes, 'clases': clases})

# Mostrar formulario para crear reporte
def nuevoReporte(request):
    estudiantes = Estudiante.objects.all()
    clases = Clase.objects.all()
    calificaciones = Calificacion.objects.all()
    
    context = {
        'estudiantes': estudiantes,
        'clases': clases,
        'calificaciones': calificaciones,
    }
    return render(request, 'nuevoReporte.html', context)
#**************************************************LISTADO ESCOLAR ********************************
def listaEstudiantes(request):
    estudiantes_bdd = Estudiante.objects.all()
    return render(request, 'listaEstudiantes.html', {'estudiantes': estudiantes_bdd})
#Listado nuevo estudiante 
def listaClases(request):
    # Obtener todas las clases para la lista
    clases_bdd = Clase.objects.all()
    return render(request, 'listaClases.html', {'clases': clases_bdd})
# Listar docentes
def listaDocentes(request):
    docentes_bdd = Docente.objects.all()
    return render(request, 'listaDocentes.html', {'docentes': docentes_bdd})
# Listar asistencias
def listaAsistencias(request):
    asistencias_bdd = Asistencia.objects.select_related('estudiante', 'clase').all()
    return render(request, 'listaAsistencias.html', {'asistencias': asistencias_bdd})

# Listar calificaciones
def listaCalificaciones(request):
    calificaciones_bdd = Calificacion.objects.select_related('estudiante', 'clase').all()
    return render(request, 'listaCalificaciones.html', {'calificaciones': calificaciones_bdd})
# Listar reportes
def listaReportes(request):
    reportes = Reporte.objects.all().select_related('estudiante', 'clase')
    return render(request, 'listaReportes.html', {'reportes': reportes})

#****************************************BOTON ELIMINAR *************************
def eliminarEstudiante(request, id):
    estudiante = get_object_or_404(Estudiante, id=id)
    estudiante.delete()
    messages.success(request, "Estudiante eliminado correctamente")
    return redirect('/listaEstudiantes') 
#-----------------------------eliminar clase ------------------------------------
def eliminarClase(request, id):
    clase = get_object_or_404(Clase, id=id)
    clase.delete()
    messages.success(request, "Clase eliminada correctamente")
    return redirect('/listaClases')
#-------------------------ELIMINAR DOCENTE------------------------------
def eliminarDocente(request, id):
    docente = get_object_or_404(Docente, id=id)
    docente.delete()
    messages.success(request, "Docente eliminado correctamente")
    return redirect('/listaDocentes')
#------------------------ELIMINAR ASISTENCIA -----------------------
def eliminarAsistencia(request, id):
    asistencia = get_object_or_404(Asistencia, id=id)
    asistencia.delete()
    messages.success(request, "Asistencia eliminada correctamente")
    return redirect('/listaAsistencias')
#-------------------------ELIMNAR CALIFICACIONES--------------------
def eliminarCalificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)
    calificacion.delete()
    messages.success(request, "Calificación eliminada correctamente")
    return redirect('/listaCalificaciones')
#----------------------------ELIMINAR PROMEDIO--------------------------
def eliminarReporte(request, id):
    reporte = get_object_or_404(Reporte, id=id)
    reporte.delete()
    messages.success(request, "Reporte eliminado correctamente")
    return redirect('/listaReportes')
#*************************************************Guardar los datos*********************************
# Vista para guardar un nuevo estudiante----------------------------------
def guardarEstudiante(request):
    if request.method == 'POST':
        nombre = request.POST.get('txt_nombre')
        apellido = request.POST.get('txt_apellido')
        matricula = request.POST.get('txt_matricula')

        # Validar que los campos no estén vacíos
        if not nombre or not apellido or not matricula:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('/nuevoEstudiante/')  # Redirige correctamente a la ruta de agregar estudiante

        # Validar que la matrícula tenga al menos 6 caracteres
        if len(matricula) < 6:
            messages.error(request, "La matrícula debe tener al menos 6 caracteres.")
            return redirect('/nuevoEstudiante/')  # Redirige correctamente a la ruta de agregar estudiante

        # Verificar si ya existe un estudiante con la misma matrícula
        if Estudiante.objects.filter(matricula=matricula).exists():
            messages.error(request, "Ya existe un estudiante con esa matrícula.")
            return redirect('/nuevoEstudiante/')  # Redirige correctamente a la ruta de agregar estudiante

        try:
            # Crear un nuevo estudiante en la base de datos
            estudiante = Estudiante.objects.create(
                nombre=nombre,
                apellido=apellido,
                matricula=matricula
            )
            messages.success(request, "Estudiante agregado exitosamente.")
            return redirect('/listaEstudiantes/')  # Redirigir a la lista de estudiantes

        except Exception as e:
            messages.error(request, f"Hubo un error al guardar el estudiante: {str(e)}")
            return redirect('/nuevoEstudiante/')  # Redirige correctamente a la ruta de agregar estudiante
    
    return redirect('/nuevoEstudiante/')  # Redirige correctamente a la ruta de agregar estudiante

# Vista para guardar un nueva CLASE ------------------------------------------------------------
def guardarClase(request):
    if request.method == 'POST':
        nombre = request.POST.get('txt_nombre')
        descripcion = request.POST.get('txt_descripcion')
        estudiante_id = request.POST.get('txt_estudiante')

        # Validar que el campo nombre no esté vacío
        if not nombre:
            messages.error(request, "El campo 'Nombre' es obligatorio.")
            return redirect('/nuevaClase/')

        # Validar que el nombre tenga al menos 3 caracteres
        if len(nombre) < 3:
            messages.error(request, "El nombre debe tener al menos 3 caracteres.")
            return redirect('/nuevaClase/')

        try:
            # Obtener el estudiante si se proporciona
            estudiante = None
            if estudiante_id:
                estudiante = Estudiante.objects.get(id=estudiante_id)

            # Crear una nueva clase en la base de datos
            Clase.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                estudiante=estudiante
            )

            messages.success(request, "Clase agregada exitosamente.")
            return redirect('/listaClases/')  # Redirigir a la lista de clases

        except Estudiante.DoesNotExist:
            messages.error(request, "El estudiante seleccionado no existe.")
            return redirect('/nuevaClase/')

        except Exception as e:
            messages.error(request, f"Hubo un error al guardar la clase: {str(e)}")
            return redirect('/nuevaClase/')

    return redirect('/nuevaClase/')
# Guardar un nuevo docente-------------------------------------------------------
def guardarDocente(request):
    if request.method == 'POST':
        nombre = request.POST.get('txt_nombre')
        apellido = request.POST.get('txt_apellido')
        email = request.POST.get('txt_email')

        # Validaciones
        if not nombre or not apellido or not email:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('/nuevoDocente/')
        
        if len(nombre) < 3 or len(apellido) < 3:
            messages.error(request, "El nombre y apellido deben tener al menos 3 caracteres.")
            return redirect('/nuevoDocente/')

        if Docente.objects.filter(email=email).exists():
            messages.error(request, "Ya existe un docente con ese correo.")
            return redirect('/nuevoDocente/')

        try:
            Docente.objects.create(nombre=nombre, apellido=apellido, email=email)
            messages.success(request, "Docente agregado exitosamente.")
            return redirect('/listaDocentes/')
        except Exception as e:
            messages.error(request, f"Hubo un error al guardar el docente: {str(e)}")
            return redirect('/nuevoDocente/')

    return redirect('/nuevoDocente/')
# Guardar asistencia--------------------------------------------------------------------------
def guardarAsistencia(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('select_estudiante')
        clase_id = request.POST.get('select_clase')
        fecha = request.POST.get('txt_fecha')
        presente = request.POST.get('select_presente') == 'True'

        if not estudiante_id or not clase_id or not fecha:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('/nuevaAsistencia/')

        try:
            estudiante = Estudiante.objects.get(id=estudiante_id)
            clase = Clase.objects.get(id=clase_id)
            Asistencia.objects.create(estudiante=estudiante, clase=clase, fecha=fecha, presente=presente)
            messages.success(request, "Asistencia registrada exitosamente.")
            return redirect('/listaAsistencias/')
        except Exception as e:
            messages.error(request, f"Hubo un error al registrar la asistencia: {str(e)}")
            return redirect('/nuevaAsistencia/')

    return redirect('/nuevaAsistencia/')
# Guardar calificación----------------------------------------------------------------------------------------------
def guardarCalificacion(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('select_estudiante')
        clase_id = request.POST.get('select_clase')
        tarea = request.POST.get('txt_tarea')
        nota = request.POST.get('txt_nota')

        if not estudiante_id or not clase_id or not tarea or not nota:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('/nuevaCalificacion/')

        try:
            estudiante = Estudiante.objects.get(id=estudiante_id)
            clase = Clase.objects.get(id=clase_id)
            Calificacion.objects.create(estudiante=estudiante, clase=clase, tarea=tarea, nota=nota)
            messages.success(request, "Calificación registrada exitosamente.")
            return redirect('/listaCalificaciones/')
        except Exception as e:
            messages.error(request, f"Hubo un error al registrar la calificación: {str(e)}")
            return redirect('/nuevaCalificacion/')

    return redirect('/nuevaCalificacion/')
# Guardar reporte---------------------------------------------------------------------------------------------
def guardarReporte(request):
    if request.method == 'POST':
        try:
            estudiante_id = request.POST.get('estudiante')
            clase_id = request.POST.get('clase')
            calificaciones_ids = request.POST.getlist('calificaciones[]')

            if not estudiante_id or not clase_id or not calificaciones_ids:
                return HttpResponse("Faltan datos requeridos", status=400)

            estudiante = Estudiante.objects.get(id=estudiante_id)
            clase = Clase.objects.get(id=clase_id)
            
            # Check if report already exists
            existing_report = Reporte.objects.filter(
                estudiante=estudiante,
                clase=clase
            ).first()
            
            if existing_report:
                # Update existing report
                reporte = existing_report
                reporte.calificaciones.clear()  # Remove old calificaciones
            else:
                # Create new report
                reporte = Reporte(
                    estudiante=estudiante,
                    clase=clase
                )
                reporte.save()
            
            calificaciones = Calificacion.objects.filter(
                id__in=calificaciones_ids,
                estudiante=estudiante,
                clase=clase
            )
            
            if not calificaciones.exists():
                if not existing_report:
                    reporte.delete()
                return HttpResponse("No se encontraron calificaciones válidas", status=400)
                
            reporte.calificaciones.add(*calificaciones)
            reporte.calcular_promedio()
            reporte.save()
            
            return redirect('listaReportes')
            
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
    
    return redirect('nuevoReporte')

def obtener_clases_por_estudiante(request):
    estudiante_id = request.GET.get('estudiante_id')
    
    if not estudiante_id:
        return JsonResponse({'error': 'ID de estudiante requerido'}, status=400)
        
    clases = Clase.objects.filter(estudiantes__id=estudiante_id)
    data = {
        'clases': [{'id': clase.id, 'nombre': clase.nombre} for clase in clases]
    }
    return JsonResponse(data)

def obtener_calificaciones_por_estudiante_y_clase(request):
    estudiante_id = request.GET.get('estudiante_id')
    clase_id = request.GET.get('clase_id')
    
    if not estudiante_id or not clase_id:
        return JsonResponse({'error': 'Datos incompletos'}, status=400)
        
    calificaciones = Calificacion.objects.filter(
        estudiante_id=estudiante_id,
        clase_id=clase_id
    )
    
    data = {
        'calificaciones': [{
            'id': c.id,
            'tarea': c.tarea,
            'nota': str(c.nota)
        } for c in calificaciones]
    }
    return JsonResponse(data)
#************************************Modificar y PROCESAR*****************
#-----------------------ESTUDIANTE--------------------------------
def editarEstudiante(request, id):
    # Obtener al estudiante a editar por su ID
    estudianteEditar = get_object_or_404(Estudiante, id=id)
    
    # Pasar los datos del estudiante a la plantilla
    return render(request, "editarEstudiante.html", {'estudiante': estudianteEditar})

def procesarEstudiante(request, id):
    # Obtener al estudiante por su ID
    estudiante = Estudiante.objects.get(id=id)
    
    # Actualizar los campos del estudiante con los datos del formulario
    estudiante.nombre = request.POST['txt_nombre']
    estudiante.apellido = request.POST['txt_apellido']
    estudiante.matricula = request.POST['txt_matricula']
    
    # Validar la matrícula (si deseas validaciones adicionales)
    if len(estudiante.matricula) < 6:
        messages.error(request, "La matrícula debe tener al menos 6 caracteres.")
        return redirect(f'/editarEstudiante/{id}/')
    
    try:
        # Guardar los cambios en la base de datos
        estudiante.save()
        messages.success(request, "Estudiante editado correctamente")
        return redirect('/listaEstudiantes/')  # Redirige a la lista de estudiantes
    except Exception as e:
        messages.error(request, f"Hubo un error al editar al estudiante: {str(e)}")
        return redirect(f'/editarEstudiante/{id}/')
#----------------------------------clase ---------------
# Función para mostrar el formulario de edición de clase
def editarClase(request, id):
    clase = get_object_or_404(Clase, id=id)
    estudiantes = Estudiante.objects.all()  # Obtener todos los estudiantes para el select
    return render(request, "editarClase.html", {'clase': clase, 'estudiantes': estudiantes})

# Función para procesar la edición de clase
def procesarClase(request, id):
    if request.method == 'POST':
        try:
            clase = Clase.objects.get(id=id)
            clase.nombre = request.POST.get('txt_nombre')
            clase.descripcion = request.POST.get('txt_descripcion')
            estudiante_id = request.POST.get('txt_estudiante')

            # Validar que el campo nombre no esté vacío
            if not clase.nombre:
                messages.error(request, "El campo 'Nombre' es obligatorio.")
                return redirect(f'/editarClase/{id}/')

            # Validar que el nombre tenga al menos 3 caracteres
            if len(clase.nombre) < 3:
                messages.error(request, "El nombre debe tener al menos 3 caracteres.")
                return redirect(f'/editarClase/{id}/')

            # Asignar estudiante si existe
            if estudiante_id:
                try:
                    estudiante = Estudiante.objects.get(id=estudiante_id)
                    clase.estudiante = estudiante
                except Estudiante.DoesNotExist:
                    messages.error(request, "El estudiante seleccionado no existe.")
                    return redirect(f'/editarClase/{id}/')

            # Guardar los cambios en la base de datos
            clase.save()
            messages.success(request, "Clase editada correctamente.")
            return redirect('/listaClases/')  # Redirigir a la lista de clases

        except Clase.DoesNotExist:
            messages.error(request, "La clase no existe.")
            return redirect('/listaClases/')

        except Exception as e:
            messages.error(request, f"Hubo un error al editar la clase: {str(e)}")
            return redirect(f'/editarClase/{id}/')

    # Si no es POST, redirigir al formulario de edición
    return redirect(f'/editarClase/{id}/')
#-----------------editar docente ---------
def editarDocente(request, id):
    docente = get_object_or_404(Docente, id=id)  # Obtener el docente a editar o mostrar un error 404
    return render(request, "editarDocente.html", {'docente': docente})

# Función para procesar la edición de docente
def procesarDocente(request, id):
    if request.method == 'POST':
        try:
            docente = Docente.objects.get(id=id)
            nombre = request.POST.get('txt_nombre')
            apellido = request.POST.get('txt_apellido')
            email = request.POST.get('txt_email')

            # Validaciones
            if not nombre or not apellido or not email:
                messages.error(request, "Todos los campos son obligatorios.")
                return redirect(f'/editarDocente/{id}/')

            if len(nombre) < 3 or len(apellido) < 3:
                messages.error(request, "El nombre y apellido deben tener al menos 3 caracteres.")
                return redirect(f'/editarDocente/{id}/')

            # Verificar si el email ya está en uso por otro docente
            if Docente.objects.filter(email=email).exclude(id=id).exists():
                messages.error(request, "Ya existe otro docente con ese correo.")
                return redirect(f'/editarDocente/{id}/')

            # Actualizar los datos del docente
            docente.nombre = nombre
            docente.apellido = apellido
            docente.email = email
            docente.save()

            messages.success(request, "Docente actualizado exitosamente.")
            return redirect('/listaDocentes/')

        except Docente.DoesNotExist:
            messages.error(request, "El docente no existe.")
            return redirect('/listaDocentes/')

        except Exception as e:
            messages.error(request, f"Hubo un error al actualizar el docente: {str(e)}")
            return redirect(f'/editarDocente/{id}/')

    # Si no es una petición POST, redirigir al formulario de edición
    return redirect(f'/editarDocente/{id}/')
#--------------------------------------------------------EDITAR ASISTENCIA------------------------
def editarAsistencia(request, id):
    asistencia = get_object_or_404(Asistencia, id=id)  # Obtener la asistencia a editar
    estudiantes = Estudiante.objects.all()  # Obtener todos los estudiantes para el select
    clases = Clase.objects.all()  # Obtener todas las clases para el select
    return render(request, "editarAsistencia.html", {
        'asistencia': asistencia,
        'estudiantes': estudiantes,
        'clases': clases
    })
def procesarAsistencia(request, id):
    if request.method == 'POST':
        try:
            # Obtener la asistencia que se quiere editar
            asistencia = Asistencia.objects.get(id=id)

            # Obtener los datos del formulario
            estudiante_id = request.POST.get('select_estudiante')
            clase_id = request.POST.get('select_clase')
            fecha = request.POST.get('txt_fecha')
            presente = request.POST.get('select_presente') == 'True'

            # Validaciones
            if not estudiante_id or not clase_id or not fecha:
                messages.error(request, "Todos los campos son obligatorios.")
                return redirect(f'/editarAsistencia/{id}/')

            # Obtener el estudiante y la clase seleccionados
            estudiante = Estudiante.objects.get(id=estudiante_id)
            clase = Clase.objects.get(id=clase_id)

            # Actualizar la asistencia
            asistencia.estudiante = estudiante
            asistencia.clase = clase
            asistencia.fecha = fecha
            asistencia.presente = presente
            asistencia.save()  # Guardar los cambios en la base de datos

            messages.success(request, "Asistencia actualizada exitosamente.")
            return redirect('/listaAsistencias/')  # Redirigir a la lista de asistencias

        except Estudiante.DoesNotExist:
            messages.error(request, "El estudiante seleccionado no existe.")
            return redirect(f'/editarAsistencia/{id}/')

        except Clase.DoesNotExist:
            messages.error(request, "La clase seleccionada no existe.")
            return redirect(f'/editarAsistencia/{id}/')

        except Asistencia.DoesNotExist:
            messages.error(request, "La asistencia no existe.")
            return redirect('/listaAsistencias/')

        except Exception as e:
            messages.error(request, f"Hubo un error al actualizar la asistencia: {str(e)}")
            return redirect(f'/editarAsistencia/{id}/')

    # Si no es una petición POST, redirigir al formulario de edición
    return redirect(f'/editarAsistencia/{id}/')


#--------------------------EDITAR CALIFICACION -------------------------
def editarCalificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)  # Obtener la calificación a editar o mostrar un error 404
    estudiantes = Estudiante.objects.all()  # Obtener todos los estudiantes para el select
    clases = Clase.objects.all()  # Obtener todas las clases para el select
    return render(request, "editarCalificacion.html", {
        'calificacion': calificacion,
        'estudiantes': estudiantes,
        'clases': clases
    })
def procesarCalificacion(request, id):
    if request.method == 'POST':
        try:
            calificacion = Calificacion.objects.get(id=id)

            # Obtener los datos del formulario
            estudiante_id = request.POST.get('select_estudiante')
            clase_id = request.POST.get('select_clase')
            tarea = request.POST.get('txt_tarea')
            nota = request.POST.get('txt_nota')

            # Validaciones
            if not estudiante_id or not clase_id or not tarea or not nota:
                messages.error(request, "Todos los campos son obligatorios.")
                return redirect(f'/editarCalificacion/{id}/')

            # Validar que el estudiante y la clase existan
            estudiante = Estudiante.objects.get(id=estudiante_id)
            clase = Clase.objects.get(id=clase_id)

            # Validar que la nota sea un número válido
            try:
                nota = float(nota)
                if nota < 0 or nota > 100:  # Supongamos que la nota es de 0 a 100
                    messages.error(request, "La nota debe estar entre 0 y 100.")
                    return redirect(f'/editarCalificacion/{id}/')
            except ValueError:
                messages.error(request, "La nota debe ser un número válido.")
                return redirect(f'/editarCalificacion/{id}/')

            # Actualizar los datos de la calificación
            calificacion.estudiante = estudiante
            calificacion.clase = clase
            calificacion.tarea = tarea
            calificacion.nota = nota
            calificacion.save()

            messages.success(request, "Calificación actualizada exitosamente.")
            return redirect('/listaCalificaciones/')

        except Estudiante.DoesNotExist:
            messages.error(request, "El estudiante seleccionado no existe.")
            return redirect(f'/editarCalificacion/{id}/')

        except Clase.DoesNotExist:
            messages.error(request, "La clase seleccionada no existe.")
            return redirect(f'/editarCalificacion/{id}/')

        except Calificacion.DoesNotExist:
            messages.error(request, "La calificación no existe.")
            return redirect('/listaCalificaciones/')

        except Exception as e:
            messages.error(request, f"Hubo un error al actualizar la calificación: {str(e)}")
            return redirect(f'/editarCalificacion/{id}/')

    # Si no es una petición POST, redirigir al formulario de edición
    return redirect(f'/editarCalificacion/{id}/')
#-----------------------------MODIFICAR REPORTE ---------------------------------------------------
def editarReporte(request, id):
    try:
        reporte = get_object_or_404(Reporte, id=id)
        estudiantes = Estudiante.objects.all()
        clases = Clase.objects.all()
        calificaciones = Calificacion.objects.filter(
            estudiante=reporte.calificaciones.first().estudiante if reporte.calificaciones.exists() else None,
            clase=reporte.calificaciones.first().clase if reporte.calificaciones.exists() else None
        )
        
        calificaciones_seleccionadas = list(reporte.calificaciones.values_list('id', flat=True))
        
        context = {
            'reporte': reporte,
            'estudiantes': estudiantes,
            'clases': clases,
            'calificaciones': calificaciones,
            'calificaciones_seleccionadas': calificaciones_seleccionadas,
        }
        
        return render(request, 'editarReporte.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar el reporte: {str(e)}")
        return redirect('listaReportes')


def procesarReporte(request, id):
    if request.method != 'POST':
        return redirect('editarReporte', id=id)
    
    try:
        # Obtener el reporte existente
        reporte = get_object_or_404(Reporte, id=id)
        
        # Obtener y validar datos del formulario
        estudiante_id = request.POST.get('estudiante')
        clase_id = request.POST.get('clase')
        calificaciones_ids = request.POST.getlist('calificaciones[]')  # Nota: volvemos a usar calificaciones[]
        
        # Validar que todos los campos necesarios estén presentes
        if not all([estudiante_id, clase_id, calificaciones_ids]):
            return JsonResponse({
                'success': False,
                'message': "Todos los campos son requeridos"
            }, status=400)
        
        # Obtener objetos relacionados
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        clase = get_object_or_404(Clase, id=clase_id)
        
        # Obtener calificaciones válidas
        calificaciones = Calificacion.objects.filter(
            id__in=calificaciones_ids,
            estudiante=estudiante,
            clase=clase
        )
        
        if not calificaciones.exists():
            return JsonResponse({
                'success': False,
                'message': "No se encontraron calificaciones válidas para el estudiante y clase seleccionados"
            }, status=400)
        
        # Actualizar el reporte
        with transaction.atomic():
            reporte.calificaciones.clear()
            reporte.calificaciones.add(*calificaciones)
            reporte.calcular_promedio()
            reporte.save()
        
        # Si la petición es AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': "Reporte actualizado exitosamente",
                'redirect_url': '/listaReportes/'
            })
        
        # Si no es AJAX, redirigir normalmente
        messages.success(request, "Reporte actualizado exitosamente")
        return redirect('listaReportes')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
        messages.error(request, f"Error al procesar el reporte: {str(e)}")
        return redirect('editarReporte', id=id)