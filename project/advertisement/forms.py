from django import forms
from .models import Advertisement, Response

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category', 'images', 'video_url']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        title = cleaned_data.get("title")
        if content and len(content) < 20:
            self.add_error('content', 'Содержание не может быть меньше 20 символов')

        if title and len(title) < 5:
            self.add_error('title', 'Заголовок должен содержать не менее 5 символов')

        return cleaned_data
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }