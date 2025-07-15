from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperUserCommand


class Command(BaseCreateSuperUserCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--age', type=int, help='Age of the user')
        parser.add_argument('--can_be_contacted', action='store_true', help='Can be contacted')
        parser.add_argument('--can_data_be_shared', action='store_true', help='Can data be shared')

    def handle(self, *args, **options):
        options['age'] = options.get('age', 25)
        options['can_be_contacted'] = options.get('can_be_contacted', False)
        options['can_data_be_shared'] = options.get('can_data_be_shared', False)
        super().handle(*args, **options)
