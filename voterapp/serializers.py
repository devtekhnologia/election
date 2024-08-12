# # voter api 

# from rest_framework import serializers
# from .models import Voterlist, Town, Booth

# class VoterlistSerializer(serializers.ModelSerializer):
#     town_name = serializers.SerializerMethodField()
#     booth_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Voterlist
#         fields = ['voter_id', 'voter_name', 'voter_parent_name', 'voter_house_number', 'voter_age', 'voter_gender', 'town_name', 'booth_name', 'voter_contact_number', 'voter_cast']

#     def get_town_name(self, obj):
#         try:
#             town = Town.objects.get(town_id=obj.voter_town_id)
#             return town.town_name
#         except Town.DoesNotExist:
#             return None

#     def get_booth_name(self, obj):
#         try:
#             booth = Booth.objects.get(booth_id=obj.voter_booth_id)
#             return booth.booth_name
#         except Booth.DoesNotExist:
#             return None


# # # register api

# from rest_framework import serializers
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # fields = '__all__'
#         fields = ['user_name', 'user_phone', 'user_password']



# # # login api

# class LoginSerializer(serializers.Serializer):
#     user_name = serializers.CharField()
#     user_password = serializers.CharField()
    

# # # Town api

# from .models import Town

# class TownSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Town
#         fields = ['town_id', 'town_name']


# # # Booth api

# from .models import Booth
# class BoothSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booth
#         fields = ['booth_id', 'booth_name']


# # # Panchayat_samiti api

# from .models import PanchayatSamiti

# class PanchayatSamitiSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PanchayatSamiti
#         fields = ['panchayat_samiti_id', 'panchayat_samiti_name']


# # # ZP api

# from .models import ZP

# class ZPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ZP
#         fields = ['zp_id', 'zp_name']


# # # Vidhansabha api 

# from .models import Vidhansabha

# class VidhansabhaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vidhansabha
#         fields = ['vidhansabha_id', 'vidhansabha_name']


# # # State api

# from .models import State

# class StateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = State
#         fields = ['state_id', 'state_name']


# # cast api

# class VoterlistSerializerWithCast(serializers.ModelSerializer):
#     class Meta:
#         model = Voterlist
#         fields = ['voter_name', 'voter_cast']



# # firm login

# class FirmLoginSerializer(serializers.Serializer):
#     firm_name  = serializers.CharField()
#     firm_password = serializers.CharField()


# # firm register

# from .models import Firm

# class FirmSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Firm
#         fields = [ 'firm_name', 'firm_contact_number', 'firm_password']


# # # Religion api

# from .models import Religion
# class ReligionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Religion
#         fields = ['religion_id', 'religion_name']


# # Favour non-favour api

# from .models import Favour_non_favour
# class Favour_non_favourSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Favour_non_favour
#         fields = ['favour_id', 'favour_type']



# # working code 

from rest_framework import serializers
from .models import Voterlist, Town, Booth, Favour_non_favour, Vote_confirmation
from django.utils.timezone import localtime
from datetime import timedelta
import pytz
from .models import LiveStatus


class VoterlistSerializer(serializers.ModelSerializer):
    town_name = serializers.SerializerMethodField()
    booth_name = serializers.SerializerMethodField()
    booth_id = serializers.SerializerMethodField()
    voter_updated_by = serializers.ReadOnlyField()
    user_name = serializers.SerializerMethodField()
    voter_updated_date = serializers.DateField(format='%Y-%m-%d', required=False, allow_null=True)
    live_status_type = serializers.SerializerMethodField()
    religion_name = serializers.SerializerMethodField()
    vote_confirmation_type = serializers.SerializerMethodField()

    class Meta:
        model = Voterlist
        fields = ['voter_id', 'voter_name', 'voter_parent_name', 'voter_house_number', 'voter_age', 'voter_gender', 'town_name', 
                  'booth_id', 'booth_name', 'voter_contact_number', 'voter_cast', 'voter_favour_id', 'voter_constituency_id', 'voter_dob', 
                  'voter_marital_status_id', 'voter_updated_by', 'user_name', 'voter_updated_date', 'voter_live_status_id',
                  'live_status_type', 'religion_name', 'voter_dead_year', 'voter_vote_confirmation_id' ,'vote_confirmation_type']
        
        extra_kwargs = {
            'voter_house_number': {'allow_null': True, 'required': False},
            'voter_parent_name': {'allow_null': True, 'required': False},
            'voter_age': {'allow_null': True, 'required': False},
            'voter_gender': {'allow_null': True, 'required': False},
            'voter_contact_number': {'allow_null': True, 'required': False},
            'voter_cast': {'allow_null': True, 'required': False},
            'voter_favour_id': {'allow_null': True, 'required': False},
            'voter_constituency_id': {'allow_null': True, 'required': False},
            'voter_dob': {'allow_null': True, 'required': False},
            'voter_marital_status_id': {'allow_null': True, 'required': False},
            'voter_updated_by': {'allow_null': True, 'required': False},
            'voter_updated_date': {'allow_null': True, 'required': False},
            'voter_live_status_id': {'allow_null': True, 'required': False},
            'voter_dead_year' : {'allow_null': True, 'required': False},
            'vote_confirmation_type' : {'allow_null': True, 'required': False},
        }



    def get_town_name(self, obj):
        if obj.voter_town_id:
            try:
                town = Town.objects.get(town_id=obj.voter_town_id)
                return town.town_name
            except Town.DoesNotExist:
                return None
        return None

    def get_booth_name(self, obj):
        if obj.voter_booth_id:
            try:
                booth = Booth.objects.get(booth_id=obj.voter_booth_id)
                return booth.booth_name
            except Booth.DoesNotExist:
                return None
        return None

    def get_booth_id(self, obj):
        return obj.voter_booth_id

  
    def get_voter_updated_by(self, obj):
        if obj.voter_updated_by:
            return obj.voter_updated_by.username  # Return the username of the editor
        return None
    
    def get_user_name(self, obj):
        try:
            user = User.objects.get(user_id=obj.voter_updated_by)
            return user.user_name
        except User.DoesNotExist:
            return None
    
    def get_live_status_type(self, obj):
        if obj.voter_live_status_id:
            try:
                live_status = LiveStatus.objects.get(live_status_id=obj.voter_live_status_id)
                return live_status.live_status_type
            except LiveStatus.DoesNotExist:
                return None
        return None
    
    def get_religion_name(self, obj):
        if obj.voter_religion_id:
            try:
                religion = Religion.objects.get(religion_id=obj.voter_religion_id)
                return religion.religion_name
            except Religion.DoesNotExist:
                return None
        return None
    
    def get_vote_confirmation_type(self, obj):
        if obj.voter_vote_confirmation_id:
            try:
                vote_confirmation = Vote_confirmation.objects.get(vote_confirmation_id=obj.voter_vote_confirmation_id)
                return vote_confirmation.vote_confirmation_type
            except Vote_confirmation.DoesNotExist:
                return None
        return None
    
   

