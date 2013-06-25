from django import forms
from django.contrib import admin
from deleteissue.models import MyTenantModel, Project, Employee

admin.site.register(MyTenantModel)
admin.site.register(Employee)

def register_models_for_tenant(tenant):
	admin.site.register(Project.for_tenant(tenant))

for i in MyTenantModel.objects.all():
	register_models_for_tenant(i)

	
