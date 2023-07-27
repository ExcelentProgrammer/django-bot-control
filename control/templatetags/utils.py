from django import template

register = template.Library()


@register.filter
def getf(num1, num2):
    try:
        return (int(num2) / int(num1)) * 100
    except Exception as e:
        print(e)
        return 0
