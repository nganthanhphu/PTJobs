from .models import User, CandidateProfile, CompanyProfile, Follow
from .serializers import CandidateProfileSerializer, CompanyProfileSerializer
from django.core.mail import send_mass_mail

class RoleMapper:

    @staticmethod
    def get_model(role):
        MAPPING = {
            User.Role.CANDIDATE: CandidateProfile,
            User.Role.COMPANY: CompanyProfile
        }
        return MAPPING.get(role)

    @staticmethod
    def get_serializer(role):
        MAPPING = {
            User.Role.CANDIDATE: CandidateProfileSerializer,
            User.Role.COMPANY: CompanyProfileSerializer
        }
        return MAPPING.get(role)

class EmailService:
    @staticmethod
    def notify_via_email(job_post):
        title = f"Tin tuyển dụng mới: {job_post.name}"
        message = f"Công ty {job_post.company.name} vừa đăng tin tuyển dụng mới:\n\n"
        message += f"Vị trí: {job_post.name}\n"
        message += f"Mô tả: {job_post.description}\n"
        message += f"Địa chỉ: {job_post.address}\n"
        message += f"Lương: {job_post.salary:,.0f} VNĐ\n"
        message += f"Hạn nộp hồ sơ: {job_post.deadline.strftime('%d/%m/%Y')}\n\n"
        message += "Để biết thêm chi tiết, vui lòng truy cập vào hệ thống.\n\n"
        message += "Trân trọng,\nPTJobs"

        followers = Follow.objects.filter(
            company=job_post.company,
            active=True
        ).select_related('candidate__user')

        email_messages = []
        from_email = 'noreply@ptjobs.com'

        for follow in followers:
            user_email = follow.candidate.user.email
            if user_email:
                email_messages.append((
                    title,
                    message,
                    from_email,
                    [user_email]
                ))
        if email_messages:
            send_mass_mail(email_messages, fail_silently=False)
