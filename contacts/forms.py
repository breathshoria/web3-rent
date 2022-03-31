from django import forms


class ContactForm(forms.Form):
    message = forms.CharField(label='Сообщение арендодателю')
    private_key = forms.CharField(max_length=100, label='Ваш приватный ключи' , help_text='Никому не сообщайте свой ключ, злоумышленники могу забрать ваши деньги!')