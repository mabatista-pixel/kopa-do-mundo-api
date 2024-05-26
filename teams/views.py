from django.shortcuts import render
from rest_framework.views import APIView, status, Response, Request
from django.forms.models import model_to_dict
from teams.models import Team
from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError 
from utils import data_processing


class TeamsView(APIView):
    def post(self, request):
        try:
            selection_data = request.data

            validation_message = data_processing(selection_data)

            if validation_message:
                team = Team.objects.create(**request.data)
                team_dict = model_to_dict(team)
            
            return Response(team_dict, status=201)

        except NegativeTitlesError:

            return Response({"error": "titles cannot be negative"}, status=400)
        
        except ImpossibleTitlesError:

            return Response({"error": "impossible to have more titles than disputed cups"}, status=400)
        
        except InvalidYearCupError:

            return Response({"error": "there was no world cup this year"}, status=400)
  
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    def get(self, request): 
        teams = Team.objects.all()
        teams_dict = [model_to_dict(team) for team in teams]
        return Response(teams_dict, status=200)
        

class TeamsDetailView(APIView):
    def get(self, request, team_id: int):
        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status=404)
        
        team_dict = model_to_dict(team)
        return Response(team_dict)
             
    def patch(self, request, team_id: int):
        if team_id:
            try:
                team = Team.objects.get(pk=team_id)
                for key, value in request.data.items():
                    setattr(team, key, value)
                team.save()
                return Response(model_to_dict(team), status=200)
            except Team.DoesNotExist:
                return Response({"message": "Team not found"}, status=404)
        else:
            return Response({"error": "Missing team ID"}, status=400)
    
    def delete(self, request, team_id: int):
        if team_id:
            try:
                team = Team.objects.get(pk=team_id)
                team.delete()
                return Response(status=204)
            except Team.DoesNotExist:
                return Response({"message": "Team not found"}, status=404)
        else:
            return Response({"error": "Missing team ID"}, status=400)
        
