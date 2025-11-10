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
    # 책크롤링
    path("book_solution/", views.book_solution, name="book_solution"),
    # 질문자동저장
    path("option_create/", views.option_create, name="option_create"),
    
    # quetion 수정 삭제
    path("quetion_delete/<int:id>/", views.quetion_delete, name="quetion_delete"),
    path("quetion_update/<int:id>/", views.quetion_update, name="quetion_update"),
    # option 수정 삭제
    path("option_delete/<int:id>/", views.option_delete, name="option_delete"),
    path("option_update/<int:id>/", views.option_update, name="option_update"),
]