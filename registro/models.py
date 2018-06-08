from django.db import models


class Program(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, default='None')
    cod = models.CharField(max_length=3, blank=False, null=False, unique=True, default='None')

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, default='None')
    ced = models.CharField(primary_key=True, max_length=60, blank=False, null=False, unique=True, default='-1')
    cod = models.CharField(max_length=60, blank=False, null=False, unique=True, default='None')
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Pc(models.Model):
    num = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    pc_disp = models.BooleanField(default=True)

    def __str__(self):
        return self.num


class Loan(models.Model):
    student = models.OneToOneField(Student, on_delete=False, default=None)
    entry_time = models.DateTimeField(auto_now_add=True)
    departure_time = models.DateTimeField(default=None, null=True)
    pc = models.OneToOneField(Pc, on_delete=False, default=None)

    def __str__(self):
        return f'{self.student.name} {self.entry_time}'
