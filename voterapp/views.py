# # working code

# import pandas as pd
# from voterapp.models import Voterlist, Booth, Town
# from django.shortcuts import render
# from django.http import HttpResponse, HttpResponseBadRequest



# def upload_file(request):
#     if request.method == 'POST':
#         if 'files' not in request.FILES:
#             return HttpResponseBadRequest("No files uploaded")
        
#         files = request.FILES.getlist('files')
#         for file in files:
#             import_excel_data(file)
        
#         return HttpResponse("Files uploaded and data imported successfully")
    
#     return render(request, 'upload_file.html')



# import pandas as pd
# from django.db import transaction 
# from voterapp.models import State, ZP, PanchayatSamiti, Town, Booth, Voterlist

# @transaction.atomic
# def import_excel_data(file):
#     df = pd.read_excel(file)
#     state_dict = {}
#     zp_dict = {}
#     panchayat_samiti_dict = {}
#     town_dict = {}
#     booth_dict = {}
#     voter_dict = {}

#     for _, row in df.iterrows():
#         state_name = row['State']
#         district_name = row['District']
#         taluka_name = row['Taluka']
#         town_name = row['Town or Village']
#         booth_name = row['Address of Polling Station']

#         # State
#         state_id = state_dict.get(state_name)
#         if state_id is None:
#             state, created = State.objects.get_or_create(state_name=state_name)
#             state_dict[state_name] = state.state_id
#             state_id = state.state_id

#         # ZP
#         zp_id = zp_dict.get(district_name)
#         if zp_id is None:
#             state_obj = State.objects.get(state_name=state_name)
#             zp, created = ZP.objects.get_or_create(zp_name=district_name, zp_state_id=state_obj.state_id)
#             zp_dict[district_name] = zp.zp_id
#             zp_id = zp.zp_id

#         # Panchayat Samiti
#         panchayat_samiti_id = panchayat_samiti_dict.get(taluka_name)
#         if panchayat_samiti_id is None:
#             zp_obj = ZP.objects.get(zp_name=district_name)
#             panchayat_samiti, created = PanchayatSamiti.objects.get_or_create(
#                 panchayat_samiti_name=taluka_name, panchayat_samiti_zp_id=zp_obj.zp_id)
#             panchayat_samiti_dict[taluka_name] = panchayat_samiti.panchayat_samiti_id
#             panchayat_samiti_id = panchayat_samiti.panchayat_samiti_id

#         # Town
#         town_id = town_dict.get(town_name)
#         if town_id is None:
#             panchayat_samiti_obj = PanchayatSamiti.objects.get(panchayat_samiti_name=taluka_name)
#             town, created = Town.objects.get_or_create(town_name=town_name, town_panchayat_samiti_id=panchayat_samiti_obj.panchayat_samiti_id)
#             town_dict[town_name] = town.town_id
#             town_id = town.town_id

#         # Booth
#         booth_id = booth_dict.get(booth_name)
#         if booth_id is None:
#             town_obj = Town.objects.get(town_name=town_name)
#             booth, created = Booth.objects.get_or_create(booth_name=booth_name, booth_town_id=town_obj.town_id)
#             booth_dict[booth_name] = booth.booth_id
#             booth_id = booth.booth_id


#         voter_id = voter_dict.get((town_name, booth_name, row['Name']))  # Adding row['Name'] for a unique identifier
#         if voter_id is None:
#             town_obj = Town.objects.get(town_name=town_name)
#             booth_obj = Booth.objects.get(booth_name=booth_name, booth_town_id=town_obj.town_id)
#             voter, created = Voterlist.objects.get_or_create(
#                 voter_name=row['Name'],
#                 voter_parent_name=row['Parent Name'],
#                 voter_house_number=row['House Number'],
#                 voter_age=row['Age'],
#                 voter_gender=row['Gender'],
#                 voter_town_id=town_obj.town_id,
#                 voter_booth_id=booth_obj.booth_id
#             )
#             voter_dict[(town_name, booth_name, row['Name'])] = voter.voter_id
#             voter_id = voter.voter_id


# # voter api

# from rest_framework import generics
# from .models import Voterlist
# from .serializers import VoterlistSerializer

# class VoterlistListCreate(generics.ListCreateAPIView):
#     queryset = Voterlist.objects.all()
#     serializer_class = VoterlistSerializer

# class VoterlistRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Voterlist.objects.all()
#     serializer_class = VoterlistSerializer
#     lookup_field = 'voter_id'  # Use the primary key field as the lookup field



# # # register api

# from rest_framework import generics
# from .models import User
# from .serializers import UserSerializer

# class UserListCreate(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def perform_create(self, serializer):
#         session_id = self.request.session.get('firm_id')  # Retrieve session ID
#         serializer.save(user_firm_id=session_id) 

# class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer




# # # login api

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth.hashers import check_password
# from .serializers import LoginSerializer, VoterlistSerializer
# from .models import User, Voterlist

# class UserLogin(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user_name = serializer.validated_data.get('user_name')
#             user_password = serializer.validated_data.get('user_password')

#             try:
#                 user = User.objects.get(user_name=user_name)
#             except User.DoesNotExist:
#                 return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#             if check_password(user_password, user.user_password):
#                 voters = Voterlist.objects.filter(voter_booth_id=user.user_booth_id)
#                 serializer = VoterlistSerializer(voters, many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # # Get users api

# from django.http import JsonResponse
# from django.db import connection

# def get_voters(request):
#     state_id_param = request.GET.get('state_id')
#     vidhansabha_id_param = request.GET.get('vidhansabha_id')
#     zp_id_param = request.GET.get('zp_id')
#     panchayat_samiti_id_param = request.GET.get('panchayat_samiti_id')
#     town_id_param = request.GET.get('town_id')
#     booth_id_param = request.GET.get('booth_id')

