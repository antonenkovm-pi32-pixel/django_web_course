from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

# Create your views here.
class HomePageView(ListView):
    model = Post
    template_name='home.html'

class PostDetailView(DetailView):
    model = Post
    template_name='post_detail.html'

class PostCreateView(CreateView):
    model = Post
    template_name='post_new.html'
    fields = ['text', 'data', 'temperature', 'pressure', 'speed', 'probability', 'author']

class PostUpdateView(UpdateView):
    model = Post
    template_name='post_edit.html'
    fields = ['text', 'data', 'temperature', 'pressure', 'speed', 'probability']

class PostDeleteView(DeleteView):
    model = Post
    template_name='post_delete.html'
    success_url = reverse_lazy('home')