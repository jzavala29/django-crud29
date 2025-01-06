#Urls especificadas de la aplicacion 
from django.urls import path
from . import views 

urlpatterns=[
    path('',views.inicio),
    path('nuevoEstudiante/',views.nuevoEstudiante),
    path('guardarEstudiante/',views.guardarEstudiante),
    path('listaEstudiantes/',views.listaEstudiantes),
    path('eliminarEstudiante/<id>',views.eliminarEstudiante),
    path('editarEstudiante/<id>',views.editarEstudiante),
    path('procesarEstudiante/<id>',views.procesarEstudiante),
    

    path('nuevaClase/',views.nuevaClase),
    path('listaClases/',views.listaClases),
    path('guardarClase/',views.guardarClase),
    path('eliminarClase/<id>',views.eliminarClase),
    path('editarClase/<id>',views.editarClase),
    path('procesarClase/<id>',views.procesarClase),

    path('nuevoDocente/',views.nuevoDocente),
    path('listaDocentes/',views.listaDocentes),
    path('guardarDocente/',views.guardarDocente),
    path('eliminarDocente/<id>',views.eliminarDocente),
    path('editarDocente/<id>',views.editarDocente),
    path('procesarDocente/<id>',views.procesarDocente),
    

    path('nuevaAsistencia/',views.nuevaAsistencia),
    path('listaAsistencias/',views.listaAsistencias),
    path('guardarAsistencia/',views.guardarAsistencia),
    path('eliminarAsistencia/<id>',views.eliminarAsistencia),
    path('editarAsistencia/<id>',views.editarAsistencia),
    path('procesarAsistencia/<id>',views.procesarAsistencia),
    

    path('nuevaCalificacion/',views.nuevaCalificacion,name='nuevaCalificacion'),
    path('listaCalificaciones/',views.listaCalificaciones),
    path('guardarCalificacion/',views.guardarCalificacion),
    path('eliminarCalificacion/<id>',views.eliminarCalificacion),
    path('editarCalificacion/<id>',views.editarCalificacion),
    path('procesarCalificacion/<id>',views.procesarCalificacion),
    

     path('nuevoReporte/', views.nuevoReporte, name='nuevoReporte'),
    path('listaReportes/', views.listaReportes, name='listaReportes'),
    path('guardarReporte/', views.guardarReporte, name='guardarReporte'),
    path('obtener_clases_por_estudiante/', views.obtener_clases_por_estudiante, name='obtener_clases_por_estudiante'),
    path('obtener_calificaciones_por_estudiante_y_clase/', views.obtener_calificaciones_por_estudiante_y_clase, name='obtener_calificaciones_por_estudiante_y_clase'),
    path('eliminarReporte/<id>',views.eliminarReporte),
    path('editarReporte/<int:id>/', views.editarReporte, name='editarReporte'),
    path('obtener_calificaciones_por_estudiante_y_clase/', views.obtener_calificaciones_por_estudiante_y_clase, name='obtener_calificaciones_por_estudiante_y_clase'),
    path('procesarReporte/<id>',views.procesarReporte),
    
 ]