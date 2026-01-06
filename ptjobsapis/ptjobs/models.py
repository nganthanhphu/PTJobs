from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    phone = models.CharField(max_length=15, null=False, blank=False, unique=True)

    class Role(models.TextChoices):
        CANDIDATE = 'CANDIDATE', 'Candidate'
        COMPANY = 'COMPANY', 'Company'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CANDIDATE)

    @property
    def profile(self):
        attr_name = f'{self.role.lower()}_profile'
        return getattr(self, attr_name, None)
    
    def __str__(self):
        return self.username


class CandidateProfile(BaseModel):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        OTHER = 'OTHER', 'Other'
        
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    dob = models.DateField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class CompanyProfile(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    tax_number = models.CharField(max_length=50, null=False, blank=False, unique=True)
    address = models.CharField(max_length=255, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    
    def __str__(self):
        return self.name


class CompanyImage(BaseModel):
    image = CloudinaryField()
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)


class Resume(BaseModel):
    file = CloudinaryField(resource_type='raw')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)


class JobPost(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=20, decimal_places=0)
    address = models.CharField(max_length=255)
    deadline = models.DateField()
    vacancy = models.IntegerField()
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='job_posts')
    category = models.ForeignKey('JobCategory', on_delete=models.SET_NULL, related_name='job_posts', null=True, blank=True)


class JobCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)


class WorkTime(BaseModel):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='work_times')


class Application(BaseModel):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class JobStatus(models.TextChoices):
        REVIEWING = 'REVIEWING', 'Reviewing',
        EMPLOYED = 'EMPLOYED', 'Employed',
        REJECTED = 'REJECTED', 'Rejected',
        TERMINATED = 'TERMINATED', 'Terminated'

    status = models.CharField(max_length=10, choices=JobStatus.choices, default=JobStatus.REVIEWING)
    resume = models.ForeignKey(Resume, on_delete=models.RESTRICT, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')

    class Meta:
        unique_together = ('candidate', 'job_post')


class Review(BaseModel):
    comment = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='reviews', null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='reviews')
    parent = models.OneToOneField('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reply')

    class Meta:
        unique_together = ('user', 'application')


class Interaction(BaseModel):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Follow(Interaction):
    class Meta:
        unique_together = ('candidate', 'company')
