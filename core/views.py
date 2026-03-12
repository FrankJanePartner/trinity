from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
from .models import ScholarshipApplication
import json

def index(request):
    return render(request, 'core/index.html')

def register_view(request):
    return render(request, 'account/register.html')

def api_register(request):
    if request.method == 'POST':
        try:
            # Handle both JSON and Form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            full_name = data.get('full_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            city_state = data.get('city_state')
            password = data.get('password')

            # Involvement
            involvement = data.get('involvement')
            # Experience (Checkbox/Radio) - handled as radio in JS but good to have safeguard
            experience = data.getlist('experience') if hasattr(data, 'getlist') else data.get('experience', [])
            if isinstance(experience, str):
                experience = [experience]
            experience_str = ", ".join(experience)

            # Interests (Multiple checkboxes)
            interests = data.getlist('interests') if hasattr(data, 'getlist') else data.get('interests', [])
            if isinstance(interests, str):
                interests = [interests]
            interests_str = ", ".join(interests)

            challenge = data.get('challenge')
            will_attend_all = data.get('will_attend_all') == 'on' or data.get('will_attend_all') is True
            will_follow_ethics = data.get('will_follow_ethics') == 'on' or data.get('will_follow_ethics') is True
            source = data.get('source')
            refer_friends = data.get('refer_friends') == 'on' or data.get('refer_friends') is True
            referral_phones = data.get('referral_phones')

            if not email or not password:
                return JsonResponse({'status': 'error', 'message': 'Email and password are required.'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'A user with this email already exists.'}, status=400)

            # Create User
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name.split(' ')[0] if full_name else '',
                last_name=' '.join(full_name.split(' ')[1:]) if full_name and len(full_name.split(' ')) > 1 else ''
            )

            # Create Scholarship Application
            application = ScholarshipApplication.objects.create(
                user=user,
                full_name=full_name,
                phone_number=phone_number,
                city_state=city_state,
                involvement=involvement,
                experience=experience_str,
                interests=interests_str,
                challenge=challenge,
                will_attend_all=will_attend_all,
                will_follow_ethics=will_follow_ethics,
                source=source,
                refer_friends=refer_friends,
                referral_phones=referral_phones
            )

            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Registration successful!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)