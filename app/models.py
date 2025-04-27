from django.db import models

import os

# Create your models here.
class UsersModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=100,null=True,default='pending')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "UsersModel"

class OwnersModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "OwnersModel"
 
class FileUploadModel(models.Model):
    email=models.EmailField(null=True)
    keyword1 = models.CharField(max_length=100)
    keyword2 = models.CharField(max_length=100)
    keyword3 = models.CharField(max_length=100)
    files = models.FileField(upload_to=os.path.join('static', 'Files'))
    filename=models.CharField(max_length=100)
    time=models.DateTimeField()

    def __str__(self):
        return f"{self.keyword1}, {self.keyword2}, {self.keyword3} , {self.filename}"
    
    class Meta:
        db_table = "FileUploadModel"

class SearchModel(models.Model):
    email=models.EmailField()
    keyword = models.CharField(max_length=100)
    time=models.DateTimeField()
    status = models.CharField(max_length=100,default='waiting')
    filerequest=models.CharField(max_length=100,default='not requested')
    files = models.FileField(upload_to=os.path.join('static', 'RequestedFiles'),null=True)
    def __str__(self):
        return f"{self.keyword}, {self.fileid}"

    class Meta:
        db_table = "SearchModel"

class DownloadModel(models.Model):
    email=models.EmailField()
    files=models.CharField(max_length=100)
    time=models.DateTimeField()

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "DownloadModel"

