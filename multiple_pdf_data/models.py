from django.db import models

# Create your models here.



class Books(models.Model):
    BookName = models.CharField(max_length=100, verbose_name='Book Name')
    SubjectName = models.CharField(max_length=100, verbose_name='Subject Name')
    LevelName = models.CharField(max_length=100, verbose_name='Level Name')
    UploadFile = models.ImageField(upload_to="books", max_length=500, null=True, verbose_name='Upload File')
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')
    ModifiedDate = models.DateTimeField(auto_now=True, verbose_name='Modified Date')
    display_fields = ['BookName','SubjectName','LevelName','UploadFile','CreatedDate','ModifiedDate']

    def __str__(self):
        return self.BookName
    
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books' 
