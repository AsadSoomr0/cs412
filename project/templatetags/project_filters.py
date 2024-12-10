from django import template
import logging

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    return dictionary.get(key)

logger = logging.getLogger(__name__)
logger.debug("Custom template tags loaded")