from django.contrib.auth.backends import BaseBackend
from .models import Admin, Receptionist, Mechanic, InventoryManager, Customer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import check_password

class VMSMSUser:
    def __init__(self, user_obj, user_type):
        self.user_obj = user_obj
        self.user_type = user_type
        self.username = getattr(user_obj, 'username', getattr(user_obj, 'email', None))
        self.is_authenticated = True
        self.role = user_type
        self.id = getattr(user_obj, 'pk', None)

    def __str__(self):
        return f"{self.user_type}: {self.username}"

class VMSMSBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, user_type=None):
        model_map = {
            'admin': Admin,
            'receptionist': Receptionist,
            'mechanic': Mechanic,
            'inventory_manager': InventoryManager,
            'customer': Customer,
        }
        model = model_map.get(user_type)
        if not model:
            return None
        try:
            user = model.objects.get(username=username)
            # For demo, use plain text. In production, use hashed passwords.
            if user.password == password:
                return VMSMSUser(user, user_type)
        except model.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        # Not used for session auth, but required by Django
        return None 