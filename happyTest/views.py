import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from happyTest.models import HappyTest, Question, Option, Result, VideoSolution , BookSolution
from django.core.exceptions import ValidationError

## 필요한 모듈 import~ 

# 
import time
import requests

# beautifulsoup
from bs4 import BeautifulSoup

# selenium
import selenium

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# 출처: https://mooonstar.tistory.com/entry/PythonBeautifulSoupbs4를-사용하여-웹-스크래핑하기 [MoonStar:티스토리]


# 테스트페이지
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
        return JsonResponse({"url": f"/result/{result_data.id}/"})
    else:   
        return redirect('start')
    
# 결과 페이지    
def result(request, id):
    result = Result.objects.get(id=id)
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
        
        print("solutions", solution)
    # 보통
    elif result.total_score < 70 :
         text = "행복지수가 보통이에요"
    # 좋음
    else:
        text = "행복지수가 높아요"
    
    
    # 결과에 따라 솔루션 데이터 달라짐
    context = {
        "result" : result,
        "solutions" : solution[:10],
        "text" : text,
    }
    
    return render(request, "./result.html", context)


# 비디오 솔루션 크롤링하는함수
def vidio_solution(request):
    # 관리자 아니면 쫓아내기
    user = request.user.is_authenticated  
    if user:
        print("관리자확인")
    else:
        return redirect("/")

    if request.method == "POST": 
        if request.POST["keyword"]:
            keyword = request.POST["keyword"]
            age = int(request.POST["age"])
            
        else:
            return # 키워드 없으면 동작시키지 말어라~~
        url = "https://www.youtube.com"
        driver = webdriver.Chrome()
        driver.set_window_size(1200, 1200)

        # 홈페이지 열것이야
        driver.get(url=url)
        # 기다리는 시간
        wait_time = .5

        # 살짝 기다려요
        time.sleep(wait_time)

        # 검색함
        try : 
            # 검색창 찾아요
            element = driver.find_element(By.CLASS_NAME, 'ytSearchboxComponentInput')
            # 키워드 입력해요
            time.sleep(wait_time)
            element.send_keys(keyword)
            # 검색어가 입력되는 시간 고려
            time.sleep(wait_time)
            # 엔터키
            element.send_keys(Keys.ENTER)
            
        except Exception as e:
            print(e)

        time.sleep(wait_time + 3)

        # "동영상만 나오도록 필터 클릭" ==================================
        try : 
            # 동영상 필터를 하기위함
            filter = "동영상"
            element = driver.find_element(By.ID, "chips").find_element(By.XPATH, ".//*[contains(.,'" + filter + "')]")
            # 아아ㅏ아아아아아!!! 된다!!!!
            time.sleep(wait_time + 2)
            element.click()
            # 해당요소 클릭함
        except Exception as e:
            print(e)

        time.sleep(wait_time + 5)
        
        driver.execute_script("document.body.style.zoom='10%'")# 이 구세주다...아....아....
        # 꽃 같은 화면 로딩을 해결하는 좋은 수단 이었습니다...

        # 영싱들을 수집합니다...
        # 3000px 만 스크롤
        finish_line = 1000
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            # 우선 스크롤 내리기
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(wait_time + 2) # 화면에 보이는 애들만 src 를 가져오기 때문에 다른 조치가 필요하다 모든 요소를 화면에서 봐야한다는점
            # 현재 위치 담기
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            
            # 과거의 길이와 현재 위치 비교하기
            if new_page_height > finish_line:
                break
            else: 
                last_page_height = new_page_height
            
        # bs4 로 페이지 소스를 가져올꺼여
        time.sleep(wait_time)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup = soup.body
        
        
        datas = []
        video_list = soup.select("ytd-video-renderer")
        for video in video_list:
            # 장고에서 VideoSolution 라는 모델에 넣을것들 선언하고 모델 객체를 넣어야 bulk_create 가능~~
            try: 
                datas.append(
                    VideoSolution(
                        keyword = keyword,
                        age = age,
                        title = video.select_one("a#video-title").get_text().strip(),
                        video_url = url + video.select_one("a#thumbnail").get("href",""),
                        thumbnail_url = video.select_one("a#thumbnail img.ytCoreImageHost").get("src",None),
                    )
                )
            except:
                print("악!")
                
        # 모델에 한번에 저장 하이소
        VideoSolution.objects.bulk_create(datas)
        
        result_datas = VideoSolution.objects.filter(keyword=keyword)
        context = {
            "result_datas" : result_datas
        }
        # 웹 드라이버 종료
        driver.quit()
        return render(request, "./solution_page.html", context)

    return render(request, "./solution_page.html")