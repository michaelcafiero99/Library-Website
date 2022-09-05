
from django.contrib import admin
from .models import Customers
from .models import Items
from .models import Rooms
from .models import Employees
from .models import RentedBooks

admin.site.register(Customers)
admin.site.register(Items)
admin.site.register(Rooms)
admin.site.register(Employees)
admin.site.register(RentedBooks)