# # # register api
# api for multiple booth asign to user

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ['user_id', 'user_name', 'user_phone', 'user_password']

from .models import UserBooth

class UserBoothSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBooth
        fields = ['user_booth_user_id', 'user_booth_booth_id']

class UserRegistrationSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255)
    user_password = serializers.CharField(max_length=255)
    user_phone = serializers.CharField(max_length=15)
    booth_ids = serializers.ListField(
        child=serializers.IntegerField()
    )


# # login api

class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    # user_booth_id = serializers.CharField()
    user_password = serializers.CharField()


# # Town api

from .models import Town

class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ['town_id', 'town_name']


# # Booth api

from .models import Booth
class BoothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth
        fields = ['booth_id', 'booth_name']


# # Panchayat_samiti api

from .models import PanchayatSamiti

class PanchayatSamitiSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanchayatSamiti
        fields = ['panchayat_samiti_id', 'panchayat_samiti_name']


# # ZP api

from .models import ZP

class ZPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZP
        fields = ['zp_id', 'zp_name']


# # Vidhansabha api 

from .models import Vidhansabha

class VidhansabhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vidhansabha
        fields = ['vidhansabha_id', 'vidhansabha_name']


# # State api

from .models import State

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['state_id', 'state_name']



# from .models import Voter
# class VoterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Voter
#         fields = '__all__'
 


class VoterlistSerializerWithCast(serializers.ModelSerializer):
    class Meta:
        model = Voterlist
        fields = ['voter_name', 'voter_cast']


# Politician register

from .models import Politician

class PoliticianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Politician
        fields = [ 'politician_name', 'politician_contact_number', 'politician_password']


# Politician login

from rest_framework import serializers

class PoliticianLoginSerializer(serializers.Serializer):
    politician_name = serializers.CharField()
    politician_password = serializers.CharField(write_only=True)


# # Religion api

from .models import Religion
class ReligionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religion
        fields = ['religion_id', 'religion_name']


# Favour non-favour api

from .models import Favour_non_favour

class Favour_non_favourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voterlist
        fields = ['voter_id', 'voter_favour_id']


# town_user login

from .models import Town_user

class Town_userLoginSerializer(serializers.Serializer):
    town_user_name  = serializers.CharField()
    town_user_password = serializers.CharField()


# town_user register

# from .models import Town_user

# class Town_userSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Town_user
#         fields = [ 'town_user_name', 'town_user_contact_number', 'town_user_password', 'town_user_town_id']


from .models import Town_user, UserTown

class TownUserSerializer(serializers.ModelSerializer):
   class Meta:
       model = Town_user
       fields = ['user_town_town_user_id', 'town_user_name', 'town_user_contact_number', 'town_user_password']

class UserTownSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTown
        fields = ['user_town_town_user_id', 'user_town_town_id']

class TownUserRegistrationSerializer(serializers.Serializer):
    town_user_name = serializers.CharField(max_length=255)
    town_user_password = serializers.CharField(max_length=255)
    town_user_contact_number = serializers.CharField(max_length=15)
    town_ids = serializers.ListField(
        child=serializers.IntegerField()
    )

# constituency wise voter api

from .models import Voterlist, Constituency

class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = ['constituency_id', 'constituency_name']


# Marital status api

from .models import MaritalStatus

class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = ['marital_status_id', 'marital_status_type']


# Panchayat Samiti Circle

from .models import PanchayatSamitiCircle

class PanchayatSamitiCircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanchayatSamitiCircle
        fields = ['panchayat_samiti_circle_id', 'panchayat_samiti_circle_name']

# ZP Circle 

from .models import ZpCircle

class ZpCircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZpCircle
        fields = ['zp_circle_id', 'zp_circle_name']



# voter vote confirmation

from .models import Vote_confirmation

class vote_confirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote_confirmation
        fields = ['vote_confirmation_id', 'vote_confirmation_type']