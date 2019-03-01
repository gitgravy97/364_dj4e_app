# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string

from wizards.models import Wizard, House
from wizards.forms import HouseForm

class MainView(LoginRequiredMixin, View) :
    def get(self, request):
        hc = House.objects.all().count();
        wl = Wizard.objects.all();

        ctx = { 'house_count': hc, 'wizard_list': wl };
        return render(request, 'wizards/wizard_list.html', ctx)

# Take the easy way out on the main table
class WizardCreate(LoginRequiredMixin,CreateView):
    model = Wizard
    fields = '__all__'
    success_url = reverse_lazy('wizards')

class WizardUpdate(LoginRequiredMixin, UpdateView):
    model = Wizard
    fields = '__all__'
    success_url = reverse_lazy('wizards')

class WizardDelete(LoginRequiredMixin, DeleteView):
    model = Wizard
    fields = '__all__'
    success_url = reverse_lazy('wizards')

class HouseView(LoginRequiredMixin,View) :
    def get(self, request):
        hl = House.objects.all();
        ctx = { 'house_list': hl };
        return render(request, 'wizards/house_list.html', ctx)

class HouseCreate(LoginRequiredMixin, View):
    template = 'wizards/house_form.html'
    success_url = reverse_lazy('wizards')
    def get(self, request) :
        form = HouseForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request) :
        form = HouseForm(request.POST)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        house = form.save()
        return redirect(self.success_url)

class HouseUpdate(LoginRequiredMixin, View):
    model = House
    success_url = reverse_lazy('wizards')
    template = 'wizards/house_form.html'
    def get(self, request, pk) :
        house = get_object_or_404(self.model, pk=pk)
        form = HouseForm(instance=house)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk) :
        house = get_object_or_404(self.model, pk=pk)
        form = HouseForm(request.POST, instance = house)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)

class HouseDelete(LoginRequiredMixin, DeleteView):
    model = House
    success_url = reverse_lazy('wizards')
    template = 'wizards/house_confirm_delete.html'

    def get(self, request, pk) :
        house = get_object_or_404(self.model, pk=pk)
        form = HouseForm(instance=house)
        ctx = { 'house': house }
        return render(request, self.template, ctx)

    def post(self, request, pk) :
        house = get_object_or_404(self.model, pk=pk)
        house.delete()
        return redirect(self.success_url)
