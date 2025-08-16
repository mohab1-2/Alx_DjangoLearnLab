
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import CommentForm

# Updated Post Detail View with Comments
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    
    # Paginate comments (10 per page)
    paginator = Paginator(comments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'post': post,
        'comments': page_obj,
        'comment_form': comment_form,
        'comment_count': comments.count()
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, 'Your comment has been added successfully!')
    else:
        messages.error(request, 'There was an error with your comment. Please try again.')
    
    return redirect('post_detail', pk=post_id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check if user is the author of the comment
    if comment.author != request.user:
        return HttpResponseForbidden("You can only edit your own comments.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated!')
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
        'post': comment.post
    }
    return render(request, 'blog/edit_comment.html', context)

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check if user is the author of the comment or post owner
    if comment.author != request.user and comment.post.author != request.user:
        return HttpResponseForbidden("You can only delete your own comments.")
    
    post_id = comment.post.pk
    comment.delete()
    messages.success(request, 'Comment has been deleted.')
    return redirect('post_detail', pk=post_id)

# AJAX view for real-time comment posting
@login_required
@require_POST
def ajax_add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'author': comment.author.username,
                'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p'),
                'can_edit': True,
                'can_delete': True
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })
