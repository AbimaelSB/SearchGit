from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
import requests
import json

from core.serializers import RepositorySerializer
from core.models import Repository

class RepositoryViewSet(viewsets.ViewSet):
  serializer_class = RepositorySerializer
  permission_classes = [permissions.IsAuthenticated]
  
  def list(self, request):
    queryset = Repository.objects.all()
    serializer = RepositorySerializer(queryset, many=True)
    return Response(serializer.data)

  def create(self, request, *args, **kwargs):
    queryset = Repository.objects.all()
    queryset.delete()
    repositorio_data = request.data
    busca = repositorio_data["repositorio"]
    if busca:
      link_api = 'https://api.github.com/search/repositories?q=' + busca
      resultados = requests.get(link_api)
      repositorio_dict = json.loads(resultados.content)
      if repositorio_dict['total_count'] > 0:
        pages = repositorio_dict['total_count'] // 30
        resto = repositorio_dict['total_count'] % 30
        if resto > 0:
          pages += 1
        for i in range(1, pages+1):
          link_per_page = link_api + '&page=' + str(i)
          search_results = requests.get(link_per_page)
          search_dict = json.loads(search_results.content)
          for i in range(len(search_dict['items'])):
            repo = Repository.objects.create(repositorio = search_dict['items'][i]['full_name'])
            repo.save()
            serializer = RepositorySerializer(repo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
        return Response({"Aviso": "Nenhum resultado encontrado"})
    else:
      return Response({"Aviso": "Campo Vazio"})
