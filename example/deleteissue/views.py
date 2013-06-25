from deleteissue.forms import WorkspaceCreationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from deleteissue.models import MyTenantModel, Project, Employee
from deleteissue.admin import register_models_for_tenant

def step1(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    newuser = form.save()
	    user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
	    if user is not None:
		if user.is_active:
		    login(request, user)
		    return HttpResponseRedirect('/deleteissue/step2/') # Redirect after POST
		else:
		    print "Return a 'disabled account' error message"
	    else:
		print "Return an 'invalid login' error message."
    else:
	form = UserCreationForm() # An unbound form
    return render(request, 'step1.html', {'form': form, 'form_action': "/deleteissue/step1/"})

@login_required
def step2(request):
    if request.method == 'POST': # If the form has been submitted...
        form = WorkspaceCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
	    name = form.cleaned_data['name']
	    workspace = MyTenantModel.objects.create(name=name)
	    Employee.objects.create(user=request.user, workspace=workspace)
	    
	    from django.contrib.contenttypes.models import ContentType
            from django.contrib.auth.management import create_permissions
	    from django.contrib.auth.models import Permission
            from django.db.models import get_app, get_models
            create_permissions(get_app('deleteissue'), get_models(), 0) ### should optimize by calling only the new models instead of get_models
	    #user = TenantUser.for_tenant(workspace).objects.create_user("max@max.com", "max")
	    user = request.user

	    ct = ContentType.objects.get_for_model(Project.for_tenant(workspace))
	    perm = Permission.objects.filter(content_type=ct)
	    for i in perm:
		user.user_permissions.add(i)

	    register_models_for_tenant(workspace)
	    return HttpResponseRedirect('/admin/') # Redirect after POST
    else:
        form = WorkspaceCreationForm() # An unbound form
    return render(request, 'step2.html', {'form': form, 'form_action': "/deleteissue/step2/"})