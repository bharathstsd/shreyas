from django.urls import path
from .views import coach_dashboard, client_profile, add_client, convert_to_coach, login_view, logout_view, celebration_view, tv_leaderboard, search_people, quick_checkin
urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("coach/<slug:slug>/", coach_dashboard, name="coach_dashboard"),
    path("person/<slug:slug>/", client_profile, name="client_profile"),
    path("coach/<slug:slug>/add-client/", add_client, name="add_client"),
    path("person/<slug:slug>/make-coach/", convert_to_coach, name="convert_to_coach"),
    path("celebrate/<slug:slug>/", celebration_view, name="celebration"),
    path("coach/<slug:slug>/leaderboard/", tv_leaderboard, name="tv_leaderboard"),
    path("search-people/", search_people, name="search_people"),
    path("coach/<slug:slug>/quick-checkin/",quick_checkin,name="quick_checkin"),
    


]
from .views import coach_leaderboard, tvs_leaderboard

urlpatterns += [
    path(
        "leaderboards/coach/<slug:slug>/",
        coach_leaderboard,
        name="coach_leaderboard"
    ),
    path(
        "leaderboards/tv/<slug:slug>/",
        tvs_leaderboard,
        name="tvs_leaderboard"
    ),
]
