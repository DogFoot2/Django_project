from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    
    password = models.CharField(max_length=20, default=None, null=True)
    #디폴트속성 지정하지 않았을 때 이 속성 지정 전에 입력한 데이터들은 패스워드 없이 작동되기 위해 None 지정
    #Null 속성 따로 지정하지 않으면 필드를 무조건 채워줘야 하기 때문에 채워지지 않은 데이터들을 위해 Null값 허용해 주기
    image = models.CharField(max_length=500, default=None, null=True)
    # 이미지에 url을 넣을 거기 때문에 CharField
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Review(models.Model):
    point = models.IntegerField()
    comment = models.CharField(max_length=500)

    # 식당 모델과의 릴레이션 정의,
    # on_delete CASCADE로 지정하면 식당이 삭제되면 같이 삭제된다.
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)  # 글 작성 시 (이 모델의 데이터(레코드) 저장 시) 생성 시각
    updated_at = models.DateTimeField(auto_now=True)
