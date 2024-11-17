from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    if not User.objects.filter(phone_number='670007058').exists():
        User.objects.create_superuser(
            phone_number='670007058',
            password='2002',
            email='davyemane2@gmail.com',
            is_staff=True,
            is_superuser=True
        )