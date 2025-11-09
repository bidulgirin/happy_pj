from django.db import models

# 질문 모델 만들것임~~
# 질문에 대한것을 설정 근데 크롤링해서 끌어올거긴한데...
# 크롤링을 내가 정제해야하긴해...그거 점수도 어느정도 설정해야하고
# 공식이 아직 안나왔기 때문에 임의로 설정해야함

# 테스트 항목들 모델(여러개로 테스트 해보기 실제 올바른 결과가 나올때까지 할것이기 때문임)
class HappyTest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

# 질문 저장 모델
class Question(models.Model):
    happy_test = models.ForeignKey(HappyTest, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=300) # "당신은 행복합니까??" 이런거 담을것임

    def __str__(self):
        return f"{self.happy_test.title} ::: {self.text}" 

# 질문 선택 모델
# 매우그렇다 그렇지 않다 그렇다 매우그렇다 이렇게 선택할수있게 할것임(4문항 생각하고있음)
class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    score = models.IntegerField(default=0) # 중요!!! 해당 설문의 점수임 (0~5)
    type = models.CharField("타입", max_length=1) # a: 안전요소, b : 관계요소, c : 건강요소...이렇게 타입을 나눠서 합산을 달리할것임

    def __str__(self):
        return f"{self.text[:10]} 점수 :: {self.score} 타입 : {self.type}"
    
# 질문의 점수 * 중요도(가중치) = 평균 저장

# 테스트 완료를 누르면 저장될 데이터
class Result(models.Model): # 몇명이 참여했는지 표기할것임
    happyTest = models.ForeignKey(HappyTest, on_delete=models.CASCADE)
    age =  models.IntegerField(default=0) # 연령대
    # 항목별 점수 합산 (가중치계산안한것임!!!!)
    a_type_score = models.IntegerField(default=0) # 안전요소
    b_type_score = models.IntegerField(default=0) # 관계요소
    c_type_score = models.IntegerField(default=0) # 성장요소
    d_type_score = models.IntegerField(default=0) # 성장요소
    e_type_score = models.IntegerField(default=0) # 성장요소
    f_type_score = models.IntegerField(default=0) # 성장요소
    
    # 백엔드에서 계산하는게 더 맞음 ㅇㅇㅇㅇ
    final_a_type_score = models.FloatField(default=0) # 안전요소
    final_b_type_score = models.FloatField(default=0) # 관계요소
    final_c_type_score = models.FloatField(default=0) # 성장요소
    final_d_type_score = models.FloatField(default=0) # 안전요소
    final_e_type_score = models.FloatField(default=0) # 관계요소
    final_f_type_score = models.FloatField(default=0) # 성장요소
    
    # 다 더한 점수
    total_score = models.IntegerField(default=0)
    # 가중치까지 계산해서 백분율로 들어간 점수(사용자에게 보여줄용 )
    final_total_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"결과 {self.total_score}"
    
    
# 솔루션데이터!!! 데이터 수집!!!
class VideoSolution(models.Model):
    keyword = models.CharField("키워드", max_length=30, blank=True, null=True)
    title = models.CharField("제목", max_length=200)
    age =  models.IntegerField("나이", default=0)
    video_url = models.URLField("영상 링크")
    thumbnail_url = models.URLField("썸네일 링크", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title
    
class BookSolution(models.Model):
    keyword = models.CharField("키워드", max_length=30, blank=True, null=True)
    title = models.CharField("제목", max_length=200)
    age =  models.IntegerField("나이", default=0)
    book_url = models.URLField("링크")
    cover_url = models.URLField("사진 링크", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title