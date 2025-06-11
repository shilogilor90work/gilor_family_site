# finance_tracker/serializers.py

from rest_framework import serializers
from .models import FamilyMember, Account, TransactionCategory, Transaction, Budget
from django.contrib.auth.models import User
# finance_tracker/serializers.py
from django.contrib.auth.password_validation import validate_password # For strong password validation

# --- Helper Serializers (for nested data or specific fields) ---
# --- Helper Serializers (for nested data or specific fields) ---

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class FamilyMemberSmallSerializer(serializers.ModelSerializer):
    """
    Used for nested representation when only basic member info is needed.
    """
    user = UserSerializer(read_only=True)
    class Meta:
        model = FamilyMember
        fields = ['id', 'name', 'user']


# --- Main Model Serializers ---

class FamilyMemberSerializer(serializers.ModelSerializer):
    """
    Full serializer for FamilyMember, including nested User data.
    """
    user = UserSerializer(read_only=True) # User is read-only for FamilyMember creation
    # You might want to include accounts and budgets here as nested serializers if needed
    # accounts = AccountSerializer(many=True, read_only=True)
    # budgets = BudgetSerializer(many=True, read_only=True)

    class Meta:
        model = FamilyMember
        fields = ['id', 'name', 'user']

class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the Account model.
    Includes the FamilyMember name for readability.
    """
    member = FamilyMemberSmallSerializer(read_only=True) # Display member name, not just ID

    class Meta:
        model = Account
        fields = ['id', 'member', 'account_name', 'balance_current', 'currency']
        read_only_fields = ['balance_current'] # Balance is updated by transactions, not directly set via API

class TransactionCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for TransactionCategory.
    """
    class Meta:
        model = TransactionCategory
        fields = ['id', 'name', 'type']

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    Handles creation and display of transactions.
    """
    account_name = serializers.CharField(source='account.account_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    member_name = serializers.CharField(source='account.member.name', read_only=True)


    class Meta:
        model = Transaction
        fields = [
            'id', 'account', 'account_name', 'member_name', 'category', 'category_name',
            'amount', 'description', 'date', 'type'
        ]
        # 'account' and 'category' are writable (Foreign Key IDs)
        # 'account_name', 'category_name', 'member_name' are read-only for display purposes

class BudgetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Budget model.
    """
    member = FamilyMemberSmallSerializer(read_only=True)
    category = TransactionCategorySerializer(read_only=True) # Display category details

    # Writable fields for creation/update
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=FamilyMember.objects.all(), source='member', write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TransactionCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Budget
        fields = [
            'id', 'member', 'member_id', 'category', 'category_id',
            'amount_monthly', 'start_date', 'end_date'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class FamilyMemberSmallSerializer(serializers.ModelSerializer):
    """
    Used for nested representation when only basic member info is needed.
    """
    user = UserSerializer(read_only=True)
    class Meta:
        model = FamilyMember
        fields = ['id', 'name', 'user']

# --- New: User Registration Serializer ---
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    family_member_name = serializers.CharField(write_only=True, required=True, max_length=255) # New field for family member's name

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'family_member_name']
        extra_kwargs = {
            'email': {'required': False} # Email is optional for this
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 and family_member_name as they are not User model fields
        validated_data.pop('password2')
        family_member_name = validated_data.pop('family_member_name')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        # The FamilyMember will be created automatically via a signal
        return user
