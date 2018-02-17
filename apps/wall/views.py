from django.contrib import auth
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.wall.forms import AddCommentForm, AddMessageForm
from apps.wall.models import Message, Comment


def logout(request):
    auth.logout(request)
    return redirect('wall:login')


def index(request):
    return render(request, 'index.html')


class Wall(ListView):
    model = Message
    template_name = 'wall/wall-msg.html'
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
                'date': self.object.posted,
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

    def get(self, request, *args, **kwargs):
        obj = Message.objects.get(id=self.kwargs['id'])
        if request.user == obj.author or request.user.is_staff:
            return super().get(request, *args, **kwargs)
        else:
            raise Http404

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
                'date': self.object.edited,
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

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().post(request, *args, **kwargs)
        else:
            raise Http404

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        try:
            self.object.parent = Comment.objects.get(pk=self.kwargs['pk'])
        except:
            self.object.parent = None
        self.object.message = Message.objects.get(id=self.kwargs['id'])
        self.object.save()
        if self.request.is_ajax():
            data = {
                'body': self.object.body,
                'author': self.object.author.username,
                'message': self.object.message.id,
                'date': self.object.posted,
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

    def get(self, request, *args, **kwargs):
        obj = Comment.objects.get(id=self.kwargs['id'])
        if request.user == obj.author or request.user.is_staff:
            return super().get(request, *args, **kwargs)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        obj = Comment.objects.get(id=self.kwargs['id'])
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
                'message': self.object.message.id,
                'date': self.object.posted,
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
