from datetime import datetime

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.db.models.functions import TruncMonth

from .models import (
    User, CandidateProfile, CompanyProfile, CompanyImage,
    Resume, JobPost, JobCategory, WorkTime, Application, Review, Follow
)


class CandidateProfileInline(admin.StackedInline):
    model = CandidateProfile
    extra = 0
    fields = ('gender', 'dob', 'active')


class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile
    extra = 0
    fields = ('name', 'tax_number', 'address', 'active')


class CompanyImageInline(admin.StackedInline):
    model = CompanyImage
    extra = 0
    fields = ('image', 'image_view', 'active')
    readonly_fields = ('image_view',)

    def image_view(self, company_image):
        if company_image.image:
            return mark_safe(f"<img src='{company_image.image.url}' width='300' />")
        return None


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'candidate_profile', 'company_profile', 'get_profile_status')
    list_select_related = ('candidate_profile', 'company_profile')
    list_filter = ['role']
    search_fields = ('username', 'email', 'phone')
    fieldsets = (
        ('Thông tin cơ bản', {'fields': ('username', 'email', 'phone', 'first_name', 'last_name')}),
        ('Trạng thái', {'fields': ('is_active', 'avatar_view')})
    )
    readonly_fields = ['avatar_view']
    inlines = [CandidateProfileInline, CompanyProfileInline]

    @admin.display(description='PROFILE STATUS')
    def get_profile_status(self, obj):
        if obj.role == User.Role.CANDIDATE and obj.candidate_profile:
            return obj.candidate_profile.active
        elif obj.role == User.Role.COMPANY and obj.company_profile:
            return obj.company_profile.active
        return None

    def avatar_view(self, user):
        if user.avatar:
            return mark_safe(f"<img src='{user.avatar.url}' width='120' />")
        return None


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_number', 'user', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'tax_number')
    fieldsets = (
        ('Thông tin công ty', {'fields': ('name', 'tax_number', 'address', 'user')}),
        ('Trạng thái', {'fields': ('active', 'created_at')}),
    )
    readonly_fields = ('created_at',)
    inlines = [CompanyImageInline]


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'dob', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    list_select_related = ['user']
    search_fields = ('user__username', 'user__email')
    fieldsets = (
        ('Thông tin ứng viên', {'fields': ('user', 'gender', 'dob')}),
        ('Trạng thái', {'fields': ('active', 'created_at')})
    )
    readonly_fields = ('created_at',)


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


class WorkTimeInline(admin.TabularInline):
    model = WorkTime
    extra = 1


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'category', 'salary', 'vacancy', 'deadline', 'active')
    list_filter = ('active', 'category', 'deadline', 'created_at')
    search_fields = ('name', 'company__name', 'description')
    fieldsets = (
        ('Thông tin công việc', {'fields': ('name', 'description', 'company', 'category')}),
        ('Chi tiết tuyển dụng', {'fields': ('salary', 'address', 'vacancy', 'deadline')}),
        ('Trạng thái', {'fields': ('active',)}),
        ('Ngày tạo', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)
    inlines = [WorkTimeInline]


@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'job_post', 'active')
    list_filter = ('day', 'active')
    search_fields = ('job_post__name',)
    readonly_fields = ('created_at',)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'file', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('candidate__user__username', 'candidate__user__email')
    readonly_fields = ('created_at',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job_post', 'status', 'start_date', 'end_date', 'active', 'created_at')
    list_filter = ('status', 'active', 'start_date', 'created_at')
    search_fields = ('candidate__user__username', 'job_post__name')
    fieldsets = (
        ('Đơn ứng tuyển', {'fields': ('candidate', 'job_post', 'resume')}),
        ('Chi tiết hợp đồng', {'fields': ('start_date', 'end_date', 'status')}),
        ('Trạng thái', {'fields': ('active',)}),
        ('Ngày tạo', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'application', 'parent', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('user__username', 'application__candidate__user__username', 'comment')
    fieldsets = (
        ('Nội dung đánh giá', {'fields': ('comment', 'user', 'application')}),
        ('Trả lời', {'fields': ('parent',)}),
        ('Trạng thái', {'fields': ('active',)}),
        ('Ngày tạo', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'company', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('candidate__user__username', 'company__name')
    fieldsets = (
        ('Thông tin theo dõi', {'fields': ('candidate', 'company')}),
        ('Trạng thái', {'fields': ('active',)}),
        ('Ngày tạo', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)


class MyAdminSite(admin.AdminSite):
    site_header = "PT Jobs Admin Portal"
    site_title = "PT Jobs Admin Portal"
    index_title = "Welcome to PT Jobs Admin"

    def get_urls(self):
        return [path('statistics/', self.stats_view)] + super().get_urls()

    def stats_view(self, request):
        selected_year = int(request.GET.get('year', datetime.now().year))
        jobs_stats = JobPost.objects.filter(created_at__year=selected_year).annotate(
            month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')

        candidates_stats = CandidateProfile.objects.filter(created_at__year=selected_year).annotate(
            month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')

        companies_stats = CompanyProfile.objects.filter(created_at__year=selected_year).annotate(
            month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')

        return TemplateResponse(request, 'admin/statistics.html', context={
            'jobs_stats': jobs_stats,
            'candidates_stats': candidates_stats,
            'companies_stats': companies_stats,
            'selected_year': selected_year
        })


admin_site = MyAdminSite(name='ptjobs_admin')
admin_site.register(User, UserAdmin)
admin_site.register(CandidateProfile, CandidateProfileAdmin)
admin_site.register(CompanyProfile, CompanyProfileAdmin)
admin_site.register(JobCategory, JobCategoryAdmin)
admin_site.register(JobPost, JobPostAdmin)
admin_site.register(Resume, ResumeAdmin)
admin_site.register(Application, ApplicationAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(Follow, FollowAdmin)
