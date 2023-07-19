from django import template
register = template.Library()

@register.filter
def index_favorite(favorites, user_id):
    park_id = None  
    for favorite in favorites:
        if favorite.user.id == user_id:
            park_id = favorite.id
    return park_id