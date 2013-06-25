from django.db import models
from tenancy.models import AbstractTenant, TenantModel
from django.contrib.auth.models import User

class MyTenantModel(AbstractTenant):
   name = models.CharField(max_length=50)
   # other fields
   def natural_key(self):
      return ((self.name, ))

class Employee(models.Model):
    user = models.OneToOneField(User)
    workspace = models.ForeignKey(MyTenantModel)

class Project(TenantModel):
   name = models.CharField(max_length=50)
   employee = models.ForeignKey(Employee)
