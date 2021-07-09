from django.urls import path
from .views import AgentCreate, AgentDelete, AgentDetail, AgentList, AgentUpdate
app_name = 'agent'

urlpatterns = [
    path('', AgentList.as_view(), name='agent_list'),
    path('agent_list/', AgentList.as_view(), name='agent_list'),
    path('agent_create/', AgentCreate.as_view(), name='agent_create'),
    path('agent_detail/<pk>', AgentDetail.as_view(), name='agent_detail'),
    path('agent_update/<pk>', AgentUpdate.as_view(), name='agent_update'),
    path('agent_delete/<pk>', AgentDelete.as_view(), name='agent_delete'),
]
