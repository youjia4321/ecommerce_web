from django import forms


class CommentForm(forms.Form):
    email = forms.EmailField(label='邮箱', error_messages={
        'required': '请填写您的邮箱',
        'invalid': '邮箱格式不正确'
    })
    content = forms.CharField(label='内容', max_length=300, error_messages={
        'required': '请填写您的评论内容!',
        'max_length': '评论内容太长咯'
    })