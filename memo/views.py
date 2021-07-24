from django.shortcuts import redirect, render
from .models import Post

# Create your views here.
from django import forms
from .models import Post
from django.utils import timezone
from django.db.models import Max


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)


def memo_list(request):
    incompletes = Post.objects.filter(status="未完了").order_by('order')
    completes = Post.objects.filter(status="完了").order_by('order')
    return render(request, 'memo/memo_list.html', {"incompletes": incompletes,
                                                   "completes": completes})


def add_item(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
            post.status = "未完了"
            post.created_data = timezone.now()
            order_max = Post.objects.filter(
                status="未完了").aggregate(Max('order'))["order__max"]
            post.order = order_max + 1 if order_max is not None else 1
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, 'memo/add_item.html', {"form": form})


def complete(request, item_id):
    item = Post.objects.get(pk=item_id)
    item.status = "完了"
    order_max = Post.objects.filter(
        status="完了").aggregate(Max('order'))["order__max"]
    item.order = order_max + 1 if order_max is not None else 1
    item.save()
    return redirect("home")


def incomplete(request, item_id):
    item = Post.objects.get(pk=item_id)
    item.status = "未完了"
    order_max = Post.objects.filter(
        status="未完了").aggregate(Max('order'))["order__max"]
    item.order = order_max + 1 if order_max is not None else 1
    item.save()
    return redirect("home")


def delete(request, item_id):
    item = Post.objects.get(pk=item_id)
    item.delete()
    return redirect("home")


def up(request, item_id):
    item = Post.objects.get(pk=item_id)
    if item.order > 1:
        item.order = item.order-1
        item_order = item.order
        replaced_item = Post.objects.get(order=item_order)
        replaced_item.order += 1
        item.save()
        replaced_item.save()
    return redirect("home")


def down(request, item_id):
    item = Post.objects.get(pk=item_id)
    if item.order < Post.objects.all().count():
        item.order = item.order+1
        item_order = item.order
        replaced_item = Post.objects.get(order=item_order)
        replaced_item.order -= 1
        item.save()
        replaced_item.save()
    return redirect("home")
