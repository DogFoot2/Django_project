from django.forms import ModelForm
from django import forms
from third.models import Restaurant, Review
from django.utils.translation import gettext_lazy as _

REVIEW_POINT_CHOICES = {
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
}   # 평점의 선택지 정의

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['point', 'comment', 'restaurant']
        labels = {
            'point': _('평점'),
            'comment': _('코멘트'),
        }
        help_texts = {
            'point': _('평점을 입력해 주세요.'),
            'comment': _('코멘트를 입력해 주세요.'),
        }
        
        widgets = { #장고에 있는 widgets 사용해서 필드 속성을 직접 선택해서 렌더링
            'restaurant': forms.HiddenInput(),  # 리뷰를 달 식당 정보는 사용자에게 보여지지 않도록
            'point': forms.Select(choices=REVIEW_POINT_CHOICES) # 선택지를 인자로 전달
        }
        

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'image', 'password']
        labels = {
            'name': _('이름'),
            'address': _('주소'),
            'image': _('이미지 url'),
            'password': _('게시물 비밀번호'),
        }
        help_texts = {
            'name': _('이름을 입력해 주세요.'),
            'address': _('주소를 입력해 주세요.'),
            'image': _('이미지에 url을 입력해 주세요.'),
            'password': _('게시물 비밀번호를 입력해 주세요.'),
        }
        widgets = {
            'password': forms.PasswordInput()
            # 비밀번호칠 때 글자가 가려지는 필드
        }
        error_messages = {
            'neme': {
                'max_length': _("이름이 너무 깁니다. 30자 이하로 해 주세요."),
            },
            'image': {
                'max_length': _("이미지 주소의 길이가 너무 깁니다. 500자 이하로 해 주세요."),
            },
            'password': {
                'max_length': _("비밀번호가 너무 깁니다. 20자 이하로 해 주세요."),
            },
        }
        
        
class UpdateRestaurantForm(RestaurantForm): # 기존 레스토랑폼 상속받음
    class Meta:
        model = Restaurant
        exclude = ['password']
        #상속받은 레스토랑폼에서 패스워드만 업데이트하지않겠다고 include로 선언