# from accounts.models import
# from django.contrib.auth.models import User
from accounts.models import User
from django.forms.models import BaseModelForm

from django.views import generic
from django.http import HttpRequest, HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from django import forms


class UserListView(LoginRequiredMixin, generic.ListView):
    queryset = User.objects.all()
    template_name = "admin_panel/pages/users.html"


class UserUpdateView(generic.UpdateView):
    queryset = User.objects.all()
    template_name = "admin_panel/forms/form.html"
    fields = [
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    ]
    # form_class = UserForm

    def get_success_url(self) -> str:
        return reverse_lazy("admin_users")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(self.request, "User Updated Successfully!")
            return self.form_valid(form)
        else:
            messages.error(self.request, "User Cannot Be Updated!")
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_joined"].widget = forms.DateInput(attrs={"type": "date"})

        return form


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             "first_name",
#             "last_name",
#             "email",
#             "is_staff",
#             "is_active",
#             "date_joined",
#         ]
