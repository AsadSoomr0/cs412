from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from .forms import CreateProfileForm
from .forms import CreateStatusMessageForm
from .forms import UpdateProfileForm
from .models import *

# Create your views here.
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_form'] = CreateStatusMessageForm()
        return context

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        sm = form.save(commit=False)  
        sm.profile = profile  

        sm.save()

        # Handle file uploads
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(status_message=sm, image_file=file)
            image.save()

        return super().form_valid(form)

    def get_success_url(self):
        profile_pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': profile_pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context
    
class UpdateProfileView(UpdateView): 
    #View inheriting django's generic updateview used to update profiles 
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class DeleteStatusMessageView(DeleteView):
    #View inheriting from django's generic deleteview, used to delete status messages
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    template_name = 'mini_fb/update_status_form.html'
    fields = ['message']

    def get_success_url(self):
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'