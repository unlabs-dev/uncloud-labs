from django.shortcuts import render, redirect, get_object_or_404
from .models import Issue, Comment
from .forms import IssueForm, CommentForm


def issue_list(request):
    """Display list of all issues with optional status filtering."""
    issues = Issue.objects.all()

    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        issues = issues.filter(status=status_filter)

    context = {
        'issues': issues,
        'status_filter': status_filter,
    }
    return render(request, 'issues/issue_list.html', context)


def issue_detail(request, pk):
    """Display detailed view of a single issue with comments."""
    issue = get_object_or_404(Issue, pk=pk)
    comments = issue.comments.all()
    comment_form = CommentForm()

    context = {
        'issue': issue,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'issues/issue_detail.html', context)


def issue_create(request):
    """Create a new issue."""
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save()
            return redirect('issue_detail', pk=issue.pk)
    else:
        form = IssueForm()

    context = {
        'form': form,
        'form_title': 'Create New Issue',
        'submit_text': 'Create Issue',
    }
    return render(request, 'issues/issue_form.html', context)


def issue_edit(request, pk):
    """Edit an existing issue."""
    issue = get_object_or_404(Issue, pk=pk)

    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('issue_detail', pk=issue.pk)
    else:
        form = IssueForm(instance=issue)

    context = {
        'form': form,
        'form_title': f'Edit Issue: {issue.title}',
        'submit_text': 'Update Issue',
        'issue': issue,
    }
    return render(request, 'issues/issue_form.html', context)


def issue_delete(request, pk):
    """Delete an issue with confirmation."""
    issue = get_object_or_404(Issue, pk=pk)

    if request.method == 'POST':
        issue.delete()
        return redirect('issue_list')

    context = {
        'issue': issue,
    }
    return render(request, 'issues/issue_confirm_delete.html', context)


def comment_add(request, pk):
    """Add a comment to an issue."""
    issue = get_object_or_404(Issue, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.issue = issue
            comment.save()

    return redirect('issue_detail', pk=pk)
