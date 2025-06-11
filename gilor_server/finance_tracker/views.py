# finance_tracker/views.py

from rest_framework import viewsets, status, serializers, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from .models import FamilyMember, Account, TransactionCategory, Transaction, Budget
from .serializers import (
    FamilyMemberSerializer, AccountSerializer, TransactionCategorySerializer,
    TransactionSerializer, BudgetSerializer, UserRegistrationSerializer
)


# --- Standard Model ViewSets (for CRUD operations) ---

class MyFamilyMemberView(APIView):
    """
    API endpoint to get the currently logged-in user's FamilyMember profile.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            print(request)
            print(request.user)
            member = request.user.family_member
            print(member)
            serializer = FamilyMemberSerializer(member)
            print(serializer.data)
            return Response(serializer.data)
        except FamilyMember.DoesNotExist:
            return Response({"detail": "No FamilyMember profile found for this user. Please create one via admin or registration."},
                            status=status.HTTP_404_NOT_FOUND)



# --- Updated: FamilyMemberViewSet (now allows creation/linking explicitly) ---
class FamilyMemberViewSet(viewsets.ModelViewSet): # Changed from ReadOnlyModelViewSet
    """
    API endpoint that allows family members to be viewed, created, or edited.
    Creation allows linking to an existing Django User.
    """
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAuthenticated] # Basic auth for all actions here

    def get_queryset(self):
        # Superusers can see all family members
        if self.request.user.is_superuser:
            return FamilyMember.objects.all()
        # Regular users can only see their own family member profile
        try:
            return FamilyMember.objects.filter(user=self.request.user)
        except FamilyMember.DoesNotExist:
            return FamilyMember.objects.none()

    def perform_create(self, serializer):
        # If user_id is provided in the request, link to that user
        # This part should ideally be restricted to admins for security
        user_to_link = serializer.validated_data.get('user')

        if user_to_link: # user_id was explicitly provided
            if not self.request.user.is_superuser:
                # If a non-superuser tries to link to someone else, reject
                if user_to_link != self.request.user:
                    raise serializers.ValidationError("You do not have permission to link a FamilyMember to another user.")
            # If the user_id points to themselves (for non-superuser) or superuser linking anyone,
            # check if a FamilyMember already exists for that user
            if FamilyMember.objects.filter(user=user_to_link).exists():
                raise serializers.ValidationError(f"User '{user_to_link.username}' is already linked to a Family Member profile.")
            serializer.save(user=user_to_link)
        else: # user_id was NOT provided in the request
            # Automatically link to the current authenticated user IF they don't have a FamilyMember yet
            if FamilyMember.objects.filter(user=self.request.user).exists():
                 raise serializers.ValidationError("You already have a FamilyMember profile.")
            serializer.save(user=self.request.user) # Link to current authenticated user by default

    def perform_update(self, serializer):
        instance = self.get_object()
        # Only superusers can update other family members. Regular users can update their own.
        if not self.request.user.is_superuser and instance.user != self.request.user:
            raise serializers.ValidationError("You do not have permission to update this FamilyMember profile.")

        # Prevent changing the linked user via update if it's already set
        if 'user' in serializer.validated_data and serializer.validated_data['user'] != instance.user:
             raise serializers.ValidationError("Cannot change the linked user for an existing FamilyMember profile. Create a new one if needed.")

        serializer.save()

    def perform_destroy(self, instance):
        # Only superusers can delete other family members. Regular users can delete their own.
        if not self.request.user.is_superuser and instance.user != self.request.user:
            raise serializers.ValidationError("You do not have permission to delete this FamilyMember profile.")
        instance.delete()


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows accounts to be viewed or edited.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users only see and manage their own accounts
        if self.request.user.is_superuser:
            return Account.objects.all()
        # Assuming each user has one FamilyMember profile linked
        try:
            member = self.request.user.family_member
            return Account.objects.filter(member=member)
        except FamilyMember.DoesNotExist:
            return Account.objects.none()

    def perform_create(self, serializer):
        # Assign the account to the current user's family member profile
        try:
            member = self.request.user.family_member
            serializer.save(member=member)
        except FamilyMember.DoesNotExist:
            raise serializers.ValidationError("User is not linked to a FamilyMember profile.")

class TransactionCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows transaction categories to be viewed.
    (Categories are typically managed by an admin).
    """
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transactions to be viewed, added, updated or deleted.
    This handles both income and outcome by creating a Transaction object.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users only see and manage their own transactions
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        try:
            member = self.request.user.family_member
            return Transaction.objects.filter(account__member=member).order_by('-date', '-id')
        except FamilyMember.DoesNotExist:
            return Transaction.objects.none()

    def perform_create(self, serializer):
        # Ensure the account belongs to the current user's family member
        account = serializer.validated_data['account']
        if self.request.user.is_superuser: # Superusers can create transactions for anyone
            pass
        elif account.member != self.request.user.family_member:
            raise serializers.ValidationError("You can only create transactions for your own accounts.")
        serializer.save()

    def perform_update(self, serializer):
        # Ensure user can only update their own transactions
        instance = self.get_object()
        if self.request.user.is_superuser:
            pass
        elif instance.account.member != self.request.user.family_member:
            raise serializers.ValidationError("You can only update your own transactions.")
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure user can only delete their own transactions
        if self.request.user.is_superuser:
            pass
        elif instance.account.member != self.request.user.family_member:
            raise serializers.ValidationError("You can only delete your own transactions.")
        instance.delete()


class BudgetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows budgets to be viewed, added, updated or deleted.
    """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users only see and manage their own budgets
        if self.request.user.is_superuser:
            return Budget.objects.all()
        try:
            member = self.request.user.family_member
            return Budget.objects.filter(member=member)
        except FamilyMember.DoesNotExist:
            return Budget.objects.none()

    def perform_create(self, serializer):
        # If member_id is not provided, default to current user's family member
        if 'member' not in serializer.validated_data:
            try:
                serializer.validated_data['member'] = self.request.user.family_member
            except FamilyMember.DoesNotExist:
                raise serializers.ValidationError("User is not linked to a FamilyMember profile.")
        # Ensure user can only create budgets for themselves unless superuser
        if not self.request.user.is_superuser and serializer.validated_data['member'] != self.request.user.family_member:
            raise serializers.ValidationError("You can only create budgets for yourself.")
        serializer.save()


# --- Custom Report Endpoints ---

# Example 1: Get Current Balance by Kid
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balance_by_kid(request, member_id):
    """
    GET /api/reports/balance_by_kid/{member_id}/
    Returns the current total balance for a specific family member across all their accounts.
    """
    member = get_object_or_404(FamilyMember, pk=member_id)

    # Ensure user can only view their own balance unless superuser
    if not request.user.is_superuser and member.user != request.user:
        return Response(
            {"detail": "You do not have permission to view this member's balance."},
            status=status.HTTP_403_FORBIDDEN
        )

    total_balance = member.accounts.aggregate(Sum('balance_current'))['balance_current__sum']
    total_balance = total_balance if total_balance is not None else 0.00

    return Response({
        "member_id": member.id,
        "member_name": member.name,
        "total_balance": total_balance,
        "currency": "USD" # Assuming a primary currency for total balance, or you might need a more complex aggregation if accounts have different currencies
    })

# Example 2: Get Transaction History by Kid (more robust filtering)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction_history_by_kid(request, member_id):
    """
    GET /api/reports/transaction_history/{member_id}/
    Returns a paginated list of transactions for a specific family member.
    Supports filtering by date range (start_date, end_date), category, and type (credit/debit).
    Usage: /api/reports/transaction_history/1/?start_date=2024-01-01&end_date=2024-12-31&category=1&type=debit
    """
    member = get_object_or_404(FamilyMember, pk=member_id)

    # Ensure user can only view their own history unless superuser
    if not request.user.is_superuser and member.user != request.user:
        return Response(
            {"detail": "You do not have permission to view this member's transaction history."},
            status=status.HTTP_403_FORBIDDEN
        )

    transactions = Transaction.objects.filter(account__member=member).order_by('-date', '-id')

    # Apply filters from query parameters
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    category_id = request.query_params.get('category')
    transaction_type = request.query_params.get('type') # 'credit' or 'debit'

    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)
    if category_id:
        transactions = transactions.filter(category__id=category_id)
    if transaction_type in ['credit', 'debit']:
        transactions = transactions.filter(type=transaction_type)

    # You'll likely want to add pagination here for large datasets
    # from rest_framework.pagination import PageNumberPagination
    # paginator = PageNumberPagination()
    # paginator.page_size = 10 # or a configurable size
    # paginated_transactions = paginator.paginate_queryset(transactions, request)
    # serializer = TransactionSerializer(paginated_transactions, many=True)
    # return paginator.get_paginated_response(serializer.data)

    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


def login_view(request):
    return render(request, 'login/login.html')


# --- New: User Registration View ---
class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Allows anyone to create a new user and automatically links a FamilyMember profile.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # Allow unauthenticated users to register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Optionally, you might want to return the token directly after registration
        # from rest_framework.authtoken.models import Token
        # token = Token.objects.get(user=serializer.instance).key
        # return Response({'message': 'User registered successfully!', 'token': token}, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'message': 'User registered successfully! Please log in.', 'username': serializer.instance.username}, status=status.HTTP_201_CREATED, headers=headers)

def register_view(request):
    return render(request, 'login/register.html')