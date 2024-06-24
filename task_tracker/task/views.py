from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category, Project
from .forms import TaskForm, CategoryForm, ProjectForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Ana sayfa görünümü
def home(request):
    return render(request, 'home.html')

# Yeni proje oluşturma
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user 
            project.save()
            messages.success(request, 'Yeni proje başarıyla oluşturuldu.')
            return redirect('task:project_list')
    else:
        form = ProjectForm()
    return render(request, 'task/project_create.html', {'form': form})

# Projeleri listele
@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'task/project_list.html', {'projects': projects})

# Proje detaylarını gösterme ve yeni görev oluşturma
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Proje düzenleme formunu işle
    if request.method == 'POST' and 'edit_project' in request.POST:
        edit_project_form = ProjectForm(request.POST, instance=project)
        if edit_project_form.is_valid():
            edit_project_form.save()
            messages.success(request, 'Proje başarıyla güncellendi.')
            return redirect('task:project_detail', pk=pk)
    else:
        edit_project_form = ProjectForm(instance=project)

    # Proje silme işlemini işle
    if request.method == 'POST' and 'delete_project' in request.POST:
        project.delete()
        messages.success(request, 'Proje başarıyla silindi.')
        return redirect('task:project_list')

    # Yeni görev ekleme formunu işle
    if request.method == 'POST':
        form = TaskForm(user=request.user, data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project  # Görevi projeye bağlama
            task.user = request.user
            task.save()
            messages.success(request, 'Yeni Görev Oluşturuldu')
            return redirect('task:project_detail', pk=pk)
    else:
        form = TaskForm(user=request.user)

    tasks = Task.objects.filter(project=project)

    return render(request, 'task/project_detail.html', {
        'project': project,
        'form': form,
        'tasks': tasks,  # Projeye ait görevleri gönderme
        'edit_project_form': edit_project_form  # Proje düzenleme formunu gönderme
    })

# Proje düzenleme
@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proje başarıyla güncellendi.')
            return redirect('task:project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'task/project_edit.html', {'form': form, 'project': project})

# Proje silme
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Proje başarıyla silindi.')
        return redirect('task:project_list')
    return render(request, 'task/project_confirm_delete.html', {'project': project})


# Tüm görevleri listele  #KALDIRALCAK
@login_required
def task_list(request):
    user_categories = Category.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    selected_category = None

    if 'category_id' in request.GET:
        category_id = request.GET['category_id']
        if category_id:
            selected_category = get_object_or_404(Category, id=category_id)
            tasks = tasks.filter(category=selected_category)

    return render(request, 'task/task_list.html', {'tasks': tasks, 'user_categories': user_categories, 'selected_category': selected_category})

# Belirli bir görevin detaylarını gösterme
@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    form = TaskForm(instance=task)
    return render(request, 'task/task_detail.html', {'task': task, 'form': form})

# Yeni görev oluşturma 
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(user=request.user, data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Yeni Görev Eklendi')
            return redirect('task:task_list')  
    else:
        form = TaskForm(user=request.user)
    
    user_projects = Project.objects.filter(user=request.user)
    
    return render(request, 'task/task_create.html', {'form': form, 'user_projects': user_projects})


# Belirli bir görevi düzenleme
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Görev başarıyla güncellendi.')
            return redirect('task:project_detail', pk=task.project.pk)
    else:
        form = TaskForm(request.user, instance=task)
    return render(request, 'task/task_edit.html', {'form': form, 'task': task})

# Belirli bir görevi silme
@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    messages.success(request, 'Görev Tamamlandı', extra_tags='primary')
    return redirect('task:task_list')

# Yeni bir kategori oluşturma
@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('task:category_list')
    else:
        form = CategoryForm()
    return render(request, 'task/category_create.html', {'form': form})

# Tüm kategorileri listele ve kategori silme işlemini gerçekleştir
@login_required
def category_list(request):
    user_categories = Category.objects.filter(user=request.user)
    form = CategoryForm()
    
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        messages.success(request, 'Kategori başarıyla silindi.')
        return redirect('task:category_list')
    
    return render(request, 'task/category_list.html', {'user_categories': user_categories, 'form': form})

# Kullanıcının seçtiği kategoriye göre görevleri filtrele
@login_required
def task_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    tasks = Task.objects.filter(user=request.user, category=category)
    user_categories = Category.objects.filter(user=request.user) 
    return render(request, 'task/task_list.html', {'tasks': tasks, 'user_categories': user_categories, 'selected_category': category})
