from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django import forms
from deleteissue.models import MyTenantModel
import re
from django.core.validators import RegexValidator

class WorkspaceCreationForm(forms.Form):
    error_messages = {
        'duplicate_workspace': _("A workspace with that name already exists."),
    }
    helptxt = _("The workspace name can only contain letters and numbers (and _).")
    regexp = re.compile(r'^[a-zA-Z0-9_]+$')
    alphanum = RegexValidator(regex=regexp, message=helptxt, code=None)
    name = forms.CharField(max_length=100, validators=[alphanum])

    def clean_name(self):
        name = self.cleaned_data["name"]
        try:
            MyTenantModel._default_manager.get(name=name)
        except MyTenantModel.DoesNotExist:
            return name
        raise forms.ValidationError(self.error_messages['duplicate_workspace'])

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that login already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.EmailField(label=_("Login"),
        help_text=_("Your email address."),
        error_messages={
            'invalid': _("This is not a valid email address.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["username"]
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user
        