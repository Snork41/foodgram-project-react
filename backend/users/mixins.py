class IsSubscribedMixin:

    def is_subscribed(self, author):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.follower.filter(author=author).exists()
        return False
