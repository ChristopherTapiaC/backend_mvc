from django import forms
from .models import Product, Client

BASE_INPUT = (
    "block w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 "
    "text-slate-800 placeholder-slate-400 shadow-sm "
    "focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
        labels = {'name': 'Nombre del producto', 'price': 'Precio'}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': BASE_INPUT, 'placeholder': 'Ej: Teclado mecánico RGB', 'autocomplete': 'off'
            }),
            'price': forms.NumberInput(attrs={
                'class': BASE_INPUT, 'step': '0.01', 'inputmode': 'decimal', 'placeholder': '19990.00'
            }),
        }
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price < 0:
            raise forms.ValidationError("El precio debe ser mayor o igual a 0.")
        return price

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']
        labels = {'name': 'Nombre', 'email': 'Email', 'phone': 'Teléfono'}
        widgets = {
            'name':  forms.TextInput(attrs={'class': BASE_INPUT, 'placeholder': 'Nombre completo', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'class': BASE_INPUT, 'placeholder': 'correo@dominio.com', 'autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={'class': BASE_INPUT, 'placeholder': '+56 9 1234 5678', 'autocomplete': 'tel', 'inputmode': 'tel'}),
        }

class AddItemForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by('name'),
        empty_label="Selecciona un producto...",
        widget=forms.Select(attrs={'class': BASE_INPUT})
    )
    quantity = forms.IntegerField(
        min_value=1, initial=1,
        widget=forms.NumberInput(attrs={'class': BASE_INPUT, 'min': '1', 'step': '1', 'inputmode': 'numeric', 'placeholder': '1'})
    )
