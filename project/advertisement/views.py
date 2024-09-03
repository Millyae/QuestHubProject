# views.py
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Advertisement, Response, EmailVerification
from .forms import AdvertisementForm, ResponseForm
from django.urls import reverse_lazy

from .utils import generate_token, send_verification_email

class AdvertisementList(ListView):
    model = Advertisement
    ordering = '-created_at'
    template_name = 'advertisement_list.html'
    context_object_name = 'advertisements'
    paginate_by = 10

class AdvertisementDetail(DetailView):
    model = Advertisement
    template_name = 'advertisement_detail.html'
    context_object_name = 'advertisement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_form'] = ResponseForm()
        return context

class AdvertisementCreate(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'advertisement_create.html'
    success_url = reverse_lazy('advertisement_list')

    def form_valid(self, form):
        advertisement = form.save(commit=False)
        advertisement.author = self.request.user
        advertisement.save()
        messages.success(self.request, "Объявление успешно опубликовано!")
        return super().form_valid(form)

class AdvertisementUpdate(LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'advertisement_edit.html'
    success_url = reverse_lazy('advertisement_list')

class AdvertisementDelete(LoginRequiredMixin, DeleteView):
    model = Advertisement
    template_name = 'advertisement_delete.html'
    success_url = reverse_lazy('advertisement_list')


class CreateResponseView(CreateView):
    model = Response
    template_name = 'responses/response_create.html'
    fields = ['text']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.advert = get_object_or_404(Advertisement, id=self.kwargs['advert_id'])
        return super().form_valid(form)
class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'response_create.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.author = self.request.user
        response.advertisement = Advertisement.objects.get(pk=self.kwargs['pk'])
        response.save()
        advertisement = response.advertisement
        advertisement.notify_responses()
        messages.success(self.request, "Ваш отклик отправлен!")
        return redirect('advertisement_list')
class MyResponsesListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'my_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(advertisement__author=self.request.user)

    def post(self, request, *args, **kwargs):
        response_id = request.POST.get('response_id')
        action = request.POST.get('action')

        try:
            response = Response.objects.get(pk=response_id, advertisement__author=request.user)
        except Response.DoesNotExist:
            messages.error(request, "Отклик не найден.")
            return redirect('my_responses')

        if action == 'accept':
            response.is_accepted = True
            response.save()
            send_mail(
                subject='Ваш отклик принят',
                message=f'Ваш отклик на объявление "{response.advertisement.title}" принят.',
                from_email='your_email@example.com',
                recipient_list=[response.author.email]
            )
            messages.success(request, "Отклик принят.")
        elif action == 'delete':
            response.delete()
            messages.success(request, "Отклик удален.")

        return redirect('my_responses')

def register_user(request):
    if request.method == 'POST':
        # Логика регистрации пользователя
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(email=email, password=password)
        token = generate_token()
        EmailVerification.objects.create(user=user, token=token)
        send_verification_email(user, token)
        return redirect('registration_complete')

def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
        user = verification.user
        user.is_active = True
        user.save()
        verification.delete()
        return HttpResponse('Email verified successfully!')
    except EmailVerification.DoesNotExist:
        return HttpResponse('Invalid verification link.')

def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    response.is_accepted = True
    response.save()
    # Notify the original author of the response
    send_mail(
        'Ваш отклик принят',
        f'Ваш отклик на объявление "{response.advertisement.title}" принят.',
        'your_email@example.com',
        [response.author.email]
    )
    return redirect('my_responses')

def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    response.delete()
    return redirect('my_responses')
