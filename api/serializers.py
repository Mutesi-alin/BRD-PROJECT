


from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from user.models import User
from clients.models import Client
from projects.models import Project
from loans.models import Loan
from disbursement.models import Disbursement



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'password'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number', 'role'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class RoleUpdateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)



class ClientSerializer(serializers.ModelSerializer):
    national_id = serializers.CharField(max_length=16, min_length=16)

    class Meta:
        model = Client
        fields = '__all__'

    def validate_national_id(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("National ID must contain only digits.")
        if len(value) != 16:
            raise serializers.ValidationError("National ID must be exactly 16 digits.")
        return value



class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

    def validate_status(self, value):
        # On create
        if not self.instance:
            if value != 'PENDING':
                raise serializers.ValidationError("New projects must start as PENDING.")
            return value

        # On update
        current_status = self.instance.status
        allowed = Project.VALID_TRANSITIONS.get(current_status, [])

        if value not in allowed:
            raise serializers.ValidationError(
                f"Cannot change status from '{current_status}' to '{value}'. "
                f"Allowed transitions: {allowed}"
            )

        return value

class LoanSerializer(serializers.ModelSerializer):
    tenure_display = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['approved_by', 'approval_date', 'tenure_display']

    def get_tenure_display(self, obj):
        return f"{obj.tenure} months"

    def validate_project(self, value):
        if value.status != 'APPROVED':
            raise serializers.ValidationError(
                f"Project '{value.name}' must be approved before a loan can be created. "
                f"Current status: {value.status}"
            )
        return value

    def validate_status(self, value):
        # On CREATE - only PENDING is allowed
        if not self.instance:
            if value != 'PENDING':
                raise serializers.ValidationError(
                    "New loans must start with PENDING status."
                )
            return value

        # On UPDATE - only ADMIN or MANAGEMENT can change status
        current_status = self.instance.status
        if value != current_status:
            user = self.context['request'].user
            if user.role not in ['ADMIN', 'MANAGEMENT']:
                raise serializers.ValidationError(
                    "Only ADMIN or MANAGEMENT can change loan status."
                )
        return value

    def create(self, validated_data):
        # Force status to PENDING regardless of what was sent
        validated_data['status'] = 'PENDING'
        validated_data.pop('approved_by', None)
        validated_data.pop('approval_date', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Auto-fill approved_by and approval_date when status changes to APPROVED
        if validated_data.get('status') == 'APPROVED' and instance.status != 'APPROVED':
            from django.utils import timezone
            validated_data['approved_by'] = self.context['request'].user
            validated_data['approval_date'] = timezone.now().date()

        return super().update(instance, validated_data)

class DisbursementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disbursement
        fields = '__all__'
        read_only_fields = ['created_by']

    def validate_loan(self, value):
        if value.status != 'APPROVED':
            raise serializers.ValidationError(
                f"Disbursement not allowed. Loan status must be APPROVED. Current: {value.status}"
            )
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
