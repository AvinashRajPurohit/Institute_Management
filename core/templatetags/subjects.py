from django import template
from django.shortcuts import get_object_or_404

from core.models import Student,Teacher,Subject
register = template.Library()


@register.filter
def distinct_subject(id):
    student = get_object_or_404(Student,id=id)
    teachers = student.teachers.all()
    sub = set()
    for i in teachers:
        for j in i.subjects.all():
            sub.add(j.name)
    return list(sub)

