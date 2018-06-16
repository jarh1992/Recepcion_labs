from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import ListView
from .models import *
import json
from django.template import loader
from django.shortcuts import render_to_response
from .forms import *
from django.core import serializers
from datetime import datetime

'''
class IndexView(ListView):
    model = Registry
    template_name = "Index.html"

    def get(self, request, *args, **kwargs):
        pass

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)
'''


def create_obj(obj_type: str, *req: object) -> object:
    if obj_type == 'student':
        prog_cod = req[0].get('sas_cod', '')
        student = Student.objects.create(
            name=req[0].get('sas_name', ''),
            ced=req[0].get('sas_ced', ''),
            cod=req[0].get('sas_cod', ''),
            program=Program.objects.get(cod=prog_cod)
        )
        return student
    elif obj_type == 'pc':
        pc = Pc.objects.create(
            num=req[0].get('num', '')
        )
        return pc
    elif obj_type == 'program':
        program = Program.objects.create(
            name=req[0].get('name', None),
            cod=req[0].get('cod', None)
        )
        return program
    elif obj_type == 'loan':
        loan = Loan.objects.create(
            student=req[1],
            pc=req[2]
        )
        return loan


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
                loan = Loan.objects.get(student=student)
                if loan.departure_time is None:
                    response_data = {
                        'response': 3,
                        'loan': serializers.serialize('json', (student, loan))
                    }
                else:
                    response_data = {
                        'response': 2,
                        'data': serializers.serialize('json', (student, student.program))
                    }
            except Student.DoesNotExist:
                progs = list(Program.objects.values('name', 'cod'))
                response_data = {
                    'response': 1,
                    'programs': progs
                }
            except Loan.DoesNotExist:
                response_data['response'] = 2
            except Exception as ex:
                print(type(ex).__name__, ex.args, '3')
        else:
            response_data['response'] = 0
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    elif request.method == 'POST':
        op = request.POST.get('flag', 0)
        if op == "sas":
            '''
            Create student and add him to Loan
            '''

            student = create_obj('student', request.POST)

            # evaluar disponibilidad de pc

            pc = create_obj('pc')
            pc.pc_disp = False
            pc.save()

            create_obj('loan', request.POST, student, pc)

        elif op == "fs":
            '''
            finish service (release Student and Pc)
            '''

            ced = request.POST.get('ifs_ced', None)
            student = Student.objects.get(ced=ced)
            loan = Loan.objects.get(student=student)
            loan.departure_time = str(datetime.now())
            loan.pc.pc_disp = True
            loan.save()

        elif op == "lds":
            '''
            add Student to Loan / delete Student
            '''

        elif op == "nap":
            '''
            New academic program
            '''

            create_obj('program', request.POST)

        elif op == "dap":
            '''
            Delete academic program
            '''
            cod = request.POST.get('del', None)
            Program.objects.filter(cod=cod).delete()

        elif op == "npc":
            '''
            New pc
            '''
            create_obj('pc', request.POST)

    form_sas = FormSAS()
    form_addprog = FormAddProg()
    form_addpc = FormAddPc()
    loan_list = list(Loan.objects.all())
    programs = list(Program.objects.values('name', 'cod'))
    context = {
        'list': loan_list,
        'form_sas': form_sas,
        'form_addprog': form_addprog,
        'form_addpc': form_addpc,
        'programs': programs
    }
    template = loader.get_template('Index.html')
    return HttpResponse(template.render(context, request))


def pc_view(request):
    if request.is_ajax():
        pass
    if request.method == 'POST':
        pass

    pc_list = list(Pc.objects.all())
    context = {
        'list': pc_list,
    }
    template = loader.get_template('Pc.html')
    return HttpResponse(template.render(context, request))
