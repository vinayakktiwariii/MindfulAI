# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status, generics, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.utils import timezone
# from datetime import timedelta
# import secrets

# from .models import User, UserSession, PasswordResetToken
# from .serializers import (
#     UserRegistrationSerializer, UserLoginSerializer,
#     UserProfileSerializer, UserProfileUpdateSerializer,
#     PasswordChangeSerializer, PasswordResetRequestSerializer,
#     PasswordResetConfirmSerializer
# )

# @api_view(['GET'])
# def users_api_root(request):
#     """Users API root"""
#     return Response({
#         'message': 'Users API',
#         'endpoints': {
#             'register': '/api/users/register/',
#             'login': '/api/users/login/',
#             'logout': '/api/users/logout/',
#             'profile': '/api/users/profile/',
#             'password_change': '/api/users/password/change/',
#             'password_reset': '/api/users/password/reset/',
#         }
#     })

# def get_tokens_for_user(user):
#     """Generate JWT tokens for user"""
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


# class RegisterView(APIView):
#     """User registration endpoint"""
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             tokens = get_tokens_for_user(user)
            
#             # Create session
#             UserSession.objects.create(
#                 user=user,
#                 token=tokens['access'],
#                 ip_address=request.META.get('REMOTE_ADDR'),
#                 user_agent=request.META.get('HTTP_USER_AGENT', ''),
#                 expires_at=timezone.now() + timedelta(days=30)
#             )
            
#             return Response({
#                 'message': 'Registration successful',
#                 'user': UserProfileSerializer(user).data,
#                 'tokens': tokens
#             }, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     """User login endpoint"""
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             tokens = get_tokens_for_user(user)
            
#             # Update last login
#             user.last_login_at = timezone.now()
#             user.save(update_fields=['last_login_at'])
            
#             # Create session
#             UserSession.objects.create(
#                 user=user,
#                 token=tokens['access'],
#                 ip_address=request.META.get('REMOTE_ADDR'),
#                 user_agent=request.META.get('HTTP_USER_AGENT', ''),
#                 expires_at=timezone.now() + timedelta(days=30)
#             )
            
#             return Response({
#                 'message': 'Login successful',
#                 'user': UserProfileSerializer(user).data,
#                 'tokens': tokens
#             }, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     """User logout endpoint"""
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self, request):
#         try:
#             # Deactivate all user sessions
#             UserSession.objects.filter(user=request.user, is_active=True).update(is_active=False)
#             return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class ProfileView(generics.RetrieveUpdateAPIView):
#     """Get and update user profile"""
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return UserProfileSerializer
#         return UserProfileUpdateSerializer
    
#     def get_object(self):
#         return self.request.user


# class PasswordChangeView(APIView):
#     """Change password"""
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self, request):
#         serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             request.user.set_password(serializer.validated_data['new_password'])
#             request.user.save()
            
#             # Deactivate all sessions
#             UserSession.objects.filter(user=request.user).update(is_active=False)
            
#             return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetRequestView(APIView):
#     """Request password reset"""
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = PasswordResetRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             user = User.objects.get(email=email)
            
#             # Generate reset token
#             token = secrets.token_urlsafe(32)
#             PasswordResetToken.objects.create(
#                 user=user,
#                 token=token,
#                 expires_at=timezone.now() + timedelta(hours=24)
#             )
            
#             # TODO: Send email with reset link
#             # send_password_reset_email(user.email, token)
            
#             return Response({
#                 'message': 'Password reset email sent',
#                 'token': token  # Remove in production, send via email only
#             }, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetConfirmView(APIView):
#     """Confirm password reset"""
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         serializer = PasswordResetConfirmSerializer(data=request.data)
#         if serializer.is_valid():
#             token = serializer.validated_data['token']
            
#             try:
#                 reset_token = PasswordResetToken.objects.get(
#                     token=token,
#                     is_used=False,
#                     expires_at__gt=timezone.now()
#                 )
#             except PasswordResetToken.DoesNotExist:
#                 return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
            
#             # Reset password
#             user = reset_token.user
#             user.set_password(serializer.validated_data['new_password'])
#             user.save()
            
#             # Mark token as used
#             reset_token.is_used = True
#             reset_token.save()
            
#             # Deactivate all sessions
#             UserSession.objects.filter(user=user).update(is_active=False)
            
#             return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    full_name = request.data.get('full_name', '')
    
    if not username or not email or not password:
        return Response(
            {'error': 'Username, email, and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        full_name=full_name
    )
    
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'message': 'User registered successfully',
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
        },
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get current authenticated user"""
    user = request.user
    return Response({
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'total_conversations': user.total_conversations,
        'total_messages': user.total_messages,
    })
