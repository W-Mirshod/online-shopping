from django import forms

from shopping.models import Comment, Order, User, Product, Category


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'message')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name', 'email', 'quantity')


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}), )

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'discount', 'rating', 'quantity', 'image', 'category')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)

    def clean_username(self):
        username = self.data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Number does not exist')
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.data.get('password')
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError('Password did not match')
        except User.DoesNotExist:
            raise forms.ValidationError(f'{username} does not exists')
        return password


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'This {username} is already registered')
        return username

    def clean_password(self):
        password1 = self.data.get('password')
        if not password1:
            raise forms.ValidationError('Passwords did not match')
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
