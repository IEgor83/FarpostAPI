from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Listing
from .serializers import ListingSerializer
from .forms import SignUpForm


@method_decorator(login_required, name="dispatch")
class ListingView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


@method_decorator(login_required, name="dispatch")
class ListingDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = 'listing_id'


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('listing')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('listing')

    def get_success_url(self):
        return self.success_url


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))
