from django.views.generic import ListView, DetailView, RedirectView, TemplateView
from django.views.generic.edit import UpdateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Route, Comment, Vote, NewsletterPost, Profile
from django.db.models import Count
from .forms import CommentForm, ProfileForm
from datetime import datetime


#User creation view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()
    return render(request, 'project/signup.html', {'form': form})


# List of all routes (current and archived)
class RouteListView(ListView):
    model = Route
    template_name = 'project/route_list.html'
    context_object_name = 'routes'
    paginate_by = 7

    def get_queryset(self):
        queryset = Route.objects.all()
        route_type = self.request.GET.get('type', '')
        v_min = self.request.GET.get('v_min', None)
        v_max = self.request.GET.get('v_max', None)

        # Filter by type
        if route_type:
            queryset = queryset.filter(type=route_type)
        
        # Filter by V-scale range
        if v_min is not None and v_max is not None:
            try:
                v_min = int(v_min)
                v_max = int(v_max)
                queryset = queryset.filter(
                    difficulty__gte=v_min,
                    difficulty__lte=v_max
                )
            except ValueError:
                pass  # Ignore invalid integer inputs

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['route_types'] = Route.TYPE_CHOICES
        context['v_min'] = self.request.GET.get('v_min', 0)
        context['v_max'] = self.request.GET.get('v_max', 13)
        return context

# Details for a single route, with comment form
class RouteDetailView(DetailView):
    model = Route
    template_name = 'project/route_detail.html'
    context_object_name = 'route'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        route = self.object

        # Check if the route is archived
        context['is_archived'] = route.status == 'archived'

        if route.status == 'archived':
            context['user_liked_route'] = False
            context['user_liked_comments'] = {}
            context['comment_form'] = None
        else:
            # If not archived, allow user actions
            user_liked_route = False
            if self.request.user.is_authenticated:
                profile = getattr(self.request.user, 'project_profile', None)
                if profile:
                    user_liked_route = profile.completed_routes.filter(pk=route.pk).exists()

            if self.request.user.is_authenticated:
                user_liked_comments = {
                    comment.id: comment.likes.filter(id=self.request.user.id).exists()
                    for comment in route.comments.all()
                }
            else:
                user_liked_comments = {}

            # Fetch top-level comments
            top_level_comments = route.comments.filter(parent__isnull=True).order_by('-created_at')

            context.update({
                'user_liked_route': user_liked_route,
                'user_liked_comments': user_liked_comments,
                'comment_form': CommentForm(),
                'top_level_comments': top_level_comments,
            })
        return context
    
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Ensure unauthenticated users are redirected to login

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.route = self.get_object()
            comment.save()
            return redirect('route-detail', pk=comment.route.pk)  # Redirect after successful comment
        else:
            # Reload the detail page with errors if the form is invalid
            return self.get(request, *args, **kwargs)

# "Like" a current route
class CompleteRouteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        route = get_object_or_404(Route, pk=kwargs['route_id'], status='current')
        profile = request.user.project_profile
        if route in profile.completed_routes.all():
            profile.completed_routes.remove(route)  # Unmark as completed
            completed = False
        else:
            profile.completed_routes.add(route)  # Mark as completed
            completed = True

        return JsonResponse({
            'completed': completed,
            'completed_count': route.completed_by.count(),
        })  


# Vote for an archived route
class VoteRouteView(LoginRequiredMixin, RedirectView):
    def post(self, request, *args, **kwargs):
        route = get_object_or_404(Route, pk=kwargs['route_id'], status='archived')
        if not Vote.objects.filter(route=route, user=request.user).exists():
            Vote.objects.create(route=route, user=request.user)
            messages.success(request, f'Your vote for {route.name} has been recorded!')
        else:
            messages.error(request, 'You have already voted for this route.')
        return redirect('route-list')

class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)  # Unlike the comment
            liked = False
        else:
            comment.likes.add(request.user)  # Like the comment
            liked = True
        return JsonResponse({'liked': liked, 'like_count': comment.likes.count()})
    
class LandingPageView(TemplateView):
    template_name = 'project/landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = NewsletterPost.objects.all().order_by('-created_at')
        
        if self.request.user.is_authenticated:
            user_liked_posts = {
                post.id: post.likes.filter(id=self.request.user.id).exists()
                for post in posts
            }
        else:
            user_liked_posts = {}

        context.update({
            'newsletter_posts': posts,
            'user_liked_posts': user_liked_posts,
        })
        return context

class LikeNewsletterView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(NewsletterPost, pk=kwargs['newsletter_id'])
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'like_count': post.likes.count()})
    
class ContactPageView(TemplateView):
    template_name = 'project/contact_us.html'

class ArchivedVotingView(TemplateView):
    template_name = 'project/archived_voting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Annotate the archived routes with the number of votes
        context['archived_routes'] = (
            Route.objects.filter(status='archived')
            .annotate(vote_count=Count('votes'))
            .order_by('-vote_count')
        )
        # Add the voting deadline
        context['voting_deadline'] = datetime(2024, 12, 31).strftime('%B %d, %Y') 
        return context
    
class ProfileView(DetailView):
    model = Profile
    template_name = 'project/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.project_profile
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'project/edit_profile.html'

    def get_object(self):
        return self.request.user.project_profile

    def get_success_url(self):
        return self.request.user.project_profile.get_absolute_url()
    
class ReplyCommentView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        parent_comment = get_object_or_404(Comment, id=comment_id)
        content = request.POST.get('content', '').strip()
        if content:
            # Create a new reply linked to the parent comment
            Comment.objects.create(
                user=request.user,
                route=parent_comment.route,
                content=content,
                parent=parent_comment,
            )
        return redirect('route-detail', pk=parent_comment.route.id)