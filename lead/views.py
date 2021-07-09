from django.db.models import query
from django.db.models.query import QuerySet
from django.forms import forms
from django.shortcuts import render, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list import ListView
from .models import Lead, Category
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AssignAgentForm, LeadForm, CustmusercreationForm, CategoryModelForm
from django.template import RequestContext, context
from django.core.mail import send_mail
from agent.mixins import OrganisrorLoginRequiredMixin
# Create your views here.


class Signupviews(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustmusercreationForm

    def get_success_url(self):
        return reverse('login')


class home(generic.TemplateView):
    template_name = 'home.html'


class LeadListviews(LoginRequiredMixin, generic.ListView):
    template_name = 'lead/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, agent__isnull=False)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListviews, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                'unassigned_leads': queryset
            })
        return context


class LeadDetailviews(LoginRequiredMixin, generic.DetailView):
    template_name = 'lead/lead_detail.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

    def lead_detail(request, pk):
        leads = Lead.objects.get(id=pk)
        return render(request, 'lead/lead_detail.html', {{'leads': leads}})


class LeadCreateviews(OrganisrorLoginRequiredMixin, generic.CreateView):
    template_name = 'lead/lead_create.html'
    form_class = LeadForm

    def get_success_url(self):
        return reverse('leads:lead_list')

    def form_valid(self, form):
        send_mail(
            subject='A lead has bean created',
            message='Go to side see the new lead',
            from_email='test23@gmail.com',
            recipient_list=['test12@gmail.com']
        )
        return super(LeadCreateviews, self).form_valid(form)


class LeadUpdateviews(OrganisrorLoginRequiredMixin, generic.UpdateView):
    template_name = 'lead/lead_update.html'
    form_class = LeadForm

    def lead_update(request, pk):
        lead = Lead.objects.get(id=pk)
        return render(request, 'lead/lead_update.html', {{'leads': lead}})

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse('lead:lead_list')


class LeadDeleteviews(OrganisrorLoginRequiredMixin, generic.DeleteView):
    template_name = 'lead/lead_delete.html'
    queryset = Lead.objects.all()
    forms_class = LeadForm

    def lead_update(request, pk):
        lead = Lead.objects.all()
        return render(request, 'lead/lead_delete.html', {{'leads': lead}})

    def get_success_url(self) -> str:
        return reverse('lead:lead_list')


class AssignagentView(OrganisrorLoginRequiredMixin, generic.FormView):
    template_name = "lead/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignagentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead_list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignagentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'lead/category_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "lead/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryUpdateView(OrganisrorLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset
