from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import urllib.request
from .models import Pagina

FORMULARIO = """
<form action="" method="POST">
    Introduzca una URL: <br>
    Url: <input type="text" name="url" required><br>
    <input type = "submit" value = "Enviar"> 
</form>
"""
def add_http(url):
    if (url.startswith('http://')) or (url.startswith('https://')):
        return url
    else:
        url = ('http://') + url
        return url
# Create your views here.
@csrf_exempt
def barra(request):
    if request.method == "POST":
        pag_nom = add_http(request.POST['url'])
        try:
            pagina = Pagina.objects.get(url=pag_nom)
            respuesta = '<h1> Página ya almacenada en la caché </h1><br>'
            respuesta += '<a href= /> Volver a la página principal </a>'
            return HttpResponse(respuesta)
        except Pagina.DoesNotExist:
            try:
                cont = urllib.request.urlopen(pag_nom)
                pag_cont = cont.read()
                pagina = Pagina(url = pag_nom,contenido = pag_cont)
                pagina.save()
            except urllib.error.URLError:
                return HttpResponse('<h1> Ha introducido mal la página o esta no existe en la caché </h1>')
            return HttpResponseRedirect(pag_nom)
    respuesta = '<h1> Django Cache </h1><br>'
    respuesta += FORMULARIO
    respuesta += 'Lista de páginas almacenadas en la caché: <br>'
    paginas = Pagina.objects.all()
    for pagina in paginas:
        respuesta += "<li>" + "<a href = /" + str(pagina.id) + ">" + pagina.url + "</a>"
    respuesta += "</ul>"
    return HttpResponse(respuesta)

def procesar(request,num):
    try:
       pagina = Pagina.objects.get(id=int(num))
    except Pagina.DoesNotExist:
        return HttpResponse('<h1> La pagina no se encuentra en la cache </h1>')
    respuesta = pagina.contenido
    return HttpResponse(respuesta)

def error(request):
   return HttpResponse('<h1> 404 Not Found </h1>')