#     cursor = connection.cursor()
#     cursor.callproc('GetVoters', [state_id_param, vidhansabha_id_param, zp_id_param, panchayat_samiti_id_param, town_id_param, booth_id_param])
#     results = cursor.fetchall()
    
#     voters = []
#     for row in results:
#         voters.append({
#             'voter_name': row[0],
#             'town_name': row[1],
#             'booth_name': row[2]
#         })
    
#     return JsonResponse({'voters': voters})


# # # Town api

# from .models import Town
# from .serializers import TownSerializer

# class TownList(generics.ListAPIView):
#     queryset = Town.objects.all()
#     serializer_class = TownSerializer


# # # Booth api

# from .models import Booth
# from .serializers import BoothSerializer

# class BoothList(generics.ListAPIView):
#     queryset = Booth.objects.all()
#     serializer_class = BoothSerializer


# # # Panchayat_samiti api

# from .models import PanchayatSamiti
# from .serializers import PanchayatSamitiSerializer

# class PanchayatSamitiListCreate(generics.ListCreateAPIView):
#     queryset = PanchayatSamiti.objects.all()
#     serializer_class = PanchayatSamitiSerializer

# class PanchayatSamitiRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = PanchayatSamiti.objects.all()
#     serializer_class = PanchayatSamitiSerializer


# # # ZP api

# from .models import ZP
# from .serializers import ZPSerializer

# class ZPlistCreate(generics.ListCreateAPIView):
#     queryset = ZP.objects.all()
#     serializer_class = ZPSerializer

# class ZPRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ZP.objects.all()
#     serializer_class = ZPSerializer


# # # vidhansabha api

# from .models import Vidhansabha
# from .serializers import VidhansabhaSerializer

# class VidhansabhaListCreate(generics.ListCreateAPIView):
#     queryset = Vidhansabha.objects.all()
#     serializer_class = VidhansabhaSerializer

# class VidhansabhaRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Vidhansabha.objects.all()
#     serializer_class = VidhansabhaSerializer


# # # state api

# from .models import State
# from .serializers import StateSerializer

# class StateListCreate(generics.ListCreateAPIView):
#     queryset = State.objects.all()
#     serializer_class = StateSerializer

# class StateRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = State.objects.all() 
#     serializer_class = StateSerializer


# # # get_voters_by_booth wise api

# def get_voters_by_booth(request, booth_id):
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT v.voter_id, v.voter_name, b.booth_name
#             FROM tbl_voter v
#             JOIN tbl_booth b ON v.voter_booth_id = b.booth_id
#             WHERE v.voter_booth_id = %s
#         """, [booth_id])
#         results = cursor.fetchall()
    
#     voters = []
#     for row in results:
#         voters.append({
#             'voter_id': row[0],
#             'voter_name': row[1],
#             'booth_name': row[2]
#         })
    
#     return JsonResponse({'voters': voters})


# # cast api

# from .serializers import VoterlistSerializerWithCast
# from django.views import View

# class GetVoterByCastView(View):
#     def get(self, request, voter_cast):
#         voters = Voterlist.objects.filter(voter_cast=voter_cast)
#         voters_list = list(voters.values())
#         return JsonResponse(voters_list, safe=False)



# # firm login

# from .serializers import FirmLoginSerializer
# from .models import Firm 

# class FirmLogin(APIView):
#     def post(self, request):
#         serializer = FirmLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             firm_name = serializer.validated_data.get('firm_name')
#             firm_password = serializer.validated_data.get('firm_password')

#             try:
#                 firm = Firm.objects.get(firm_name=firm_name)

#             except Firm.DoesNotExist:
#                 return Response({"message": "Invalid name credentials"}, status=status.HTTP_401_UNAUTHORIZED) 


#             # if check_password(firm_password, firm.firm_password)
#             if firm_password == firm.firm_password:
#                 request.session['firm_id'] = firm.firm_id
#                 print(request.session.get('firm_id'))
#                 return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"message": "Invalid password credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# # firm register

# from .models import Firm
# from .serializers import FirmSerializer

# class FirmCreate(generics.ListCreateAPIView):
#     queryset = Firm.objects.all()
#     serializer_class = FirmSerializer


# # # Religion api

# from .models import Religion
# from .serializers import ReligionSerializer

# class ReligionListCreate(generics.ListCreateAPIView):
#     queryset = Religion.objects.all()
#     serializer_class = ReligionSerializer

# class ReligionRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Religion.objects.all() 
#     serializer_class = ReligionSerializer


# # Favour non-favour api

# from .models import Favour_non_favour
# from .serializers import Favour_non_favourSerializer

# class Favour_non_favourListCreate(generics.ListCreateAPIView):
#     queryset = Favour_non_favour.objects.all()
#     serializer_class = Favour_non_favourSerializer

# class Favour_non_favourRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Favour_non_favour.objects.all() 
#     serializer_class = Favour_non_favourSerializer





# # working code 

import pandas as pd
from voterapp.models import Voterlist, Booth, Town
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest



def upload_file(request):
    if request.method == 'POST':
        if 'files' not in request.FILES:
            return HttpResponseBadRequest("No files uploaded")
        
        files = request.FILES.getlist('files')
        for file in files:
            import_excel_data(file)
        
        return HttpResponse("Files uploaded and data imported successfully")
    
    return render(request, 'upload_file.html')


# excel to DB

