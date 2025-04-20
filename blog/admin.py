from django.contrib import admin
from .models import *
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

def deactivepost(modeladmin, request, queryset):
    result = queryset.update(active=False)
    message = f"{result} posts are deactive"
    modeladmin.message_user(request, message)

deactivepost.short_description = 'Deactive'

def activepost(modeladmin, request, queryset):
    result = queryset.update(active=True)
    message = f"{result} posts are active"
    modeladmin.message_user(request, message)

activepost.short_description = 'Active'

def activeuser(modeladmin, request, queryset):
    result = queryset.update(is_active=True)
    message = f"{result} users are active"
    modeladmin.message_user(request, message)

activeuser.short_description = 'Active'

def deactiveuser(modeladmin, request, queryset):
    result = queryset.update(is_active=False)
    message = f"{result} users are deactive"
    modeladmin.message_user(request, message)

deactiveuser.short_description = 'Deactive'

class FirstNameInitialFilter(admin.SimpleListFilter):
    title = _('First Name Initial')
    parameter_name = 'first_name_initial'

    def lookups(self, request, model_admin):
        letters = sorted(set(user.first_name[0].upper() for user in User.objects.exclude(first_name="") if user.first_name))
        return [(letter, letter) for letter in letters]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                Q(first_name__istartswith=self.value()) |
                Q(first_name__istartswith=persian_equivalent(self.value()))
            )
        return queryset

class LastNameInitialFilter(admin.SimpleListFilter):
    title = _('Last Name Initial')
    parameter_name = 'last_name_initial'

    def lookups(self, request, model_admin):
        letters = sorted(set(user.last_name[0].upper() for user in User.objects.exclude(last_name="") if user.last_name))
        return [(letter, letter) for letter in letters]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                Q(last_name__istartswith=self.value()) |
                Q(last_name__istartswith=persian_equivalent(self.value()))
            )
        return queryset

class UsernameInitialFilter(admin.SimpleListFilter):
    title = _('Username Initial')
    parameter_name = 'username_initial'

    def lookups(self, request, model_admin):
        letters = sorted(set(user.username[0].upper() for user in User.objects.exclude(username="") if user.username))
        return [(letter, letter) for letter in letters]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                Q(username__istartswith=self.value()) |
                Q(username__istartswith=persian_equivalent(self.value()))
            )
        return queryset

def persian_equivalent(letter):
    mapping = {
        'A': 'ا', 'B': 'ب', 'P': 'پ', 'T': 'ت', 'S': 'س',
        'J': 'ج', 'C': 'چ', 'H': 'ح', 'D': 'د', 'R': 'ر',
        'Z': 'ز', 'S': 'س', 'SH': 'ش', 'F': 'ف', 'Q': 'ق',
        'K': 'ک', 'G': 'گ', 'L': 'ل', 'M': 'م', 'N': 'ن',
        'V': 'و', 'Y': 'ی',
    }
    return mapping.get(letter.upper(), '')

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'auther', 'created', 'active']
    ordering = ['title', 'created']
    list_filter = ['auther', 'created']
    search_fields = ['title', 'description']
    raw_id_fields = ['auther']
    prepopulated_fields = {"slug": ['title']}
    list_editable = ['active']
    inlines = [ImageInline]
    actions = [deactivepost, activepost]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'created']
    ordering = ['created', 'username']
    list_filter = [UsernameInitialFilter, 'created', FirstNameInitialFilter, LastNameInitialFilter]
    actions = [deactiveuser, activeuser]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'text', 'active']
    list_editable = ['active']
