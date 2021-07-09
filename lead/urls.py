from django.urls import path
from.views import AssignagentView, LeadCreateviews, LeadDeleteviews, LeadDetailviews, LeadListviews, LeadUpdateviews, CategoryListView, CategoryDetailView, CategoryUpdateView

app_name = 'leads'

urlpatterns = [
    path("lead_list/", LeadListviews.as_view(), name='lead_list'),
    path("lead_detail/<int:pk>", LeadDetailviews.as_view(), name='lead_detail'),
    path("category_detail/<int:pk>",
         CategoryDetailView.as_view(), name='category_detail'),
    path("lead_create/", LeadCreateviews.as_view(), name='lead_create'),
    path("category_list/", CategoryListView.as_view(), name='category_list'),
    path("assign_agent/<int:pk>", AssignagentView.as_view(), name='assign_agent'),
    path("lead_update/<int:pk>", LeadUpdateviews.as_view(), name='lead_update'),
    path("category_update/<int:pk>",
         CategoryUpdateView.as_view(), name='category_update'),
    path("lead_delete/<int:pk>", LeadDeleteviews.as_view(), name='lead_delete'),
]
