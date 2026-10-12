from django import forms

from .models import Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'audience', 'is_pinned']
        widgets = {'content': forms.Textarea(attrs={'rows': 5})}
