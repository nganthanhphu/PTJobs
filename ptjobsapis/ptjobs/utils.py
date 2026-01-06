from .models import User, CandidateProfile, CompanyProfile
from .serializers import CandidateProfileSerializer, CompanyProfileSerializer

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