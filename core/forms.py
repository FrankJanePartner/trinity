from django import forms
from allauth.account.forms import SignupForm
from .models import ScholarshipApplication

class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=255, label='Full Name')
    phone_number = forms.CharField(max_length=20, label='Phone Number')
    city_state = forms.CharField(max_length=255, label='City / State')
    
    involvement = forms.ChoiceField(
        choices=ScholarshipApplication.INVOLVEMENT_CHOICES,
        widget=forms.RadioSelect
    )
    experience = forms.ChoiceField(
        choices=ScholarshipApplication.EXPERIENCE_CHOICES,
        widget=forms.RadioSelect
    )
    
    # Interests as a multiple choice field, but we'll store it as a string
    INTEREST_CHOICES = [
        ('land-sales', 'Land Sales'),
        ('residential-rentals', 'Residential Rentals'),
        ('property-development', 'Property Development'),
        ('property-investment', 'Property Investment'),
        ('property-management', 'Property Management'),
        ('re-marketing', 'Real Estate Marketing'),
        ('other', 'Other'),
    ]
    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    
    challenge = forms.CharField(widget=forms.Textarea)
    
    will_attend_all = forms.BooleanField(required=False)
    will_follow_ethics = forms.BooleanField(required=False)
    
    source = forms.ChoiceField(
        choices=ScholarshipApplication.SOURCE_CHOICES,
        widget=forms.RadioSelect
    )
    
    refer_friends = forms.BooleanField(required=False)
    referral_phones = forms.CharField(widget=forms.Textarea, required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        
        # Save interests as a comma-separated string
        interests_list = self.cleaned_data.get('interests', [])
        interests_str = ', '.join(interests_list)
        
        ScholarshipApplication.objects.create(
            user=user,
            full_name=self.cleaned_data.get('full_name'),
            phone_number=self.cleaned_data.get('phone_number'),
            city_state=self.cleaned_data.get('city_state'),
            involvement=self.cleaned_data.get('involvement'),
            experience=self.cleaned_data.get('experience'),
            interests=interests_str,
            challenge=self.cleaned_data.get('challenge'),
            will_attend_all=self.cleaned_data.get('will_attend_all'),
            will_follow_ethics=self.cleaned_data.get('will_follow_ethics'),
            source=self.cleaned_data.get('source'),
            refer_friends=self.cleaned_data.get('refer_friends'),
            referral_phones=self.cleaned_data.get('referral_phones'),
        )
        return user
