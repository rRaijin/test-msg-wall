from django.contrib import auth
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.wall.forms import AddCommentForm, AddMessageForm
from apps.wall.models import Message, Comment


#  Логаут
def logout(request):
    auth.logout(request)
    return redirect('wall:login')

#  Домашняя страница для входа на сайт
def index(request):
    return render(request, 'index.html')


#  Вывод страницы стены сообщений
class Wall(ListView):
    model = Message
    template_name = 'wall/wall-msg.html'
    paginate_by = 2
    context_object_name = 'messages'
    queryset = Message.objects.all().order_by('-posted').prefetch_related('comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['AddCommentForm'] = AddCommentForm()
        context['AddMessageForm'] = AddMessageForm()
        return context


class AddMessage(CreateView):
    model = Message
    form_class = AddMessageForm
    template_name = 'wall/wall-msg.html'
    success_url = 'wall:msg-wall'

# Разрешение оставлять сообщения только для аутентифицированных пользователей
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        if self.request.is_ajax():
            data = {
                'id': self.object.id,
                'body': self.object.body,
                'author': self.object.author.username,
                'date': self.object.posted.strftime('%Y-%m-%d %H:%M'),
                'update_url': self.object.get_update_url(),
                'create_url': self.object.get_create_url(),
            }
            return JsonResponse(data)
        return redirect('wall:msg-wall')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class EditMessage(UpdateView):
    model = Message
    fields = ['body']
    template_name = 'wall/wall-msg.html'
    pk_url_kwarg = 'id'
    success_url = '/wall/'

# Разрешение на получение формы редактироавния только для автора сообщения и staff
    def get(self, request, *args, **kwargs):
        obj = Message.objects.get(id=self.kwargs['id'])
        if request.user == obj.author or request.user.is_staff:
            return super().get(request, *args, **kwargs)
        else:
            raise Http404

# Разрешение на редактироавние только для автора сообщения и staff
    def post(self, request, *args, **kwargs):
        obj = Message.objects.get(id=self.kwargs['id'])
        if request.user == obj.author or request.user.is_staff:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'body': self.object.body,
                'author': self.object.author.username,
                'date': self.object.edited.strftime('%Y-%m-%d %H:%M'),
                'update_url': self.object.get_update_url(),
                'create_url': self.object.get_create_url(),
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


# Разрешение на удаление только для staff
class MessageDelete(DeleteView):
    model = Message

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_staff:
            self.object.delete()
            return redirect('wall:msg-wall')
        else:
            raise Http404


class AddComment(CreateView):
    model = Comment
    fields = ['body']
    template_name = 'wall/wall-msg.html'
    success_url = 'wall:msg-wall'

# Разрешение комментировать только для аутентифицированных пользователей
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        try:  # Получить родительский комментарий или это нулевой коммент
            self.object.parent = Comment.objects.get(pk=self.kwargs['pk'])
        except:
            self.object.parent = None
        self.object.message = Message.objects.get(id=self.kwargs['id'])
        self.object.save()
        if self.request.is_ajax():  # Передача словаря в ajax
            data = {
                'body': self.object.body,
                'author': self.object.author.username,
                'message': self.object.message.id,
                'date': self.object.posted.strftime('%Y-%m-%d %H:%M'),
                'update_url': self.object.get_update_url(),
                'create_url': self.object.get_create_url(),
            }
            return JsonResponse(data)
        return redirect('wall:msg-wall')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class EditComment(UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'wall/wall-msg.html'
    pk_url_kwarg = 'id'
    success_url = '/wall/'

# Разрешение на получение формы редактироавния только для автора комментария и staff
    def get(self, request, *args, **kwargs):
        obj = Comment.objects.get(id=self.kwargs['id'])
        if request.user == obj.author or request.user.is_staff:
            return super().get(request, *args, **kwargs)
        else:
            raise Http404

# Разрешение на редактироавние только для автора комментария и staff
    def post(self, request, *args, **kwargs):
        obj = Comment.objects.get(id=self.kwargs['id'])
        if request.user == obj.author or request.user.is_staff:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():  # Передача словаря в ajax
            data = {
                'body': self.object.body,
                'author': self.object.author.username,
                'message': self.object.message.id,
                'date': self.object.edited.strftime('%Y-%m-%d %H:%M'),
                'update_url': self.object.get_update_url(),
                'create_url': self.object.get_create_url(),
            }
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


# Разрешение на удаление только для staff
class CommentDelete(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_staff:
            self.object.delete()
            return redirect('wall:msg-wall')
        else:
            raise Http404
