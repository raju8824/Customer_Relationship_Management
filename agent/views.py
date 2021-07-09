# from crm.lead.models import UserProfile
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import render
from lead.models import Agent
from django.views import generic
from .forms import AgentModelForm
from django.shortcuts import reverse
from .mixins import OrganisrorLoginRequiredMixin
# Create your views here.
import random


class AgentList(OrganisrorLoginRequiredMixin, generic.ListView):
    template_name = 'agent/agent_list.html'
    context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreate(OrganisrorLoginRequiredMixin, generic.CreateView):
    template_name = 'agent/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agent:agent_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f'{random.randint(0, 1000)}')
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        send_mail(
            subject='your invaited to be agent',
            message='your aad to be agent',
            from_email='test234@test.com',
            recipient_list=[user.email],
        )
        return super(AgentCreate, self).form_valid(form)


class AgentDetail(OrganisrorLoginRequiredMixin, generic.DetailView):
    template_name = 'agent/agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def agentdetail(request, pk):
        agent = Agent.objects.get(id=pk)
        return render(request, 'agen/agent_detail.html', {'agent': agent})


class AgentUpdate(OrganisrorLoginRequiredMixin, generic.UpdateView):
    template_name = 'agent/agent_update.html'
    form_class = AgentModelForm

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self) -> str:
        return reverse('agent:agent_list')

    def agent_update(request, pk):
        agent = Agent.objects.get(id=pk)
        return render(request, 'agent/agent_update', {'agent': agent})


class AgentDelete(OrganisrorLoginRequiredMixin, generic.DeleteView):
    template_name = 'agent/agent_delete.html'
    context_object_name = 'agent'

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def agent_delete(request, pk):
        agent = Agent.objects.get(id=pk)
        return render(request, 'agent/agent_delete.html', {'agent': agent})

    def get_success_url(self) -> str:
        return reverse('agent:agent_list')
