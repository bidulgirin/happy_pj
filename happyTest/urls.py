from django.urls import path
from happyTest import views

urlpatterns = [
    path("", views.start, name="start"),
    # 해피테스트 1
    path("save/<int:q_id>/", views.save, name="save"),
    # 각자 결과들
    path("result/<int:id>/", views.result, name="result"),
    # 비디오크롤링
    path("vidio_solution/", views.vidio_solution, name="vidio_solution"),
]