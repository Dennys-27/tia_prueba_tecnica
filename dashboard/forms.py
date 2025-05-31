from django import forms

class login(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'autocomplete': 'current-password'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega 'is-invalid' a inputs con error para que Bootstrap marque el borde rojo
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = existing_classes + ' is-invalid'



# FORMULARIO DE VENTAS
class VentasForm(forms.Form):
    row_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )

    order_id = forms.CharField(
        label='ID de Pedido',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el ID del pedido'
        })
    )

    order_date = forms.DateField(
        label='Fecha del Pedido',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la fecha del pedido (YYYY-MM-DD)',
            'type': 'date'
        })
    )

    ship_date = forms.DateField(    
        label='Fecha del Shipping',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la fecha del shipping (YYYY-MM-DD)',
            'type': 'date'
        })
    )    

    ship_mode = forms.CharField(
        label='Modo de Envío',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el modo de envío'
        })
    )

    customer_id = forms.CharField(
        label='ID del Cliente',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el ID del cliente'
        })
    )
    customer_name = forms.CharField(
        label='Nombre del Cliente',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del cliente'
        })
    )

    segment = forms.CharField(  
        label='Segmento',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el segmento del cliente'
        })
    )

    country = forms.CharField(
        label='País',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el país del cliente'
        })
    )

    city = forms.CharField(
        label='Ciudad',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la ciudad del cliente'
        })
    )

    state = forms.CharField(
        label='Estado',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el estado del cliente'
        })
    )

    postal_code = forms.CharField(
        label='Código Postal',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el código postal del cliente'
        })
    )




    product_id = forms.CharField(
        label='ID del Producto',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el ID del producto'
        })
    )

    category = forms.CharField(     
        label='Categoría',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la categoría del producto'
        })
    )

    region = forms.CharField(
        label='Región',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la región del cliente'
        })
    )   

    sub_category = forms.CharField( 
        label='Subcategoría',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la subcategoría del producto'
        })
    )

    product_name = forms.CharField(
        label='Nombre del Producto',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del producto'
        })
    )

    sales = forms.DecimalField( 
        label='Ventas',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el monto de ventas'
        })
    )


    fields = '__all__'