from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Category, Transaction, Wallet
from .serializers import UserSerializerWithToken, UserSerializer, CategorySerializer, TransactionSerializer, \
    WalletSerializer
from django.db.models import Q
from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Sum


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def latest_first(self, request):
        limit = request.query_params.get('limit', None)
        queryset = self.get_queryset().order_by('-date')
        if limit:
            queryset = queryset[:int(limit)]
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def oldest_first(self, request):
        transactions = self.get_queryset().order_by('date')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query')
        transactions = self.get_queryset().filter(
            Q(description__icontains=query) | Q(category__name__icontains=query) | Q(
                wallet__name__icontains=query))
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        transactions = self.get_queryset().filter(date__range=[start_date, end_date])
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_amount_range(self, request):
        min_amount = request.query_params.get('min_amount', None)
        max_amount = request.query_params.get('max_amount', None)
        transactions = self.get_queryset().filter(amount__range=[min_amount, max_amount])
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category_id')
        transactions = self.get_queryset().filter(category_id=category_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_wallet(self, request):
        wallet_id = request.query_params.get('wallet_id')
        transactions = self.get_queryset().filter(wallet_id=wallet_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data

    print("data", data)

    try:
        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=make_password(data['password']),
        )

        serializer = UserSerializerWithToken(user, many=False)

        return Response(serializer.data)

    except:
        message = {'detail': 'An Unknown error occurred during registration'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    user_wallets = Wallet.objects.filter(user=user)
    wallets_serializer = WalletSerializer(user_wallets, many=True)
    serializer = UserSerializer(user, many=False)
    return Response({'user': serializer.data, 'wallets': wallets_serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    data = request.POST
    print("data", data)
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.save()
    serializer = UserSerializerWithToken(user, many=False)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    data = request.data
    print("data", data)
    category = Category.objects.create(
        name=data['name'],
    )

    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    user = request.user
    data = request.data
    print("data", data)
    transaction = Transaction.objects.create(
        user=user,
        category=Category.objects.get(id=data['category_id']),
        wallet=Wallet.objects.get(id=data['wallet_id']),
        amount=Decimal(data['amount']),
        transaction_type=data['transaction_type'],
        receipt=request.FILES.get('receipt'),
        date=data['date'],
        note=data['note']
    )

    serializer = TransactionSerializer(transaction, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_grouped_transactions(request):
    today = date.today()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)

    transactions_today = Transaction.objects.filter(date__gte=today)
    transactions_yesterday = Transaction.objects.filter(date__gte=yesterday, date__lt=today)
    transactions_last_week = Transaction.objects.filter(date__gte=last_week, date__lt=yesterday)

    grouped_transactions = {
        'Today': TransactionSerializer(transactions_today, many=True).data,
        'Yesterday': TransactionSerializer(transactions_yesterday, many=True).data,
        'Last Week': TransactionSerializer(transactions_last_week, many=True).data,
    }

    return Response(grouped_transactions)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wallets(request):
    wallets = Wallet.objects.all()
    serializer = WalletSerializer(wallets, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_wallet(request):
    user = request.user
    data = request.data
    print("data", data)
    wallet = Wallet.objects.create(
        user=user,
        name=data['name'],
        balance=data['balance']
    )

    serializer = WalletSerializer(wallet, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stats(request):
    # Calculate total expenses
    total_expenses = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum']
    # Calculate total income
    total_income = Transaction.objects.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum']
    # Calculate total balance
    total_balance = Wallet.objects.filter(user=request.user).aggregate(Sum('balance'))['balance__sum']

    # Calculate total expenses for last 7 days
    today = date.today()
    last_week = today - timedelta(days=7)
    total_expenses_last_week = \
    Transaction.objects.filter(transaction_type='expense', date__gte=last_week).aggregate(Sum('amount'))['amount__sum']

    data = {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'total_balance': total_balance,
        'total_expenses_last_week': total_expenses_last_week
    }

    return Response(data)
