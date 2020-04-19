from slugify import slugify_ru

def generate_slug(nickname):
    if nickname is None:
        raise ValueError('Nickname can\'t be empty')
    else:
        return slugify_ru(nickname, to_lower=True)
