from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):

    return dictionary.get(key)


@register.filter
def lesson_type_class(value):

    if value == 'lecture':
        return 'lesson-type-lecture'
    elif value == 'lab':
        return 'lesson-type-lab'
    elif value == 'seminar':
        return 'lesson-type-seminar'
    elif value == 'practical':
        return 'lesson-type-practical'
    elif value == 'exam':
        return 'lesson-type-exam'
    elif value == 'consultation':
        return 'lesson-type-consultation'
    return ''
