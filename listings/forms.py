from django import forms
from listings import models


class NewListingForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'city', 'state', 'address',  'description', 'price', 'bedrooms', 'sqft', 'photo_main']
        model = models.Listing

    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Название объявления'
        self.fields['city'].label = 'Город'
        self.fields['state'].label = 'Район'
        self.fields['address'].label = 'Адрес'
        self.fields['description'].label = 'Описание'
        self.fields['price'].label = 'Сумма аренды за месяц'
        self.fields['bedrooms'].label = 'Количество спален'
        self.fields['sqft'].label = 'Площадь квартиры в квадратных метрах'
        self.fields['photo_main'].label = 'Фотография'
        self.fields['photo_main'].required = False


class DeployingForm(forms.Form):
    rentLength = forms.IntegerField(label='Длительность аренды')
    private_key = forms.CharField(max_length=100, label='Ваш приватный ключ',
                                  help_text='Никому не сообщайте свой ключ, злоумышленники могу забрать ваши деньги!', widget=forms.PasswordInput)


class PayForm(forms.Form):
    private_key = forms.CharField(max_length=100, label='Ваш приватный ключи' , help_text='Никому не сообщайте свой ключ, злоумышленники могу забрать ваши деньги!')


class TerminationForm(forms.Form):
    private_key = forms.CharField(max_length=100, label='Ваш приватный ключи' , help_text='Никому не сообщайте свой ключ, злоумышленники могу забрать ваши деньги!')












