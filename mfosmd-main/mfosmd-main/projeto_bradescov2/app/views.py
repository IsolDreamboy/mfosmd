from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .jwt_auth import CustomTokenObtainPairSerializer

# Endpoint de registro
class RegistroView(APIView):
    def post(self, request):
        print("DADOS RECEBIDOS:", request.data)
        data = request.data.copy()
        data['senha'] = make_password(data['senha'])  # Criptografa a senha
        serializer = ClientSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'mensagem': 'Usuário registrado com sucesso!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint de login
class LoginView(APIView):
    def post(self, request):
        cpf = request.data.get('cpf')
        senha = request.data.get('senha')

        try:
            client = Client.objects.get(cpf=cpf)
            if check_password(senha, client.senha):
                return Response({'mensagem': 'Login realizado com sucesso!'})
            else:
                return Response({'erro': 'Senha incorreta'}, status=status.HTTP_401_UNAUTHORIZED)
        except Client.DoesNotExist:
            return Response({'erro': 'CPF não encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Endpoint alyson
class ValoresReceberView(APIView):
    def post(self, request):
        cpf = request.data.get('cpf')
        nascimento = request.data.get('nascimento')

        if cpf and nascimento:
            return Response({'valores': 'R$ 123,45'})  # simulação
        else:
            return Response({'erro': 'Dados insuficientes'}, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MeuValorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        client = Client.objects.get(email=user.email)
        return Response({
            'nome': client.nome,
            'valor_a_receber': client.valor_a_receber
        })

