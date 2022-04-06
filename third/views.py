from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from third.models import Restaurant, Review
from django.core.paginator import Paginator
from third.forms import RestaurantForm, ReviewForm, UpdateRestaurantForm
from django.http import HttpResponseRedirect
from django.db.models import Count, Avg

# Create your views here.
def list(request):
    restaurants = Restaurant.objects.all().annotate(reviews_count=Count('review'))\
        .annotate(average_point=Avg('review__point')) #언더바 두개는 장고 규칙/ 속성명 써 주면 그부분 실행됨
    # annotate메소드에 counts{연산 결과를 저장할 속성명}  Count{ORM 연산 메소드}   'review'{relation 이름}
    paginator = Paginator(restaurants, 5) ## 한 페이지에 5개씩 표시
    
    page = request.GET.get('page')  ## third/list?page=1
    # query params에서 page 데이터를 가져옴
    items = paginator.get_page(page)
    context = {
        'restaurants': items ## 필터링을 한 아이템이라는 변수 넣어주기
    }
    return render(request, 'third/list.html', context)

def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)  # request의 POST 데이터들을 바로 PostForm에 담을 수 있습니다.
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크합니다.
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가합니다.
        return HttpResponseRedirect('/third/list/')  # 리스트 화면으로 이동합니다.
    form = RestaurantForm()
    return render(request, 'third/create.html', {'form': form})

def update(request):
    if request.method == 'POST' and 'id' in request.POST:   ##id가 request.POST에 있는지 확인해 주기
#        item = Restaurant.objects.get(pk=request.POST.get('id'))    #id값과 일치하는 데이터 가져오기
        item = get_object_or_404(Restaurant, pk=request.POST.get('id')) #에러가 페이지없음 화면으로만 뜨게 됨
        password = request.POST.get('password', '')
        form = UpdateRestaurantForm(request.POST, instance=item)     # NOTE: instance 인자(수정대상) 지정
        #request.POST로 초기화
        if form.is_valid() and password == item.password:
            item = form.save() # 데이터 저장
    elif request.method == 'GET':
#        item = Restaurant.objects.get(pk=request.GET.get('id')) ##third/update?id=2 이것도 바꿔주기
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))
        form =RestaurantForm(instance=item)
        return render(request, 'third/update.html', {'form': form})
    
    return HttpResponseRedirect('/third/list/') ##리스트 화면으로 이동


def detail(request, id):     # restaurant의 id (pk)를 직접 url path parameter을 통해 전달 받습니다.
    if id is not None:
        item = get_object_or_404(Restaurant, pk=id)
        reviews = Review.objects.filter(restaurant=item).all()  ## 위에 review 모델 선언(import)
        return render(request, 'third/detail.html', {'item': item, 'reviews':reviews})
    return HttpResponseRedirect('/third/list/')


def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    if request.method == 'POST' and 'password' in request.POST:
        if item.password == request.POST.get('password') or item.password is None :
            item.delete()
            return redirect('list')
        return redirect('restaurant-detail', id=id)
    return render(request, 'third/delete.html', {'item': item})  # 리스트 화면으로 이동


def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():  # 데이터가 form 클래스에서 정의한 조건 (max_length 등)을 만족하는지 체크
            new_item = form.save()  # save 메소드로 입력받은 데이터를 레코드로 추가\
        return redirect('restaurant-detail', id=restaurant_id)  # 레스토랑아이디 그대로 전달
    
    item = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(initial={'restaurant': item}) #미리 값을 채워주길 원하는 레스토랑을 넣어주기
    return render(request, 'third/review_create.html', {'form': form, 'item':item})


def review_delete(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)
    item.delete()
    
    return redirect('restaurant-detail', id=restaurant_id)


def review_list(request):
    reviews = Review.objects.all().select_related().order_by('-created_at')  #최신순 정렬
    # select_related() => 쿼리 하나로 정보를 전부 다 들고 옴(join)
    paginator = Paginator(reviews, 10)
    
    page = request.GET.get('page') # query params에서 page 데이터를 가져옴
    items = paginator.get_page(page)     # 해당 페이지의 아이템으로 필터링
    
    context = {
        'reviews': items
    }
    return render(request, 'third/review_list.html', context)
    