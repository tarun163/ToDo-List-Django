from django.db import models

# Create your models here.

class Task(models.Model):
    taskname = models.CharField(max_length=30)
    taskdesc = models.TextField()
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.taskname 

