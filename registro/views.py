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
    obj = None
    if obj_type == 'student':
        prog_cod = req[0].get('sas_progs', '')
        obj = Student.objects.create(
            name=req[0].get('sas_name', ''),
            ced=req[0].get('sas_ced', ''),
            cod=req[0].get('sas_cod', ''),
            program=Program.objects.get(cod=prog_cod)
        )
    elif obj_type == 'pc':
        obj = Pc.objects.create(
            name=req[0].get('name', '')
        )
    elif obj_type == 'program':
        obj = Program.objects.create(
            name=req[0].get('name', None),
            cod=req[0].get('cod', None)
        )
    elif obj_type == 'loan':
        obj = Loan.objects.create(
            student=req[1],
            pc=req[2]
        )
    return obj


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

            # pc = add existsent pc

            # create_obj('loan', request.POST, student, pc)

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


def pc_view(request):
    if request.is_ajax():
        print('ajax')
        id = request.POST.get('id', None)

        def update_all_pcs(state):
            pcs = Pc.objects.all()
            for pc in pcs:
                pc.pc_disp = state
                pc.save()

        if request.POST.get('fun') == 'all_av':
            update_all_pcs(True)
        elif request.POST.get('fun') == 'not_av':
            update_all_pcs(False)
        elif request.POST.get('fun') == 'updt':
            pc = Pc.objects.get(id=id)
            if pc.pc_disp is True:
                pc.pc_disp = False
            else:
                pc.pc_disp = True
            pc.save()
        elif request.POST.get('fun') == 'del':
            Pc.objects.get(id=id).delete()
        return HttpResponse(content_type="application/json")
    elif request.method == 'POST':
        print('post')
        op = request.POST.get('flag', 0)
        if op == "npc":
            '''
            New pc
            '''
            create_obj('pc', request.POST)

    pc_list = list(Pc.objects.all())
    form_addpc = FormAddPc()
    context = {
        'list': pc_list,
        'form_addpc': form_addpc
    }
    template = loader.get_template('Pc.html')
    return HttpResponse(template.render(context, request))
