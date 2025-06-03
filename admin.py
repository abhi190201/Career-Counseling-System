from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import InterestQuestion
from .models import Course  # ✅ Import Course model
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = (UserProfileInline,)

    list_display = ('username', 'email', 'full_name', 'tenth_percentage', 'twelfth_percentage', 'graduation_percentage', 'graduation_year', 'graduation_stream', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'full_name')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {
            'fields': (
                'full_name', 
                'profile_picture',
                'tenth_percentage', 
                'twelfth_percentage', 
                'graduation_percentage', 
                'graduation_year', 
                'graduation_stream', 
                'resume'
            )
        }),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


@admin.register(InterestQuestion)
class InterestQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'link')
    search_fields = ('title', 'domain')

from .models import Domain, DomainQuestion, InterestOption

# ✅ Register Domain model
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('DomainID', 'DomainName')
    search_fields = ('DomainName',)


# ✅ Register DomainQuestion model
@admin.register(DomainQuestion)
class DomainQuestionAdmin(admin.ModelAdmin):
    list_display = ('DomainQuestionID', 'Domain', 'QuestionNumber', 'QuestionText')
    list_filter = ('Domain',)
    search_fields = ('QuestionText',)
    ordering = ('Domain', 'QuestionNumber')


# ✅ Register InterestOption model
@admin.register(InterestOption)
class InterestOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'option_label', 'option_text')
    list_filter = ('option_label',)
    search_fields = ('option_text',)

from .models import UserProfile, InterestResult, DomainTestResult, Roadmap, Progress


# ✅ Register DomainTestResult
@admin.register(DomainTestResult)
class DomainTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'domain', 'score', 'submitted_at')
    search_fields = ('user__username', 'domain__DomainName')
    list_filter = ('domain',)


# ✅ Register Roadmap
@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('user', 'domain', 'level', 'generated_at')
    search_fields = ('user__username', 'domain__DomainName')
    list_filter = ('level',)
    readonly_fields = ('generated_at',)  # ✅ Mark as read-only



# ✅ Register InterestResult
@admin.register(InterestResult)
class InterestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'recommended_domains')
    search_fields = ('user__username',)

# ✅ Register Progress
@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_complete', 'test_complete', 'roadmap_complete', 'courses_complete', 'domain_complete')
    search_fields = ('user__username',)
