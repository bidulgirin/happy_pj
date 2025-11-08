import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from happyTest.models import HappyTest, Question, Option, Result, VideoSolution , BookSolution
from django.core.exceptions import ValidationError
# Create your views here.
def start(request):
    # 전달할것
    # 총참여수, 질문, 질문옵션들
    questions = Question.objects.filter(happy_test__id=1).order_by("id")
    result_len = Result.objects.count()
    context = {
        "question" : questions,
        "result_len" : result_len
    }  
        
    return render(request, "./index.html", context)

# 결과 저장 =============================================
def save(request, q_id):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        a_type_score = int(data["a_type_score"])
        b_type_score = int(data["b_type_score"])
        c_type_score = int(data["c_type_score"])
        d_type_score = int(data["d_type_score"])
        e_type_score = int(data["e_type_score"])
        f_type_score = int(data["f_type_score"])
        
        # 공식도출예시
        a = a_type_score * 2
        b = b_type_score * 3
        c = c_type_score * 5
        d = d_type_score * 1
        e = e_type_score * 4
        f = f_type_score * 6
        
        total_score = data["total_score"]
        final_total_score = a + b + c + d + e + f
        
        happy_test = HappyTest.objects.get(id=q_id)
        
        try: 
            result_data = Result.objects.create(
                happyTest = happy_test, # 테스트번호
                age = int(data["age"]),
                a_type_score = a_type_score,
                b_type_score = b_type_score,
                c_type_score = c_type_score,
                d_type_score = d_type_score,
                e_type_score = e_type_score,
                f_type_score = f_type_score,
                
                final_a_type_score = a,
                final_b_type_score = b,
                final_c_type_score = c,
                final_d_type_score = d,
                final_e_type_score = e,
                final_f_type_score = f,
                
                total_score = total_score,
                final_total_score = final_total_score
        )
        except ValidationError as e:
            print(f"Validation error: {e.message_dict}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        print("저장됨.")    
        return JsonResponse({"url": f"/result/{result_data.id}/"})
    else:   
        return redirect('start')
    
   
def result(request, id):
    result = Result.objects.get(id=id)
    print("result", result)
    solution = VideoSolution.objects.all()
    
    # 좋음 보통 나쁨으로 10대, 20대, 30대...에 따라 다른 데이터
    
    # 나쁨
    if result.total_score < 50:
        text = "행복지수가낮아요"
        if result.age == 10:
            pass
        elif result.age == 20:
            pass
        elif result.age == 30:
            pass
        elif result.age == 40:
            pass
        elif result.age == 50:
            pass
        elif result.age == 60:
            pass
        elif result.age == 70:
            pass
        elif result.age >= 80:
            pass
        
        solutions = VideoSolution.objects.filter(age= result.age )
    # 보통
    elif result.total_score < 70 :
         text = "행복지수가 보통이에요"
    # 좋음
    else:
        text = "행복지수가 높아요"
    
    
    # 결과에 따라 솔루션 데이터 달라짐
    context = {
        "result" : result,
        "solutions" : solutions,
        "text" : text,
    }
    
    return render(request, "./result.html", context)