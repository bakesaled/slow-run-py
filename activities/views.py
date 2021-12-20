from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from activities.models import Activity
from activities.serializers import ActivitySerializer, StravaActivitySerializer
from rest_framework.decorators import api_view

from strava_api import StravaApi

# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
def activity_list(request):
    # GET list of activities, POST a new activity, DELETE all activities
    if request.method == 'GET':
        activities = Activity.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            activities = activities.filter(name__icontains=name)

        activities = activities.order_by('-start_date')

        activities_serializer = ActivitySerializer(activities, many=True)
        return JsonResponse({'results': activities_serializer.data}, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        activity_data = JSONParser().parse(request)
        activity_serializer = ActivitySerializer(data=activity_data)
        if activity_serializer.is_valid():
            activity_serializer.save()
            return JsonResponse(activity_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Activity.objects.all().delete()
        return JsonResponse({'message': '{} Activities were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def activity_detail(request, pk):
    # find activity by pk (id)
    try:
        activity = Activity.objects.get(pk=pk)
    except Activity.DoesNotExist:
        return JsonResponse({'message': 'The activity does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET / PUT / DELETE activity
    if request.method == 'GET':
        activity_serializer = ActivitySerializer(activity)
        return JsonResponse(activity_serializer.data)
    elif request.method == 'PUT':
        activity_data = JSONParser().parse(request)
        activity_serializer = ActivitySerializer(activity, data=activity_data)
        if activity_serializer.is_valid():
            activity_serializer.save()
            return JsonResponse(activity_serializer.data)
        return JsonResponse(activity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        activity.delete()
        return JsonResponse({'message': 'Activity was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def activity_sync(request):
    if request.method == 'POST':
        activity_data = StravaApi.sync()

        filtered_activity_data = []
        for activity in activity_data:
            if not Activity.objects.filter(extern_id=activity['id']).exists():
                filtered_activity_data.append(activity)

        print(f'Activities pulled from Strava: {len(activity_data)}')
        print(f'Activities new to us: {len(filtered_activity_data)}')
        if len(filtered_activity_data) == 0:
            return JsonResponse({'message': 'No new activities to sync!'}, status=status.HTTP_200_OK)

        # update?  don't think this works yet.
        for activity in activity_data:
            if Activity.objects.filter(extern_id=activity['id']).exists():
                activity['existing_id'] = Activity.objects.filter(
                    extern_id=activity['id']).first()

        activity_serializer = StravaActivitySerializer(
            data=filtered_activity_data, many=True)
        if activity_serializer.is_valid():
            activity_serializer.save()
            return JsonResponse({'message': 'Activities synced successfully!'}, status=status.HTTP_200_OK)
        return JsonResponse(activity_serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({'message': 'Activities synced successfully!'}, status=status.HTTP_200_OK)
