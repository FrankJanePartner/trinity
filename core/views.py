from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ScholarshipApplication
import json

def index(request):
    return render(request, 'core/index.html')

def register_view(request):
    return render(request, 'account/register.html')

def api_register(request):
    if request.method == 'POST':
        print("POST received")
        try:
            # Handle both JSON and Form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                print("JSON data:", data)
            else:
                data = request.POST
                print("Form data:", data)

            full_name = data.get('full_name')
            email = data.get('email')
            phone_number = data.get('phone')
            city_state = data.get('location')
            involvement = data.get('involvement')
            experience = data.get('experience')
            interests = data.get('interests', [])
            if isinstance(interests, list):
                interests_str = ", ".join(interests)
            else:
                interests_str = interests
            challenge = data.get('challenge')
            will_attend_all = data.get('attend_all') == 'yes'
            will_follow_ethics = data.get('ethics_commitment') == 'yes'
            source = data.get('heard_from')
            refer_friends = data.get('refer_friends') == 'yes'
            referral_phones = data.get('referral_numbers')

            print("Parsed data:", full_name, email, phone_number, city_state, involvement, experience, interests_str, challenge, will_attend_all, will_follow_ethics, source, refer_friends, referral_phones)

            # Validate required fields
            required_fields = [full_name, email, phone_number, city_state, involvement, experience, challenge, source]
            if not all(required_fields):
                print("Validation failed")
                return JsonResponse({'status': 'error', 'message': 'All required fields must be filled.'}, status=400)

            if ScholarshipApplication.objects.filter(email=email).exists():
                print("Email exists")
                return JsonResponse({'status': 'error', 'message': 'An application with this email already exists.'}, status=400)

            # Create Scholarship Application
            application = ScholarshipApplication.objects.create(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                city_state=city_state,
                involvement=involvement,
                experience=experience,
                interests=interests_str,
                challenge=challenge,
                will_attend_all=will_attend_all,
                will_follow_ethics=will_follow_ethics,
                source=source,
                refer_friends=refer_friends,
                referral_phones=referral_phones
            )
            print("Application created:", application.id)
            return JsonResponse({'status': 'success', 'message': 'Application submitted successfully!'})

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)