from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.models import PhoneNumber, Department
import jdatetime 

def user_image_path (instance, filename):
    return f"user_images/{instance.pk}/{filename}"

def gregorian2jalali(year, month, day):
    return jdatetime.date.fromgregorian(day=day,month=month,year=year).year

class UserProfile(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_admin   = models.BooleanField(default=False)
    user_image = models.ImageField(upload_to=user_image_path)
    phone_number = models.ManyToManyField(PhoneNumber,blank=True,related_name="user_phone_number")
    

class UserLastLogin(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.ip
    

class StudentProfile(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20,unique=True,blank=True)
    enrollment = models.DateField()
    
    def __str__(self):
        return self.student_id
    
    def save(self,*args,**kwargs):
        """Auto generate student id"""
        
        if not self.student_id:
            d = self.enrollment
            year = gregorian2jalali(year=d.year,month=d.month, day=d.day)
            last_student = StudentProfile.objects.filter(student_id__startswith=str(year)).order_by("-student_id").first()
            new_number = int(last_student.student_id[-3:]) +1 if last_student else 1
            self.student_id = f"{year}{new_number:03d}"
        super().save(*args,**kwargs)

class FacultyProfile(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=20,unique=True,blank=True)
    department = models.ForeignKey(Department,on_delete=models.PROTECT)  
    enrollment = models.DateField()
    
    def __str__(self):
        return self.faculty_id
    
    def save(self,*args,**kwargs):
        """Auto generate faculty id"""
        
        if not self.faculty_id:
            d = self.enrollment
            year = gregorian2jalali(year=d.year,month=d.month, day=d.day)
            last_faculty = FacultyProfile.objects.filter(faculty_id__startswith=str(year)).order_by("-faculty_id").first()
            new_number = int(last_faculty.faculty_id[-3:]) +1 if last_faculty else 1
            self.faculty_id = f"{year}{new_number:03d}"
        super().save(*args,**kwargs)