from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)
try:
	admin.site.register(Profile)
except Exception:
	# If migrations haven't been run yet or Profile isn't available, skip register
	pass
