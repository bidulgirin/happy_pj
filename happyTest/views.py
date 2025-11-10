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
    questions = Question.objects.filter(happy_test_id=1).order_by("id")
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
        age = int(data["age"])
        a_type_score = int(data["a_type_score"])
        b_type_score = int(data["b_type_score"])
        c_type_score = int(data["c_type_score"])
        # 사용안할듯
        d_type_score = 0
        e_type_score = 0
        f_type_score = 0
        
        # 공식도출예시
        a = a_type_score * 2.5 # 생존
        b = b_type_score * 2.5 # 관계
        c = c_type_score * 5 # 성장
        d = 0
        e = 0
        f = 0
        
        total_score = data["total_score"]
        final_total_score = a + b + c
        
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
    age = 0
    # 좋음 보통 나쁨으로 10대, 20대, 30대...에 따라 다른 데이터
    keywords = []
    if result.age == 10:
        keywords = ["가족관계", "인간관계"]
    elif result.age == 20:
        keywords = ["스트레스", "인간관계"]
    elif result.age == 30:
        keywords = ["가족관계"]
    elif result.age == 40:
        keywords = ["가족관계"]
    elif result.age == 50:
        keywords = ["가족관계"]
    elif result.age == 60:
        keywords = ["가족관계"]
    
    # 평균 행복지수는 10점 만점에 5.94점에서 6.68점
    
    # 나쁨
    if result.final_total_score < 59:
        text = "행복지수가 평균보다 낮아요"
        
    # 보통
    elif result.final_total_score < 66 :
         text = "행복지수가 보통이에요"
    # 좋음
    else:
        text = "행복지수가 높아요"
        
    a_type_low = None
    b_type_low = None
    c_type_low = None
    
    book_keyword = []
    # 개인 점수가 평균보다 낮을때
    if result.final_a_type_score < int(5.94 * 2.5):
        a_type_low = "개인"
        book_keyword += ["건강","외모"]
        
    if result.final_b_type_score < int(5.94 * 2.5):
        b_type_low = "관계"
        book_keyword += ["인간관계","가족"]
        
    if result.final_c_type_score < int(5.94 * 5):
        c_type_low = "성장"
        book_keyword += ["성장"]
        
    # 연령대별 키워드별 필터링
    solution = VideoSolution.objects.filter(age=result.age, keyword__in=keywords).order_by('?')[:6]
    # 책 정보를 넘긴다
    bookSolution = BookSolution.objects.filter(keyword__in=book_keyword).order_by('?')[:2]
    
    
    # 결과에 따라 솔루션 데이터 달라짐
    context = {
        "result" : result,
        "total_score" : int(result.final_total_score),
        "solutions" : solution[:6],
        "bookSolution" : bookSolution[:4],
        "text" : text,
        "a_type_low" : a_type_low,
        "b_type_low" : b_type_low,
        "c_type_low" : c_type_low,
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
        # 영싱들을 수집합니다...
        # 3000px 만 스크롤
        finish_line = 800
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
                thumbnail_url_dom = video.select_one("a#thumbnail img.ytCoreImageHost").get("src",None)
                if thumbnail_url_dom:
                    datas.append(
                        VideoSolution(
                            keyword = keyword,
                            age = age,
                            title = video.select_one("a#video-title").get_text().strip(),
                            video_url = url + video.select_one("a#thumbnail").get("href",""),
                            thumbnail_url = thumbnail_url_dom,
                        )
                    )
            except:
                print("악!")
                
        # 모델에 한번에 저장 하이소
        VideoSolution.objects.bulk_create(datas[:10]) # 용량부족하니까 10개로 잘라
        
        result_datas = VideoSolution.objects.filter(keyword=keyword)
        context = {
            "result_datas" : result_datas
        }
        # 웹 드라이버 종료
        driver.quit()
        return render(request, "./solution_page.html", context)

    return render(request, "./solution_page.html")

# 책 솔루션 크롤링하는함수
def book_solution(request):
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
        url = "https://product.kyobobook.co.kr/"

        driver = webdriver.Chrome()
        # 홈페이지 열것이야
        driver.get(url=url)
        # 기다리는 시간
        wait_time = .8

        # 살짝 기다려요
        time.sleep(wait_time)

        # 검색함
        try : 
            # 검색창 찾아요
            element = driver.find_element(By.ID, 'searchKeyword')
            # 기다려요
            time.sleep(wait_time)
            # 키워드 입력해요
            element.send_keys(keyword)
            # 검색어가 입력되는 시간 고려
            time.sleep(wait_time)
            # 엔터키 입력해요
            element.send_keys(Keys.ENTER)
            
        except Exception as e:
            print(e)

        time.sleep(wait_time + 3)
        #driver.execute_script("document.body.style.zoom='10%'")# 이 구세주다...아....아....
        time.sleep(wait_time)

        # 19세상품제외 필터를 하기위함
        try : 
            # 명시적대기
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "exclAgeOver")))
            filter_element = driver.find_element(By.ID, "exclAgeOver")
            time.sleep(wait_time + 2)
            filter_element.click()
        except Exception as e:
            print(e)

        time.sleep(wait_time + 5)
         # 추천 필터가 있을경우
        try :
            elements = driver.find_element(By.CLASS_NAME, "filter_list_box").find_elements(By.ID, "recommend_category_filter")
            time.sleep(wait_time + 2)
            if elements[0]:
                elements[0].parent.click()
        except Exception as e:
            print(e)

        time.sleep(wait_time + 5)
       
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup = soup.body
        # 책 리스트에서 값 뽑아올것임
        book_list = soup.select("ul.prod_list li.prod_item")
            
        datas = []
        if len(book_list) > 0:
            for book  in book_list:
            # 장고에서 VideoSolution 라는 모델에 넣을것들 선언하고 모델 객체를 넣어야 bulk_create 가능~~
                try: 
                    datas.append(
                        BookSolution(
                            keyword = keyword,
                            age = age,
                            title = book.select_one(".prod_name_group .prod_category + span").get_text().strip(),
                            book_url = book.select_one(".prod_info").get("href", ""),
                            cover_url = book.select_one(".prod_img_load").get("src", "")
                        )
                    )
                except:
                    print("악!")
                    
            # 모델에 한번에 저장 하이소
            BookSolution.objects.bulk_create(datas[:10])
            
            result_datas = BookSolution.objects.filter(keyword=keyword)

            context = {
                "result_datas" : result_datas
            }
            # 웹 드라이버 종료
            driver.quit()
            return render(request, "./solution_page.html", context)
    return render(request, "./solution_page.html")

