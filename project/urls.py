from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    LandingPageView,
    RouteListView,
    RouteDetailView,
    CompleteRouteView,
    VoteRouteView,
    LikeCommentView,
    signup,
    ContactPageView,
    LikeNewsletterView,
    ArchivedVotingView,
    ProfileView,
    EditProfileView,
    ReplyCommentView
)

urlpatterns = [
    # Main pages
    path('', LandingPageView.as_view(), name='landing-page'),  # Landing page
    path('routes/', RouteListView.as_view(), name='route-list'),  # Route list
    path('contact-us/', ContactPageView.as_view(), name='contact-us'),  # Contact page
    path('archived-voting/', ArchivedVotingView.as_view(), name='archived-voting'),  # Archived voting page

    # Route-specific actions
    path('route/<int:pk>/', RouteDetailView.as_view(), name='route-detail'),  # Route details
    path('route/<int:route_id>/complete/', CompleteRouteView.as_view(), name='complete-route'),
    path('route/<int:route_id>/vote/', VoteRouteView.as_view(), name='vote-route'),  # Vote for a route

    # Comment actions
    path('comment/<int:comment_id>/like/', LikeCommentView.as_view(), name='like-comment'),  # Like a comment
    path('comment/<int:comment_id>/reply/', ReplyCommentView.as_view(), name='reply-comment'), # Reply to a comment

    # Newsletter actions
    path('newsletter/<int:newsletter_id>/like/', LikeNewsletterView.as_view(), name='like-newsletter'),  # Like a newsletter post

    # User actions
    path('signup/', signup, name='signup'),  # Sign-up page
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
