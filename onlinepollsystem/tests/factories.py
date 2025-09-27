import factory
from users.models import User  # Import directly instead of get_user_model()
from polls.models import Poll, Option
from votes.models import Vote

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)

    username = factory.Sequence(lambda n: f'user{n}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        password = extracted or 'password123'
        self.set_password(password)
        self.save()

class PollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Poll
    
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text', max_nb_chars=200)
    created_by = factory.SubFactory(UserFactory)

class OptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Option
    
    option_text = factory.Faker('word')
    poll = factory.SubFactory(PollFactory)

class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote
    
    user = factory.SubFactory(UserFactory)
    poll = factory.SubFactory(PollFactory)
    option = factory.SubFactory(OptionFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Ensure the option belongs to the poll
        if 'poll' in kwargs and 'option' not in kwargs:
            poll = kwargs['poll']
            option = OptionFactory(poll=poll)
            kwargs['option'] = option
        elif 'option' in kwargs and 'poll' not in kwargs:
            kwargs['poll'] = kwargs['option'].poll
            
        return super()._create(model_class, *args, **kwargs)