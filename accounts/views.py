from rest_framework import status
from rest_framework.generics import *
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from .models import Customer
from payment.models import Balance
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from payment.models import Invoice
from payment.serializers import InvoiceSerializer

class RegistrationView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        if not request.data:  # Check if the request data is empty
            return Response({'message': 'No data provided in the request.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Generate an activation token
        auth_token, _ = Token.objects.get_or_create(user=user)
        Balance.objects.create(
            order_id="order_id",
            balance=0,
            created_by=user
        )
        total_products = Invoice.objects.filter(sold=True, created_by=user, received__gte=0).count()
        # Include the token key in the response data
        response_data = {
            'message': 'User registered successfully',
            'token': auth_token.key, # Serialize the token key as a string
            "username":user.username,
            "email":user.email,
            "total_products":total_products
        }

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = True
        user.set_password(serializer.validated_data['password'])
        user.save()

        return user

class AccountActivate(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Customer.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Activation failed"}, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.data:  # Check if the request data is empty
            return Response({'message': 'No data provided in the request.'}, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = Customer.objects.get(email=email)
            if user.is_active:
                pass
            else:
                return Response({"message": "Account not activated"}, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            raise AuthenticationFailed(detail="Invalid Email")

        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed(detail="Invalid password")

        token, _ = Token.objects.get_or_create(user=user)

        # Log the user in within the session
        login(request, user)
        total_products = Invoice.objects.filter(sold=True, created_by=user, received__gte=0).count()
        return Response({"message": "Login successful", "token": token.key, "username":user.username,"email":user.email,"total_products":total_products}, status=status.HTTP_200_OK)

class UserLogoutView(GenericAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class DashboardView(ListAPIView):
    serializer_class = InvoiceSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        invoices = Invoice.objects.filter(sold=True, created_by=user, received__gte=0)
        return invoices
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        balance = Balance.objects.get(created_by=user).balance
        invoices = Invoice.objects.filter(sold=True, created_by=user, received__gte=0).count()
        response_data = {
            "username": user.username,
            "email": user.email,
            "invoices": serializer.data,
            "balance": balance,
            "total_products": invoices
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated] 

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.data:  # Check if the request data is empty
            return Response({'message': 'No data provided in the request.'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'message': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)