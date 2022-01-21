from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from activities.models import Activity
from activities.serializers import ActivitySerializer, StravaActivitySerializer
from rest_framework.decorators import api_view

from strava_api import StravaApi
from threading import Thread

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


@api_view(['POST'])
def register_webhook(request):
    if request.method == 'POST':
        res = StravaApi.register_webhook()
        return JsonResponse({'message': 'Webhook registered successfully!'}, status=status.HTTP_200_OK)


# strava webhook only
def save_activity_from_strava(json_body):
    if json_body['object_type'] != 'activity':
        return

    activity_id = json_body['object_id']
    existing_activity = Activity.objects.get(extern_id=activity_id)
    if json_body['aspect_type'] == 'create':
        if existing_activity:
            print(
                f'activity already exists, bailout from create {activity_id}')
            return

        # This is a new activity
        strava_api_client = StravaApi()
        activity_data = strava_api_client.get_activity(activity_id)
        print(f'saving new activity {activity_data}')
        activity_serializer = StravaActivitySerializer(data=activity_data)
        if activity_serializer.is_valid():
            activity_serializer.save()
            print(f'activity saved')
    elif json_body['aspect_type'] == 'delete':
        if existing_activity:
            print(f'deleting activity {activity_id}')
            existing_activity.delete()
            print(f'activity deleted')

    elif json_body['aspect_type'] == 'update':
        if not existing_activity:
            print(
                f'activity does not exist, bailout from update {activity_id}')
            return
        print(f'updating activity {activity_id}')
        strava_api_client = StravaApi()
        activity_data = strava_api_client.get_activity(activity_id)

        # Need to get local activity and apply changes from strava.
        # Can this be done with the serializer?
        activity_data.existing_id = existing_activity.id
        activity_serializer = StravaActivitySerializer(data=activity_data)
        if activity_serializer.is_valid():
            activity_serializer.save()
            print(f'activity saved')


@api_view(['GET', 'POST'])
def receive_webhook(request):
    if request.method == 'GET':
        # """Response Strava Webhook API Challenge"""
        mode = request.GET.get('hub.mode', None)
        token = request.GET.get('hub.verify_token', None)
        challenge = request.GET.get('hub.challenge', None)

        print(
            f"Received verify request. mode {mode}, token {token}")

        if mode == 'subscribe' and token == 'STRAVA':
            print(
                f"Received verify request. Responding with {challenge}")
            return JsonResponse({"hub.challenge": challenge})
        return JsonResponse({'message': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'POST':
        # """Receive Strava Webhook Notifications"""
        json_body = JSONParser().parse(request)

        print(f'Received Strava Push Notification: {json_body}')
        # Complete Async so Strava Webhook Response is Instant
        thread = Thread(target=save_activity_from_strava(json_body))
        thread.start()

        return JsonResponse({'message': 'event received!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def webhooks(request):
    if request.method == 'GET':
        res = StravaApi.view_webhook_subscriptions()
        return JsonResponse(res, safe=False)


@api_view(['DELETE'])
def webhook(request, pk):
    if request.method == 'DELETE':
        StravaApi.delete_webhook_subscription(pk)
        return JsonResponse({'message': 'Activity was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
