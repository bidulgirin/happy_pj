from django.contrib import admin
from happyTest.models import *



# 행복테스트에서 바로 질문항목 만들것임   
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True  
    
    
# 질문항목의 옵션들을 바로편집
class OptionInline(admin.TabularInline):
    model = Option
    extra = 1 
  
     
@admin.register(HappyTest)
class HappyTestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

# 보기 편하게 하기
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("happy_test", "text") 
    inlines = [OptionInline]
    def question_title(self, obj):
        return obj.happy_test.title
    question_title.short_description = "제목"
    
    
admin.site.register(Option)
admin.site.register(Result)
admin.site.register(VideoSolution)
admin.site.register(BookSolution)
