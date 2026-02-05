from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),


    path('questions/', include("questions.urls")),
    path('accounts/', include("accounts.urls")),
    path('calendar/', include("calendar_app.urls")),
    path('', include("tasks.urls")), 
]