from django.db import transaction
@transaction.atomic
def import_excel_data(file):
    try:
        df = pd.read_excel(file)
    except Exception as e:
        # logger.error(f"Error reading Excel file: {str(e)}")
        return f"Error reading Excel file: {str(e)}"

    successful_imports = 0
    total_rows = len(df)

    data_list = df.values.tolist()

    booth_dict = {}
    town_dict = {}
    for rec in data_list:
        state_name = rec[10]
        district_name = rec[9]
        taluka_name = rec[8]
        town_name = rec[6]
        booth_name = rec[7]
        vote_name = rec[1]

        

        booth_id = None
        town_id = None
        

        state, created = State.objects.get_or_create(state_name=state_name)

        zp, created = ZP.objects.get_or_create(zp_name=district_name, zp_state_id=state.state_id)

        panchayat_samiti, created = PanchayatSamiti.objects.get_or_create(panchayat_samiti_name=taluka_name, panchayat_samiti_zp_id=zp.zp_id)
        
        if town_name not in town_dict:
            town, created = Town.objects.get_or_create(town_name=town_name, town_panchayat_samiti_id=panchayat_samiti.panchayat_samiti_id)
            town_dict[town_name] = town.town_id
            town_id = town.town_id
        else:
            town_id = town_dict[town_name]

        if booth_name not in booth_dict:
            booth, created = Booth.objects.get_or_create(booth_name=booth_name, booth_town_id=town.town_id)
            booth_dict[booth_name] = booth.booth_id
            booth_id = booth.booth_id
        else:
            booth_id = booth_dict[booth_name]
        

        #voter_name, created = Voterlist.objects.get_or_create(voter_name = vote_name, voter_town_id = town.town_id, voter_booth_id = booth.booth_id)

        vote_obj = Voterlist(
            
            voter_name = vote_name,
            voter_parent_name = rec[2],
            voter_house_number = rec[3],
            voter_age = rec[4],
            voter_gender = rec[5],
            voter_town_id = town_id,
            voter_booth_id = booth_id
        )

        vote_obj.save()



# # voter api


from rest_framework import generics
from .models import Voterlist
from .serializers import VoterlistSerializer

class VoterlistListCreate(generics.ListCreateAPIView):
    queryset = Voterlist.objects.all()
    serializer_class = VoterlistSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class VoterlistRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voterlist.objects.all()
    serializer_class = VoterlistSerializer
    lookup_field = 'voter_id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.refresh_from_db()  # Refresh from database to ensure updated fields are fetched
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        user_id = self.request.session.get('user_id')
        serializer.save(voter_updated_by=user_id)


# # # user registration api             # api for multiple booth asign to user with registration


# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import User, UserBooth
# from .serializers import UserRegistrationSerializer, UserSerializer, UserBoothSerializer

# @api_view(['POST'])
# def register_user(request):
#     serializer = UserRegistrationSerializer(data=request.data)
    
#     if serializer.is_valid():
#         user_data = {
#             'user_name': serializer.validated_data['user_name'],
#             'user_password': serializer.validated_data['user_password'],
#             'user_phone': serializer.validated_data['user_phone']
#         }
        
#         user_serializer = UserSerializer(data=user_data)
        
#         if user_serializer.is_valid():
#             session_id = request.session.get('user_town_town_user_id')
#             user = user_serializer.save(user_town_town_user_id=session_id)
#             booth_ids = serializer.validated_data['booth_ids']
            
#             for booth_id in booth_ids:
#                 UserBooth.objects.create(user_booth_user_id=user.user_id, user_booth_booth_id=booth_id)
                
