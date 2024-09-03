from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Advertisement
from .forms import AdvertisementForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import AdvertisementFilter

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

class AdvertisementSearch(View):
    def get(self, request):
        advertisement_filter = AdvertisementFilter(request.GET, queryset=Advertisement.objects.all())
        return render(request, 'advertisement_search.html', {'filter': advertisement_filter})