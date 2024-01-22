from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, ProjectForm, TaskCreateForm, TestForm
from django.contrib.auth import login, authenticate
from .models import Project , Task, User, Post
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, FormView, TemplateView
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .forms import PostForm ,CommentForm, UpdateProfileForm
from django.db.models import Q


class qrange(CreateView):
    template_name = "qrange.html"
    form_class=['email pasword']
    success_url = reverse_lazy('home')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User(username=name, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'home.html', context)


class Registration (CreateView):
    template_name = 'registration.html'
    model = User
    #fields = ['username', 'email', 'password1', 'password']
    form_class = RegistrationForm
    success_url = reverse_lazy('home')


class LoginPage (LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user=True


class Create_project (CreateView):
    template_name = 'project_create.html'
    form_class = ProjectForm
    success_url = reverse_lazy('home')



def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/login')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'home.html', context)


def home (request):
    projects = Project.objects.all()
    context = {'projects': projects }
    return render(request, 'home.html', context)


class Home (ListView):
    template_name = 'home.html'
    model = Project
    paginate_by = 1
    #context object name 'projects'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.all()
        context['pages'] = len(projects)
        return context


def project(request):
    id = request.kwargs['id']
    project = Project.object.get(id=id)
    tasks = Task.object.filter(project=project)


def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            project = Project(name=name)
            project.save()
            return redirect('/')
    else:
        form = ProjectForm()
        return render(request, 'project_create.html', {'form': form})


def project(request, **kwargs):
    project = Project.objects.get(id=kwargs['id'])
    if request.method == "POST":
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            status = form.cleaned_data['status']
            deadline = form.cleaned_data['deadline']
            task = Task(text=text, status=status, deadline=deadline,project=project)
            task.save()
            return redirect('/')
    else:
        tasks = Task.objects.filter(project=project)
        form = TaskCreateForm()
        context = {'fore': form, 'tasks': tasks, 'project': project}
        return render(request, 'projects.html', context)


class Projects(CreateView):
    template_name = 'project_create.html'
    model = Project
    form_class = Project
    success_urt = reverse_lazy('home')


def edit_project(request, **kwargs):
    project = Project.objects.get(id=kwargs['id'])
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            project.name = name
            project.save()
            return redirect('/')
    else:
        form = ProjectForm()
        return render(request, 'project create.html', {'form', form})


class ProjectEditPage(UpdateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = ProjectForm
    success_url = reverse_lazy ('/')


class FormPage (FormView):
    template_name = 'form.html'
    form_class = TestForm
    success_url = reverse_lazy()

    def form_valid (self, form):
        response = HttpResponse()
        response.set_cookie('name', form.cleaned_data['name'])
        return super().form_valid(form)


class ProjectPage(TemplateView):
    template_name='project.html'


    def get_success_url(self):
        return f'/project/{self.kwargs["id"]}'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        project = Project.objects.get(id=self.kwargs['id'])
        context['project'] = project
        context['tasks'] = Task.objects.filter(project-project)
        context['form'] = TaskCreateForm()
        return context


    def post(self, request, **kwargs):
        data = request.POST
        project = Project.objects.get(id=self.kwargs['id'])
        task = Task(text=data['text'],status=data['status'],project=project,deadline=data['deadline'])
        task.save()
        return JsonResponse({ 'resp': 'OK'})


    def post(self, request):
        data = request.POST
        resp = render_to_string('response.html', {'name': data['name'],'email':data['email'],'password':data['password']})
        return JsonResponse (resp, safe=False)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def user_search(request):
    return render(request, 'search.html')


class SearchPage(TemplateView):
    template_name = 'search.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


    def post(self, request,):
        data = request.POST
        users = User.objects.filter(username__contains=data['text'])
        html = render_to_string('users.html', {'users': users})
        return JsonResponse(html, safe=False)


def profile(request, **kwargs):
    try:
        user = User.objects.get(**kwargs)
        post = Post.objects.filter(user=user)
    except User.DoesNotExist:
        user = None
        posts = None

    context = {
        'user': user,
        'posts': post,
    }

    return render(request, 'profile.html', context)


def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return render(request, 'post_not_found.html')

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', post_id=post.id)


def comment(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)

        if request.method == 'POST':
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()

                return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Invalid form submission'})

    except Post.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'}, status=404)


def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {'form': form})