#             return Response({'status': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, UserBooth
from .serializers import UserRegistrationSerializer, UserSerializer

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_data = {
                'user_name': serializer.validated_data['user_name'],
                'user_password': serializer.validated_data['user_password'],
                'user_phone': serializer.validated_data['user_phone']
            }

            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                session_id = request.session.get('user_town_town_user_id')
                user = user_serializer.save(user_town_town_user_id=session_id)
                booth_ids = serializer.validated_data['booth_ids']

                for booth_id in booth_ids:
                    UserBooth.objects.create(user_booth_user_id=user.user_id, user_booth_booth_id=booth_id)

                return Response({'status': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# # login api

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from .serializers import LoginSerializer
from .models import User

class UserLogin(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('user_name')
            user_password = serializer.validated_data.get('user_password')

            try:
                user = User.objects.get(user_name=user_name)
            except User.DoesNotExist:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if check_password(user_password, user.user_password):
                user_id = user.user_id
                response_data = {
                    "message" : "Login Successful",
                    "user_id" : user_id
                }
                request.session['user_id'] = user.user_id
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Booth user Logout API

class UserLogout(APIView):
    def post(self, request):
        if 'user_id' in request.session:
            del request.session['user_id']
            return Response({"message": "Logout Successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not logged in"}, status=status.HTTP_400_BAD_REQUEST)



# # Get users api

from django.http import JsonResponse
from django.db import connection

def get_voters(request, booth_id=None):
    state_id_param = request.GET.get('state_id')
    vidhansabha_id_param = request.GET.get('vidhansabha_id')
    zp_id_param = request.GET.get('zp_id')
    panchayat_samiti_id_param = request.GET.get('panchayat_samiti_id')
    town_id_param = request.GET.get('town_id')
    booth_id_param = request.GET.get('booth_id') if booth_id is None else booth_id

    cursor = connection.cursor()
    cursor.callproc('GetVoters', [state_id_param, vidhansabha_id_param, zp_id_param, panchayat_samiti_id_param, town_id_param, booth_id_param])
    results = cursor.fetchall()
    
    voters = []
    for row in results:
        voters.append({
            'voter_id': row[0],
            'voter_name': row[1],
            'booth_name': row[2], 
            'town_name': row[3]
        })
    
    return JsonResponse({'voters': voters})



# # Town api

from .models import Town
from .serializers import TownSerializer

class TownList(generics.ListAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer


# # Booth api

from .models import Booth
from .serializers import BoothSerializer

class BoothList(generics.ListAPIView):
    queryset = Booth.objects.all()
    serializer_class = BoothSerializer
    lookup_field = 'booth_id' 


# # Panchayat_samiti API

from .models import PanchayatSamiti
from .serializers import PanchayatSamitiSerializer

class PanchayatSamitiListCreate(generics.ListCreateAPIView):
    queryset = PanchayatSamiti.objects.all()
    serializer_class = PanchayatSamitiSerializer

class PanchayatSamitiRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PanchayatSamiti.objects.all()
    serializer_class = PanchayatSamitiSerializer


# # ZP api

from .models import ZP
from .serializers import ZPSerializer

class ZPListCreate(generics.ListCreateAPIView):
    queryset = ZP.objects.all()
    serializer_class = ZPSerializer

class ZPRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZP.objects.all()
    serializer_class = ZPSerializer


# # vidhansabha api

from .models import Vidhansabha
from .serializers import VidhansabhaSerializer

class VidhansabhaListCreate(generics.ListCreateAPIView):
    queryset = Vidhansabha.objects.all()
    serializer_class = VidhansabhaSerializer

class VidhansabhaRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vidhansabha.objects.all()
    serializer_class = VidhansabhaSerializer


# # state api

from .models import State
from .serializers import StateSerializer

class StateListCreate(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class StateRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer



# # get_voters_by_booth wise api

def get_voters_by_booth(request, booth_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.voter_id, v.voter_name, b.booth_name, voter_contact_number, voter_cast, voter_favour_id, voter_booth_id,
                       voter_town_id, voter_parent_name, voter_age, voter_gender, voter_marital_status_id
            FROM tbl_voter v
            JOIN tbl_booth b ON  b.booth_id = v.voter_booth_id 
            WHERE v.voter_booth_id = %s
        """, [booth_id])
        results = cursor.fetchall()
    
    voters = []
    for row in results:
        voters.append({
            'voter_id': row[0],
            'voter_name': row[1],
            'booth_name': row[2],
            'voter_contact_number' : row[3],
            'voter_cast' : row[4],
            'voter_favour_id' : row[5],
            'voter_booth_id' : row[6],
            'voter_town_id' : row[7],
            'voter_parent_name' : row[8],
            'voter_age' : row[9],
            'voter_gender' : row[10],
            'voter_marital_status_id' : row[11]

        })
    
    return JsonResponse({'voters': voters})


# Get voters by cast wise

from .serializers import VoterlistSerializerWithCast
from django.views import View

class GetVoterByCastView(View):
    def get(self, request, voter_cast):
        voters = Voterlist.objects.filter(voter_cast=voter_cast)
        voters_list = list(voters.values())
        return JsonResponse(voters_list, safe=False)
    

# Politician register

from .models import Politician
from .serializers import PoliticianSerializer

class PoliticianCreate(generics.ListCreateAPIView):
    queryset = Politician.objects.all()
    serializer_class = PoliticianSerializer



# Politician login

from .serializers import PoliticianLoginSerializer
from .models import Politician

class PoliticianLoginView(APIView):
    def post(self, request):
        serializer = PoliticianLoginSerializer(data=request.data)
        if serializer.is_valid():
            username_or_contact = serializer.validated_data['politician_name']
            password = serializer.validated_data['politician_password']

            try:
                # Determine if the input is a name or contact number
                if username_or_contact.isdigit():
                    politician = Politician.objects.get(politician_contact_number=username_or_contact)
                else:
                    politician = Politician.objects.get(politician_name=username_or_contact)

                if check_password(password, politician.politician_password):
                    request.session['politician_id'] = politician.politician_id
                    return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
            except Politician.DoesNotExist:
                return Response({"error": "Politician not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



# # Religion api

from .models import Religion
from .serializers import ReligionSerializer

class ReligionListCreate(generics.ListCreateAPIView):
    queryset = Religion.objects.all()
    serializer_class = ReligionSerializer

class ReligionRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Religion.objects.all() 
    serializer_class = ReligionSerializer


# Favour non-favour api

# from .models import Favour_non_favour
# from .serializers import Favour_non_favourSerializer

# class Favour_non_favourListCreate(generics.ListCreateAPIView):
#     queryset = Favour_non_favour.objects.all()
#     serializer_class = Favour_non_favourSerializer

# class Favour_non_favourRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Favour_non_favour.objects.all() 
#     serializer_class = Favour_non_favourSerializer


from .serializers import Favour_non_favourSerializer

class Favour_non_favourRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voterlist.objects.all()
    serializer_class = Favour_non_favourSerializer



# town_user login

from .serializers import Town_userLoginSerializer
from .models import Town_user 

from .serializers import Town_userLoginSerializer
from .models import Town_user 

# class Town_userLogin(APIView):
#     def post(self, request):
#         serializer = Town_userLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             town_user_name = serializer.validated_data.get('town_user_name')
#             town_user_password = serializer.validated_data.get('town_user_password')

#             try:
#                 town_user = Town_user.objects.get(town_user_name=town_user_name)

#             except Town_user.DoesNotExist:
#                 return Response({"message": "Invalid name credentials"}, status=status.HTTP_401_UNAUTHORIZED) 


#             # if check_password(town_user_password, town_user.town_user_password)
#             if town_user_password == town_user.town_user_password:
#                 request.session['town_user_id'] = town_user.town_user_id
#                 town_user_town_id = town_user.town_user_town_id 
#                 response_data = {
#                     "message": "Login successful",
#                     "town_user_town_id": town_user_town_id  # Include town_user_town_id in the response
#                 }
#                 print(request.session.get('town_user_id'))
#                 return Response(response_data, status=status.HTTP_200_OK)
#             else:
#                 return Response({"message": "Invalid password credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .serializers import Town_userLoginSerializer
from .models import Town_user
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Town_userLogin(APIView):
    def post(self, request):
        serializer = Town_userLoginSerializer(data=request.data)
        if serializer.is_valid():
            town_user_name = serializer.validated_data.get('town_user_name')
            town_user_password = serializer.validated_data.get('town_user_password')

            try:
                town_user = Town_user.objects.get(town_user_name=town_user_name)
            except Town_user.DoesNotExist:
                return Response({"message": "Invalid name credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            # if check_password(town_user_password, town_user.town_user_password)
            if town_user_password == town_user.town_user_password:
                request.session['town_user_id'] = town_user.town_user_id
                town_user_id = town_user.town_user_id  # Get the town_user_id
                response_data = {
                    "message": "Login successful",
                    "town_user_id": town_user_id  # Include town_user_id in the response
                }
                print(request.session.get('town_user_id'))
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid password credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# town_user register

# from .models import Town_user
# from .serializers import Town_userSerializer

# class Town_userCreate(generics.ListCreateAPIView):
#     queryset = Town_user.objects.all()
#     serializer_class = Town_userSerializer

#     def perform_create(self, serializer):
#         session_id = self.request.session.get('politician_id')
#         serializer.save(town_user_politician_id=session_id) 


from .models import Town_user
from .serializers import TownUserRegistrationSerializer, UserTown, UserTownSerializer

class Town_userCreate(generics.ListCreateAPIView):
    queryset = Town_user.objects.all()
    serializer_class = TownUserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  
        
        if serializer.is_valid():
            user_data = {
                'town_user_name': serializer.validated_data['town_user_name'],
                'town_user_password': serializer.validated_data['town_user_password'],
                'town_user_contact_number': serializer.validated_data['town_user_contact_number'],
            }

            town_user = Town_user(**user_data)  
            town_user.town_user_politician_id = request.session.get('politician_id')
            town_user.save()

            town_ids = serializer.validated_data['town_ids']
            for town_id in town_ids:
                UserTown.objects.create(user_town_town_user_id=town_user.town_user_id, user_town_town_id=town_id)

            return Response({'status': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get_town_voter

def get_town_voter_list(request, town_user_town_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT
                v.voter_id, 
                v.voter_name, 
                b.booth_id, 
                b.booth_name, 
                t.town_id, 
                t.town_name,
                v.voter_parent_name,
                v.voter_house_number,
                v.voter_age,
                v.voter_gender,
                v.voter_cast,
                v.voter_contact_number
            FROM 
                tbl_voter v
            JOIN 
                tbl_booth b ON v.voter_booth_id = b.booth_id
            JOIN 
                tbl_town t ON b.booth_town_id = t.town_id
            JOIN 
                tbl_town_user tu ON t.town_id = tu.town_user_town_id
            WHERE 
                tu.town_user_town_id = %s;
        """, [town_user_town_id])
        results = cursor.fetchall()

    voters = []
    for row in results:
        voters.append({
            'voter_id': row[0],
            'voter_name': row[1],
            'booth_id': row[2],
            'booth_name': row[3],
            'town_id': row[4],
            'town_name': row[5],
            'voter_parent_name': row[6],
            'voter_house_number': row[7],
            'voter_age': row[8],
            'voter_gender': row[9],
            'voter_cast': row[10],
            'voter_contact_number': row[11]
        })

    return JsonResponse({'voters': voters})



# get_taluka_voter_list

def get_taluka_voter_list(request, politician_taluka_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                v.voter_id, 
                v.voter_name, 
                b.booth_id, 
                b.booth_name, 
                t.town_id, 
                t.town_name,
                v.voter_parent_name,
                v.voter_house_number,
                v.voter_age,
                v.voter_gender,
                v.voter_cast,
                v.voter_contact_number
            FROM 
                tbl_voter v
            JOIN 
                tbl_booth b ON v.voter_booth_id = b.booth_id
            JOIN 
                tbl_town t ON b.booth_town_id = t.town_id
            JOIN 
                tbl_panchayat_samiti ps ON ps.panchayat_samiti_id = t.town_panchayat_samiti_id
            JOIN 
                tbl_politician p ON p.politician_taluka_id = ps.panchayat_samiti_id
            
            
            WHERE 
                p.politician_taluka_id = %s;
        """, [politician_taluka_id])
        results = cursor.fetchall()

    voters = []
    for row in results:
        voters.append({
            'voter_id': row[0],
            'voter_name': row[1],
            'booth_id': row[2],
            'booth_name': row[3],
            'town_id': row[4],
            'town_name': row[5],
            'voter_parent_name': row[6],
            'voter_house_number': row[7],
            'voter_age': row[8],
            'voter_gender': row[9],
            'voter_cast': row[10],
            'voter_contact_number': row[11]
        })

    return JsonResponse({'voters': voters})


# constituency wise voter api

from .serializers import VoterlistSerializer

class VotersByConstituencyView(generics.ListAPIView):
    serializer_class = VoterlistSerializer

    def get_queryset(self):
        constituency_id = self.kwargs['constituency_id']
        return Voterlist.objects.filter(voter_constituency_id=constituency_id)

# voter data updateed date and time

from .models import MaritalStatus
from .serializers import MaritalStatusSerializer

class MaritalStatusRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MaritalStatus.objects.all()
    serializer_class = MaritalStatusSerializer


# Get voter list by constituency wise

from django.http import JsonResponse
from django.db import connection

def get_voters_by_constituency(request, constituency_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.voter_id, v.voter_name, c.constituency_name, v.voter_contact_number, v.voter_cast, 
                   v.voter_favour_id, v.voter_booth_id, v.voter_town_id, v.voter_parent_name, 
                   v.voter_age, v.voter_gender, v.voter_marital_status_id
            FROM tbl_voter v
            JOIN tbl_constituency c ON c.constituency_id = v.voter_constituency_id
            WHERE v.voter_constituency_id = %s
        """, [constituency_id])
        results = cursor.fetchall()
    
    voters = []
    for row in results:
        voters.append({
            'voter_id': row[0],
            'voter_name': row[1],
            'constituency_name': row[2],
            'voter_contact_number': row[3],
            'voter_cast': row[4],
            'voter_favour_id': row[5],
            'voter_booth_id': row[6],
            'voter_town_id': row[7],
            'voter_parent_name': row[8],
            'voter_age': row[9],
            'voter_gender': row[10],
            'voter_marital_status_id': row[11] 
        })
    
    return JsonResponse({'voters': voters})


# Get voters by user wise (assign by multi booth wise)

def get_voters_by_userwise(request, user_booth_user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.voter_id, 
            	   v.voter_name, 
            	   v.voter_parent_name, 
            	   v.voter_age, 
            	   v.voter_gender, 
            	   v.voter_contact_number,
                   v.voter_dob,
                   v.voter_cast, 
                   t.town_id,
            	   t.town_name,
            	   b.booth_id,
            	   b.booth_name,
                   r.religion_id,
                   r.religion_name,
                   f.favour_id,
                   f.favour_type,
                   ct.constituency_id,
                   ct.constituency_name,
                   u.user_id,
                   u.user_name,
                   d.live_status_id,
                   d.live_status_type      
                
            FROM tbl_voter v
            JOIN 
                tbl_booth b ON v.voter_booth_id = b.booth_id
            JOIN 
                tbl_town t ON v.voter_town_id = t.town_id
            LEFT JOIN
            	tbl_religion r ON v.voter_religion_id = r.religion_id
            LEFT JOIN
                tbl_favour f ON v.voter_favour_id = f.favour_id
            LEFT JOIN
                tbl_constituency ct ON v.voter_constituency_id = ct.constituency_id
            LEFT JOIN
                 tbl_user u ON v.voter_updated_by = u.user_id
            LEFT JOIN
                 tbl_live_status d ON v.voter_live_status_id = d.live_status_id        
            INNER JOIN (
                SELECT user_booth_booth_id AS booth_id
                FROM tbl_user_booth
                WHERE user_booth_user_id = %s
            ) AS temp_booth_ids ON v.voter_booth_id = temp_booth_ids.booth_id;
        """, [user_booth_user_id])
        results = cursor.fetchall()

    voters = []
    for row in results:
        voters.append({
            'voter_id': row[0],
            'voter_name': row[1],
            'voter_parent_name': row[2], 
            'voter_age': row[3],
            'voter_gender': row[4],
            'voter_contact_number': row[5],
            'voter_date_of_birth': row[6],
            'voter_cast' : row[7],
            'town_name' : row[9],
            'booth_id' : row[10],
            'booth_name' : row[11], 
            'voter_religion' : row[13],
            'voter_favour_id' : row[14],
            'voter_favour_type' : row[15],
            'voter_constituency' : row[17],
            'voter_data_edited_by': row[19],
            'voter_live_status_id' : row[20],
            'voter_live_status_type': row[21]
            
        })
    
    return JsonResponse({'voters': voters})


# get edited data with user wise

class EditedVoterlistList(generics.ListAPIView):
    serializer_class = VoterlistSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Voterlist.objects.filter(voter_updated_by=user_id)  # Fetch edited records by specific user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# get updated data date wise

from rest_framework.exceptions import ValidationError
from datetime import datetime

class EditedVoterlistByDate(generics.ListAPIView):
    serializer_class = VoterlistSerializer

    def get_queryset(self):
        date_str = self.kwargs.get('date')
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError('Invalid date format. Use YYYY-MM-DD.')
            return Voterlist.objects.filter(voter_updated_date=date)
        return Voterlist.objects.none()  # No date provided, return empty queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# get voters list by town wise

from rest_framework import generics
from .models import Voterlist
from .serializers import VoterlistSerializer

class VoterlistByTown(generics.ListAPIView):
    serializer_class = VoterlistSerializer

    def get_queryset(self):
        town_id = self.kwargs['town_id']
        return Voterlist.objects.filter(voter_town_id=town_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

# voter count

class VoterCountView(APIView):
    def get(self, request, *args, **kwargs):
        sql_query = 'SELECT COUNT(*) AS count FROM vote.tbl_voter;'

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            row = cursor.fetchone()

        count = row[0] if row else 0

        data = {'count': count}

        return Response(data, status=status.HTTP_200_OK)
    

# voter count by booth wise

def VoterCountByBoothView(request, voter_booth_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM vote.tbl_voter WHERE voter_booth_id = %s;
        """, [voter_booth_id])
        row = cursor.fetchone()  

    result = {
        'booth_wise_voter_count': row[0] if row else 0
    }

    return JsonResponse(result)




# Booth List By Town wise

class BoothListByTown(generics.ListAPIView):
    serializer_class = BoothSerializer

    def get_queryset(self):
        town_id = self.kwargs['town_id']
        return Booth.objects.filter(booth_town_id=town_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# Total Voter List
from django.views.decorators.http import require_http_methods
@require_http_methods(["GET"])
def total_voters(request):
    try:
        # Define the SQL query
        sql_query = "SELECT voter_id, voter_name FROM tbl_voter ; "
        
        # Execute the raw SQL query
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            # Fetch all rows from the executed query
            rows = cursor.fetchall()
        
        # Convert rows to a list of dictionaries
        voter_list = [{'voter_id': row[0], 'voter_name': row[1]} for row in rows]
        
        # Return the result as a JSON response
        return JsonResponse(voter_list, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from django.http import JsonResponse
from django.core.paginator import Paginator

def get_all_voters(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)  # Adjust page size as needed

    cursor = connection.cursor()
    cursor.callproc('sp_voter_list')
    results = cursor.fetchall()

    voters = [{
        'voter_id': row[0],
        'voter_name': row[1],
        'booth_name': row[2]
    } for row in results]

    paginator = Paginator(voters, page_size)
    paginated_voters = paginator.get_page(page)

    data = {
        'voters': list(paginated_voters),
        'page': paginated_voters.number,
        'pages': paginated_voters.paginator.num_pages,
    }

    return JsonResponse(data)
    

# Booth Count api

class BoothCountView(APIView):
    def get(self, request, *args, **kwargs):
        sql_query = 'SELECT COUNT(*) AS count FROM vote.tbl_booth;'

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            row = cursor.fetchone()

        count = row[0] if row else 0

        data = {'count': count}

        return Response(data, status=status.HTTP_200_OK)


# Town Count api

class TownCountView(APIView):
    def get(self, request, *args, **kwargs):
        sql_query = 'SELECT COUNT(*) AS count FROM vote.tbl_town;'

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            row = cursor.fetchone()

        count = row[0] if row else 0

        data = {'count': count}

        return Response(data, status=status.HTTP_200_OK)
    

# religion api

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Voterlist, Religion
from .serializers import VoterlistSerializer, ReligionSerializer

class ReligionListView(generics.ListAPIView):
    queryset = Religion.objects.all()
    serializer_class = ReligionSerializer

class VoterlistByReligion(APIView):
    def get(self, request, religion_id=None):
        if religion_id:
            try:
                religion = Religion.objects.get(religion_id=religion_id)
                voters = Voterlist.objects.filter(voter_religion_id=religion.religion_id)
                serializer = VoterlistSerializer(voters, many=True)
                return Response({
                    'religion_id': religion.religion_id,
                    'religion_name': religion.religion_name,
                    'voters': serializer.data
                })
            except Religion.DoesNotExist:
                return Response({'error': 'Religion not found'}, status=404)
        else:
            return Response({'error': 'Religion ID is required'}, status=400)
        
# Religion wise voter data 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Voterlist, Religion
from .serializers import VoterlistSerializer

class VoterlistByReligionView(APIView):
    def get(self, request, religion_id):
        try:
            # Check if the religion exists
            religion = Religion.objects.get(religion_id=religion_id)
            # Get voters with the specified religion_id
            voters = Voterlist.objects.filter(voter_religion_id=religion.religion_id)
            # Serialize the voter data
            serializer = VoterlistSerializer(voters, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Religion.DoesNotExist:
            return Response({'error': 'Religion not found'}, status=status.HTTP_404_NOT_FOUND)



# Remove multi Booth API

class UserBoothDeleteView(APIView):
    def delete(self, request, user_booth_user_id):
        user_booth_booth_id = request.data.get('user_booth_booth_id')

        if not user_booth_booth_id:
            return Response({'error': 'user_booth_booth_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        sql_query = """
            DELETE FROM vote.tbl_user_booth 
            WHERE user_booth_user_id = %s 
            AND user_booth_booth_id = %s
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query, [user_booth_user_id, user_booth_booth_id])
                if cursor.rowcount == 0:
                    return Response({'message': 'No records found to delete'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message': 'Record deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# Remove multi town API

class TownUserTownDeleteView(APIView):
    def delete(self, request, user_town_town_user_id):
        user_town_town_id = request.data.get('user_town_town_id')

        if not user_town_town_id:
            return Response({'error': 'user_town_town_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Write the SQL DELETE query
        sql_query = """
            DELETE FROM vote.tbl_user_town
            WHERE user_town_town_user_id = %s 
            AND user_town_town_id = %s
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query, [user_town_town_user_id, user_town_town_id])
                if cursor.rowcount == 0:
                    return Response({'message': 'No records found to delete'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'message': 'Record deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# Api for storing panchayat samiti circle and assigning to the town

from .serializers import PanchayatSamitiCircleSerializer
from .models import PanchayatSamitiCircle

@api_view(['POST'])
def update_town_panchayat(request):
    town_ids = request.data.get('town_ids')  # Expecting a list of town IDs
    panchayat_samiti_circle_name = request.data.get('panchayat_samiti_circle_name')
    
    if not town_ids or not isinstance(town_ids, list) or not panchayat_samiti_circle_name:
        return Response({'error': 'Both town_ids (as an array) and panchayat_samiti_circle_name are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Check if the PanchayatSamitiCircle exists or create a new one
        panchayat_circle, created = PanchayatSamitiCircle.objects.get_or_create(
            panchayat_samiti_circle_name=panchayat_samiti_circle_name
        )
        
        # Update each town with the panchayat_samiti_circle_id
        towns_updated = []
        for town_id in town_ids:
            try:
                town = Town.objects.get(town_id=town_id)
                town.town_panchayat_samiti_circle_id = panchayat_circle.panchayat_samiti_circle_id
                town.save()
                towns_updated.append(town_id)
            except Town.DoesNotExist:
                continue  # Skip towns that do not exist
        
        if not towns_updated:
            return Response({'error': 'None of the provided town_ids were found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'success': 'Towns updated successfully.', 'updated_town_ids': towns_updated}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

#API for get panchayat samiti circle

def get_panchayat_samiti_circle(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT panchayat_samiti_circle_id, panchayat_samiti_circle_name FROM tbl_panchayat_samiti_circle")
        rows = cursor.fetchall()
        
    # Convert the result into a list of dictionaries
    result = [
        {
            "panchayat_samiti_circle_id": row[0],
            "panchayat_samiti_circle_name": row[1]
        }
        for row in rows
    ]
    
    return JsonResponse(result, safe=False)


from .models import ZpCircle
@api_view(['POST'])
def update_panchayat_circle(request):
    panchayat_samiti_circle_ids = request.data.get('panchayat_samiti_circle_ids')  # Expecting a list of town IDs
    zp_circle_name = request.data.get('zp_circle_name')
    
    if not panchayat_samiti_circle_ids or not isinstance(panchayat_samiti_circle_ids, list) or not zp_circle_name:
        return Response({'error': 'Both town_ids (as an array) and panchayat_samiti_circle_name are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Check if the PanchayatSamitiCircle exists or create a new one
        zp_circle, created = ZpCircle.objects.get_or_create(
            zp_circle_name= zp_circle_name
        )
        
        # Update each town with the panchayat_samiti_circle_id
        panchayatsamiti_updated = []
        for panchayat_samiti_circle_id in panchayat_samiti_circle_ids:
            try:
                panchayatSamitiCircle = PanchayatSamitiCircle.objects.get(panchayat_samiti_circle_id = panchayat_samiti_circle_id)
                panchayatSamitiCircle.panchayat_samiti_circle_zp_circle_id = zp_circle.zp_circle_id
                panchayatSamitiCircle.save()
                panchayatsamiti_updated.append(panchayat_samiti_circle_id)
            except PanchayatSamitiCircle.DoesNotExist:
                continue  # Skip towns that do not exist
        
        if not panchayatsamiti_updated:
            return Response({'error': 'None of the provided town_ids were found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'success': 'Towns updated successfully.', 'updated_town_ids': panchayatsamiti_updated}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# get voter list by zp circle wise

@require_http_methods(["GET"])
def get_voter_list_by_zpcircle(request, zp_circle_id):
    try:
        zp_circle_id = int(zp_circle_id)
    except ValueError:
        return JsonResponse({'error': 'zp_circle_id must be an integer'}, status=400)

    with connection.cursor() as cursor:
        cursor.callproc('sp_vw_GetVoterListByZpCircleId', [zp_circle_id])
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

    results_list = [dict(zip(columns, row)) for row in results]

    return JsonResponse(results_list, safe=False)


# get voter list by panchayat samiti circle

@require_http_methods(["GET"])
def get_voter_list_by_panchayat_samiti_circle(request, panchayat_samiti_circle_id):
    try:
        panchayat_samiti_circle_id = int(panchayat_samiti_circle_id)
    except ValueError:
        return JsonResponse({'error': 'zp_circle_id must be an integer'}, status=400)

    with connection.cursor() as cursor:
        cursor.callproc('sp_vw_GetVoterListByPanchayatSamitiCircleId', [panchayat_samiti_circle_id])
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

    results_list = [dict(zip(columns, row)) for row in results]

    return JsonResponse(results_list, safe=False)


# activity log

class VoterUpdatedBy(View):
    def get(self, request, args, *kwargs):
        voter_updated_by = kwargs.get('voter_updated_by')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT voter_id, voter_name
                FROM vote.tbl_voter
                WHERE voter_updated_by = %s
            """, [voter_updated_by])
            rows = cursor.fetchall()
        
        result = [{'voter_id': row[0], 'voter_name': row[1]} for row in rows]
        
        return JsonResponse(result, safe=False)



# get zp circle names

@require_http_methods(["GET"])
def get_zp_circle_names(request, zp_circle_id=None):
    try:
        with connection.cursor() as cursor:
            if zp_circle_id:
                cursor.execute("SELECT zp_circle_id, zp_circle_name FROM tbl_zp_circle WHERE zp_circle_id = %s", [zp_circle_id])
            else:
                cursor.execute("SELECT zp_circle_id, zp_circle_name FROM tbl_zp_circle")
                
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

        zp_circle_list = [dict(zip(columns, row)) for row in results]
        return JsonResponse(zp_circle_list, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

# get PS circle names
    
@require_http_methods(["GET"])
def get_panchayat_samiti_circle_names(request, panchayat_samiti_circle_id=None):
    try:
        with connection.cursor() as cursor:
            if panchayat_samiti_circle_id:
                cursor.execute("SELECT panchayat_samiti_circle_id, panchayat_samiti_circle_name FROM tbl_panchayat_samiti_circle WHERE panchayat_samiti_circle_id = %s", [panchayat_samiti_circle_id])
            else:
                cursor.execute("SELECT panchayat_samiti_circle_id, panchayat_samiti_circle_name FROM tbl_panchayat_samiti_circle")
                
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

        psc_circle_list = [dict(zip(columns, row)) for row in results]
        return JsonResponse(psc_circle_list, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# get town user info 

def get_town_user_info(request):
    with connection.cursor() as cursor:
        cursor.callproc('vote.GetTownUserInfo')
        result = cursor.fetchall()
        
        data = [dict(zip([desc[0] for desc in cursor.description], row)) for row in result]

    return JsonResponse(data, safe=False)


def get_town_user_info_with_id(request, user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return HttpResponseBadRequest("Invalid 'id' parameter")

    with connection.cursor() as cursor:
        cursor.callproc('vote.GetTownUserInfoWithId', [user_id])
        result = cursor.fetchall()
        
        data = [dict(zip([desc[0] for desc in cursor.description], row)) for row in result]

    return JsonResponse(data, safe=False)



# get booth user info 

def get_booth_user_info(request):
    with connection.cursor() as cursor:
        cursor.callproc('vote.GetBoothUserInfo')
        result = cursor.fetchall()
        
        data = [dict(zip([desc[0] for desc in cursor.description], row)) for row in result]

    return JsonResponse(data, safe=False)


def get_booth_user_info_with_id(request, user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return HttpResponseBadRequest("Invalid 'id' parameter")

    with connection.cursor() as cursor:
        cursor.callproc('vote.GetBoothUserInfoWithId', [user_id])
        result = cursor.fetchall()
        
        data = [dict(zip([desc[0] for desc in cursor.description], row)) for row in result]

    return JsonResponse(data, safe=False)


# Get Town user wise voter data

def get_voter_list_by_town_user(request, user_town_town_user_id):
    try:
        user_id = int(user_town_town_user_id)
    except ValueError:
        return HttpResponseBadRequest("Invalid 'user_id' parameter")

    with connection.cursor() as cursor:
        cursor.callproc('sp_GetVoterListByTownUser', [user_town_town_user_id])
        result = cursor.fetchall()
        
        data = [dict(zip([desc[0] for desc in cursor.description], row)) for row in result]

    return JsonResponse(data, safe=False)

    