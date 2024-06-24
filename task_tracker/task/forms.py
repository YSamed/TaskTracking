from django import forms
from .models import Task, Category, Project

# Proje oluşturma formu
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }

# Görev oluşturma formu
class TaskForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.user = user 

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-select'})
        }

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category and category.user != self.user:
            raise forms.ValidationError("Bu kategoriye erişim izniniz yok.")
        return category

# Kategori oluşturma formu
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
