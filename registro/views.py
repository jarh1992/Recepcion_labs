from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView
from .models import *
import json
from django.template import loader
from django.shortcuts import render_to_response
from .forms import *

'''
class IndexView(ListView):
    model = Registry
    template_name = "Index.html"

    def get(self, request, *args, **kwargs):
        pass

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)
'''


def index_view(request):
    if request.is_ajax():
        response_data = {}
        id = request.POST.get('id', None)
        '''
        Busqueda
        '''
        if id is not None:
            try:
                student = Student.objects.get(ced=id)
                registry = Registry.objects.get(student=student)
                response = 3
            except Student.DoesNotExist as sn:
                progs = list(Program.objects.values('name', 'cod'))
                response_data = {
                    'response': 1,
                    'programs': progs
                }
            except Registry.DoesNotExist as rn:
                response_data = {
                    'response': 2,
                }
            except Exception:
                print(Exception, 'er 3')
        else:
            response_data = {
                'response': 0
            }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == 'POST':
        op = request.POST.get('flag', 0)
        if op == "1":
            '''
            Save and add student to a Registry
            '''
            student = Student()
            student.name = request.POST.get('name', 0)
            student.ced = request.POST.get('ced', 0)
            student.cod = request.POST.get('cod', 0)
            student.program = Program.objects.get(name=request.POST.get('prog_name', None))
            student.save()
        elif op == "2":
            '''
            finalizar servicio (liberar Student y Pc)
            '''
        elif op == "3":
            '''
            Agregar a Registry / eliminar Student
            '''
        elif op == "nap":
            '''
            New academic program
            '''
            program = Program()
            program.name = request.POST.get('name', None)
            program.cod = request.POST.get('cod', None)
            program.save()

    form_sas = FormSAS()
    form_addprog = FormAddProg()
    reg_list = Registry.objects.all()
    context = {
        'list': reg_list,
        'form_sas': form_sas,
        'form_addprog': form_addprog
    }
    template = loader.get_template('Index.html')
    return HttpResponse(template.render(context, request))
