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

'''
def create_obj(obj, *args):
    if type(obj) == Student:
        student = obj()
        student.name = args[0]
        student.ced = args[1]
        student.cod = args[2]
        prog_cod = args[3]
        student.program = Program.objects.get(cod=prog_cod)
        student.save()
    elif type(obj) == Pc:
        pc = obj()
        pc.num = args[0]
        pc.pc_disp = args[1]
        pc.save()
    elif type(obj) == Student:
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
                registry = Loan.objects.get(student=student)
                response = 3
            except Student.DoesNotExist as sn:
                progs = list(Program.objects.values('name', 'cod'))
                response_data = {
                    'response': 1,
                    'programs': progs
                }
            except Loan.DoesNotExist as rn:
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
        if op == "sas":
            '''
            Save and add student to a Loan
            '''
            student = Student()
            student.name = request.POST.get('sas_name', '')
            student.ced = request.POST.get('sas_ced', '')
            student.cod = request.POST.get('sas_cod', '')
            prog_cod = request.POST.get('sas_progs', None)
            student.program = Program.objects.get(cod=prog_cod)
            student.save()
            pc = Pc()
            pc.num = 2
            pc.pc_disp = False
            pc.save()
            loan = Loan()
            loan.student = student
            loan.pc = pc
            loan.save()

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
        elif op == "dap":
            '''
            Delete academic program
            '''
            cod = request.POST.get('del', None)
            Program.objects.filter(cod=cod).delete()

    form_sas = FormSAS()
    form_addprog = FormAddProg()
    loan_list = list(Loan.objects.all())
    programs = list(Program.objects.values('name', 'cod'))
    context = {
        'list': loan_list,
        'form_sas': form_sas,
        'form_addprog': form_addprog,
        'programs': programs
    }
    template = loader.get_template('Index.html')
    return HttpResponse(template.render(context, request))