# 질문 크롤링하는 함수(등록하는게더빠를듯?)
def option_create(request):
    if request.method == "POST":
        # 질문내용
        title = request.POST["title"]
        # 정방향인지 역방향인지
        score = int(request.POST["score"])
        option_type = request.POST["type"]
        option_list = ["매우그렇다","그렇다","보통이다","아니다","매우아니다"]
        
        # Question 에 다가 먼저 질문내용을 넣습니다
        question = Question.objects.create(
            happy_test = HappyTest.objects.get(id=1),
            text = title,
        )
        question.save()
        
        options = []
        
        # 정방향으로
        if score == 0:
            option_score_list = [0,1,2,3,4]
        # 역방향으로    
        else:
            option_score_list = [4,3,2,1,0]
            
        for idx, i in enumerate(option_list):
            options.append(
                Option(
                   question = Question.objects.get(id=question.id), 
                   text = i, 
                   score = option_score_list[idx], 
                   type = option_type, 
                )
            )
            
        Option.objects.bulk_create(options)
        
    question = Question.objects.filter(happy_test_id = 1) 
    context = {
        "question" : question
    }
    return render(request, "./option_create.html", context)
 # quetion 수정 삭제
 
def quetion_update(request,id):
    text = request.POST["text"]
    Question.objects.filter(id=id).update(text=text)
    return redirect("option_create")

def quetion_delete(request,id):
    Question.objects.get(id=id).delete()
    return redirect("option_create")

def option_update(request,id):
    text = request.POST.get("text")
    score = request.POST.get("score")
    Option.objects.filter(id=id).update(text=text, score=score)
    
    return redirect("option_create")
# option 수정 삭제
def option_delete(request,id):
    Option.objects.get(id=id).delete()
    return redirect("option_create")