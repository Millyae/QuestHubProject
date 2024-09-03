from django import template

register = template.Library()

@register.filter
def censor(value):
    unwanted_words = ['удар', 'убийство', 'наркотики', 'насилие', 'смерть', 'стрельбу', 'выстрел', 'жертвы']
    censored_value = value
    for word in unwanted_words:
        if word in censored_value:
            word_length = len(word)
            censored_word = word[0] + '*' * (word_length - 2) + word[-1]
            censored_value = censored_value.replace(word, censored_word)

    return censored_value