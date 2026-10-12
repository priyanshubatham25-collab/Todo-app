from django.shortcuts import render,redirect,get_object_or_404
from .models import Task
# Create your views here.
def todo_list(request):
    task= Task.objects.all().order_by('-created_at')
    return render(request,'todo_list.html',{'tasks':task})  

def add_todo(request):
    if request.method == 'POST':
        title =request.POST.get('title','')
        description=request.POST.get('description','')
        if title:
            Task.objects.create(title=title,description=description)
            return redirect(todo_list)
        error="This is required"
        return render(request, 'add.html',{ 'error':error,'title':title,'description':description})
    return render(request,'add.html',{'title':'','description':''})

def edit_todo(request,pk):
    task = get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title','')
        description =request.POST.get('description','')
        if title:
            task.title=title
            task.description=description
            task.save()
            return redirect('todo_list')
        error='title is required'
        return render(request, 'add.html', {
            'task': task, 'error': error,
            'title_text': title, 'desc_text': description,})
    return render(request,'add.html', {
        'task': task,
        'title_text': task.title,
        'desc_text': task.description })
        

def delete_todo(request,pk):
    task = get_object_or_404(Task,pk=pk)
    if request.method=='POST':
        task.delete()
        return redirect('todo_list')
    return render(request,'delete.html',{'tasks':task})

def toggle_todo(request,pk):
    task = get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
    return redirect('todo_list')