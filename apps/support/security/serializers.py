# Importaciones necesarias para los serializadores
from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group, Permission
from .models import UserProfile, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# ==================
# SERIALIZADOR DE LOGIN
# ==================

class LoginSerializer(serializers.Serializer):
    """
    Serializador para el proceso de autenticación/login.
    
    Características:
    - Valida credenciales (username/email y password)
    - Soporta login con username o email
    - Proporciona mensajes de error específicos en español
    - Incluye validación personalizada de credenciales
    
    Campos:
    - username: Puede ser username o email del usuario
    - password: Contraseña del usuario
    
    Uso:
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # Proceder con el login
    """
    
    # Campo que acepta tanto username como email
    username = serializers.CharField(
        max_length=150,
        help_text="Nombre de usuario o email",
        error_messages={
            'required': 'El nombre de usuario o email es requerido.',
            'blank': 'El nombre de usuario o email no puede estar vacío.',
            'max_length': 'El nombre de usuario o email es demasiado largo.'
        }
    )
    
    # Campo de contraseña
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Contraseña del usuario",
        error_messages={
            'required': 'La contraseña es requerida.',
            'blank': 'La contraseña no puede estar vacía.'
        }
    )
    
    def validate(self, attrs):
        """
        Validación personalizada para autenticar al usuario.
        
        Proceso:
        1. Extrae username/email y password de los datos
        2. Busca al usuario por username o email
        3. Verifica la contraseña
        4. Retorna el usuario autenticado o lanza error
        
        Args:
            attrs (dict): Datos validados del serializador
            
        Returns:
            dict: Datos validados incluyendo el usuario autenticado
            
        Raises:
            ValidationError: Si las credenciales son inválidas
        """
        identifier = attrs.get('username')
        password = attrs.get('password')
        user = None
        
        if identifier and password:
            # Intentar encontrar el usuario por username
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                # Si no se encuentra por username, intentar por email
                try:
                    user = User.objects.get(email=identifier)
                except User.DoesNotExist:
                    # Último intento: buscar en UserProfile por email
                    try:
                        profile = UserProfile.objects.get(user__email=identifier)
                        user = profile.user
                    except UserProfile.DoesNotExist:
                        user = None
            
            # Verificar si el usuario existe y la contraseña es correcta
            if user and user.check_password(password):
                # Verificar si el usuario está activo
                if not user.is_active:
                    raise serializers.ValidationError({
                        'non_field_errors': ['Esta cuenta está desactivada.']
                    })
                
                # Usuario autenticado exitosamente
                attrs['user'] = user
                return attrs
            else:
                # Credenciales inválidas
                raise serializers.ValidationError({
                    'non_field_errors': ['Credenciales inválidas. Verifica tu usuario/email y contraseña.']
                })
        else:
            # Faltan campos requeridos
            raise serializers.ValidationError({
                'non_field_errors': ['Debe proporcionar usuario/email y contraseña.']
            })
    
    def to_representation(self, instance):
        """
        Personaliza la representación de salida del serializador.
        No incluye datos sensibles como la contraseña.
        """
        if hasattr(instance, 'user'):
            user = instance['user']
            return {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'groups': [group.name for group in user.groups.all()]
            }
        return super().to_representation(instance)


# ==================
# SERIALIZADORES DE ROLES Y USUARIOS
# ==================

# Serializador básico para roles/grupos
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

# Serializador para grupos con permisos detallados
class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        required=False
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

# Serializador para usuarios del sistema
class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'groups']
        read_only_fields = ['is_active']


# Serializador principal para perfiles de usuario con datos extendidos
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    user_roles = serializers.SerializerMethodField()  # Roles del User (groups)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'birth_date', 'profile_picture', 'user_roles']

    def get_user_roles(self, obj):
        """Obtener los roles del User (groups)"""
        if obj.user:
            return [{'id': group.id, 'name': group.name} for group in obj.user.groups.all()]
        return []

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        return ret

    def update(self, instance, validated_data):
        # Actualizar campos del perfil
        user_data = validated_data.pop('user', {})

        if 'first_name' in user_data:
            instance.user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            instance.user.last_name = user_data['last_name']
        instance.user.save()

        return super().update(instance, validated_data)


# Serializador para el registro de nuevos usuarios
class RegisterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    roles = serializers.PrimaryKeyRelatedField(
     many=True,
     queryset=Group.objects.all(),
     required=False
     )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'roles', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        roles = validated_data.pop('roles', [])

        user = User.objects.create_user(**validated_data)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        if roles:
            for role in roles:
                user.groups.add(role)
                user.save()

        if profile_data:
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            profile_serializer = UserProfileSerializer(
             instance=user_profile,
             data=profile_data,
             partial=True,
             context={'request': self.context.get('request')}
            )
            if not profile_serializer.is_valid():
                raise serializers.ValidationError({'profile': profile_serializer.errors})
            profile_serializer.save()

        return user

# Serializador básico para perfiles
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'birth_date', 'profile_picture']
        extra_kwargs = {
            'phone': {'required': False},
            'address': {'required': False},
            'birth_date': {'required': False},
            'profile_picture': {'required': False}
        }


# Serializador para usuarios con perfil opcional
class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)

        if profile_data:
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            profile_serializer = ProfileSerializer(instance=user_profile, data=profile_data, partial=True, context={'request': self.context.get('request')})
            if not profile_serializer.is_valid():
                raise serializers.ValidationError({'profile': profile_serializer.errors})
            profile_serializer.save()

        return user
    

# Serializador personalizado para tokens JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = None
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError('No active account found with the given credentials')

        if user and user.check_password(password):
            return super().validate(attrs)
        else:
            raise serializers.ValidationError('No active account found with the given credentials')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        
        # Add user profile data to token
        try:
            user_profile = user.user_profile
            token['first_name'] = user.first_name
            token['last_name'] = user.last_name
            token['profile_picture'] = user_profile.profile_picture.url if user_profile.profile_picture else None
            token['role'] = user.groups.first().name if user.groups.exists() else 'cliente'
            token['phone'] = user_profile.phone
            token['address'] = user_profile.address
            token['birth_date'] = str(user_profile.birth_date) if user_profile.birth_date else None
        except:
            # If user profile doesn't exist, use default values
            token['first_name'] = user.first_name
            token['last_name'] = user.last_name
            token['profile_picture'] = None
            token['role'] = 'cliente'
            token['phone'] = None
            token['address'] = None
            token['birth_date'] = None
        
        return token


# Serializador para grupos/roles con permisos
class GroupWithPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


# Serializador para permisos de grupos
class GroupPermissionsSerializer(serializers.Serializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())
