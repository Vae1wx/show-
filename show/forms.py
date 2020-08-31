from django import forms
from ckeditor.widgets import CKEditorWidget
from mdeditor.fields import MDTextField
from .models import LoveLetter



class WriteForm(forms.Form):
    title = forms.CharField(label='起一个煽情的标题吧', required=True,  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '爱情不只是字里行间'}))
    school = forms.CharField(label='学校', required=True,  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '学校或是班级'}))
    like_name = forms.CharField(label='喜欢的人', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '喜欢的人'}))
    content = forms.CharField(label='阐述你的爱', required=True, widget=CKEditorWidget(
        config_name='comment_ckeditor'), error_messages={'required': '内容不可以是空的哦。'})
   

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(WriteForm, self).__init__(*args, **kwargs)

    def clean(self):
         # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_write(self):
        content = self.cleaned_data.get('content', '').strip()
        if content == '':
            raise forms.ValidationError('内容不能为空')
        return content


