from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# import the Todo model from the models file
from .models import Todo

def all_todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todos/all_list.html', {'todos': todos})

@login_required
def todo_list(request):
    if request.method == 'GET': # if its a GET request, just display the todos/add.html template
        user = request.user
        todos = Todo.objects.filter(user = request.user)  # get all of the todos from the database and store them in todos
        # create the context dictionary to send the todos to the template
        context = {
            'todos': todos,
            'user': user
        }
        return render(request, 'todos/list.html', context) # context is sent to 'todos/list.html'
    elif request.method == 'POST': # if it's a POST request ...
        title = request.POST['title']   # get the title from the POST submission, this comes form a form
        text = request.POST['text']     # get the text from the POST submission, this comes form a form
        if (request.POST['status'] == 'False'): # check the status because it's a string and booleans are not strings
            status = False
        else:
            status = True
        # add the new todo to the databse. objects.create() automatically saves the new todo for us so we
        # don't need a separate call to the save() method
        todo = Todo.objects.create(title = title, text = text, status = status, user = request.user)
        return redirect('list')


@login_required
def details(request, id):
    todo = Todo.objects.get(id = id)
    return render(request, 'todos/detail.html', {"todo": todo})


# view add a todo to the database. this view handles both GET and POST HTTP requests
@login_required
def add_todo(request):
    if request.method == 'GET': # if its a GET request, just display the todos/add.html template
        return render(request, 'todos/add.html')
    elif request.method == 'POST': # if it's a POST request ...
        title = request.POST['title']   # get the title from the POST submission, this comes form a form
        text = request.POST['text']     # get the text from the POST submission, this comes form a form
        user = request.user
        if (request.POST['status'] == 'False'): # check the status because it's a string and booleans are not strings
            status = False
        else:
            status = True
        # add the new todo to the databse. objects.create() automatically saves the new todo for us so we
        # don't need a separate call to the save() method
        todo = Todo.objects.create(title = title, text = text, status = status, user = request.user)
        return redirect('list')


# view to remove a specific todo from the database specified by its id
@login_required
def remove_todo(request, id):
    todo = Todo.objects.get(id = id)
    todo.delete()
    return redirect('list')

# helper function for updating a todo. gets the todo info specified by the id and redirects to its detail page
@login_required
def update_todo(request, id):
    todo = Todo.objects.get(id = id)
    return redirect('details', todo.id)

# view to update a todo in the databse specified by its id
@login_required
def update(request, id):
    todo = Todo.objects.get(id = id)
    if request.method == 'GET':
        return render(request, 'todos/update.html', {'todo': todo})
    elif request.method == 'POST':
        todo.title = request.POST['title']
        todo.text = request.POST['text']
        if (request.POST['status'] == 'False'):
            todo.status = False
        else:
            todo.status = True
        todo.save()
        return redirect('details', todo.id)


# mark a todo as done
@login_required
def mark_done(request, id):
    todo = Todo.objects.get(id = id)
    todo.status = True
    todo.save()

    return redirect('list')