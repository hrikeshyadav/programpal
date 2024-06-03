from django.contrib import admin

from .models import Room , Topic, Message, Product


class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['id','name','price','pdetail']
    list_filter = ['id' ]
admin.site.register(Product,ProductAdmin)


admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
# admin.site.register(Product)

