from django.urls import path
from .views import CourseListView, CourseDetailView, CourseCreateView, CourseDeleteView, CourseUploadView, CourseUpdateView, EvalWeightForm, CourseCategoryForm, StudentDetailView, CourseGradelineForm
from . import views


urlpatterns = [
    path('', CourseListView.as_view(), name="stats-home"),
    path('about/', views.about, name="stats-about"),
    path('demo/', views.demo, name="stats-demo"),
    path('curves/', views.curves, name="stats-curves"),
    path('course/<int:pk>/', CourseDetailView.as_view(), name="course-detail"),
    path('course/<int:pk>/delete', CourseDeleteView.as_view(), name="course-delete"),
    path('course/<int:pk>/upload', CourseUploadView.as_view(), name="course-upload"),
    path('course/<int:pk>/update', CourseUpdateView.as_view(), name="course-update"),
    path('course/<int:pk>/weights', EvalWeightForm.as_view(), name="course-config"),
    path('course/<int:pk>/categories', CourseCategoryForm.as_view(), name="course-categories"),
    path('course/<int:pk>/gradelines', CourseGradelineForm.as_view(), name="course-gradelines"),
    path('student/<int:pk>/', StudentDetailView.as_view(), name="student-detail"),
    path('course/create/', CourseCreateView.as_view(), name="course-create"),
]
