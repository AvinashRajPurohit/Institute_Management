from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Student, Teacher
from .serializers import StudentSerializer, UpdateSubjectSerializer


def table(request):
    students = Student.objects.all()
    context = {
        'students':students
    }
    return render(request,'table.html',context)


class get_student(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        if request.query_params.get('id'):
            studentId = request.query_params.get('id')
            if get_object_or_404(Student, id=studentId).student.is_student:
                student = Student.objects.get(id=studentId)
                serializer = StudentSerializer(student)
                return Response(serializer.data)
            else:
                return Response({'message':'No Student found with this id'})
        else:
            return Response({'message':"Please Enter Student Id"})


class UpdateSubjectView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        return Teacher.objects.get(id=id)

    def patch(self, request):
        teacherId = request.data.get('id')
        if teacherId:
            teacher_object = self.get_object(teacherId)
            serializer = UpdateSubjectSerializer(teacher_object, data=request.data, partial=True) # set partial=True to update a data partially
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(status=201, data=serializer.data, safe=False)
            return JsonResponse(status=400, data=serializer.errors, safe=False)
        else:
            return JsonResponse(status=400, data="Please Enter Teacher Id ", safe=False)