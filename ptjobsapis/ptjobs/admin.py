from django.contrib import admin

from .models import (
    User, CandidateProfile, CompanyProfile, CompanyImage,
    Resume, JobPost, JobCategory, WorkTime, Application, Review, Follow
)


admin.site.site_header = "PT Jobs Administration"
admin.site.site_title = "PT Jobs Admin Portal"
admin.site.index_title = "Welcome to PT Jobs Admin"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email', 'phone')
    fieldsets = (
        ('Thông tin cơ bản', {'fields': ('username', 'email', 'phone', 'first_name', 'last_name')}),
        ('Trạng thái', {'fields': ('is_active', 'avatar')}),
    )
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'dob', 'active', 'created_at')
    list_filter = ('gender', 'active', 'created_at')
    search_fields = ('user__username', 'user__email')
    fieldsets = (
        ('Thông tin cơ bản', {'fields': ('user', 'gender', 'dob')}),
        ('Trạng thái', {'fields': ('active',)}),
        ('Ngày tạo', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_number', 'address', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'tax_number', 'user__email')
    fieldsets = (
        ('Thông tin công ty', {'fields': ('user', 'name', 'tax_number', 'address')}),
        ('Trạng thái', {'fields': ('active',)}),
        ('Ngày tạo', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(CompanyImage)
class CompanyImageAdmin(admin.ModelAdmin):
    list_display = ('company', 'image', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('company__name',)
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


@admin.register(Follow)
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
