from .models import User,Student,Teacher,Subject
from rest_framework import serializers


class SubjectSerializer(serializers.ModelSerializer):
    subname = serializers.CharField(source='name')
    class Meta:
        model = Subject
        fields = ('subname',)

    # def to_representation(self, instance):
    #     data = super(SubjectSerializer, self).to_representation(instance)
    #     resdata = []
    #     print(data)
    #     for i,j in data.items():
    #         resdata.append(j)
    #     print(resdata)
    #     return resdata


class TeacherSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    def get_subjects(self, obj):
        subjects = []
        for n in obj.subjects.all():
            subjects.append(n.name)
        return subjects

    class Meta:
        model = Teacher
        fields = ('id', 'name', 'subjects')


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="student.username")
    teachers = TeacherSerializer(many=True,read_only=True)

    class Meta:
        model = Student
        fields = ("student_name", 'id', 'username', 'teachers')
        depth=1


class UpdateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'subjects')

