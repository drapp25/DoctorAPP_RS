from .models import Publication

def recent_notifications(request):
    if request.user.is_authenticated:
        seguidos = request.user.siguiendo.all()
        recent_posts = Publication.objects.filter(autor__in=seguidos).order_by('-creado')[:2]
        return {'recent_notifications': recent_posts}
    return {}
