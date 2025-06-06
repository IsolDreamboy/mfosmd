import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Client

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def consultar_valores_externos(request):
    usuario = request.user

    try:
        client = Client.objects.get(email=usuario.email)
    except Client.DoesNotExist:
        return Response({"erro": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    payload = {
        "cpf": client.cpf,
        "data_nascimento": client.nascimento.strftime('%Y-%m-%d')
    }

    try:
        resposta = requests.post("https://api-java.com/consultar", json=payload, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            return Response({"tem_valores": dados.get("tem_valores", False)})
        else:
            return Response({"erro": "Erro ao consultar a API externa."}, status=resposta.status_code)
    except requests.exceptions.RequestException as e:
        return Response({"erro": f"Erro de conexão: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)
