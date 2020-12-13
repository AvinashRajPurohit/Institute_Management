from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save


'''
     As you give in Assessment that "The System Should have 2 types of users".
     That's why i use abstract user
'''


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='subjects')

    def __str__(self):
        return self.name


class Student(models.Model):
    student_name = models.CharField(max_length=200)
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher, related_name='teachers')

    def __str__(self):
        return self.student_name


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    students = models.ManyToManyField(Student)


    def __str__(self):
        return self.title


'''
This post Save function help us to separate our users and make our system loose couple
'''


def post_save_roll(sender, instance, created, *args, **kwargs):
    if created:
        instance.set_password(instance.password)
        try:
            if instance.is_teacher:
                instance.is_student = False
                instance.save()
                Teacher.objects.create(name=instance.username,teacher=instance)
            elif instance.is_student:
                instance.is_teacher= False
                instance.save()
                Student.objects.create(student_name=instance.username,student=instance)
            else:
                pass
        except:
            pass


post_save.connect(post_save_roll, sender=User)