from django.db import models

class ScholarshipApplication(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    city_state = models.CharField(max_length=255)
    
    INVOLVEMENT_CHOICES = [
        ('full-time', 'Yes — Full-time realtor'),
        ('part-time', 'Yes — Part-time realtor'),
        ('interested', 'Not yet, but interested'),
        ('investor', 'Property investor'),
        ('other', 'Other'),
    ]
    involvement = models.CharField(max_length=20, choices=INVOLVEMENT_CHOICES)
    
    EXPERIENCE_CHOICES = [
        ('none', 'None'),
        ('<1yr', 'Less than 1 year'),
        ('1-3yr', '1–3 years'),
        ('4-7yr', '4–7 years'),
        ('8+yr', '8+ years'),
    ]
    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES)
    
    # Interests will be stored as a comma-separated string.
    interests = models.TextField(help_text="Comma-separated interests")
    
    challenge = models.TextField()
    
    will_attend_all = models.BooleanField(default=False)
    will_follow_ethics = models.BooleanField(default=False)
    
    SOURCE_CHOICES = [
        ('instagram', 'Instagram'),
        ('whatsapp', 'WhatsApp'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('trinity-community', 'Trinity Community'),
        ('rurblist', 'Rurblist'),
        ('friend-referral', 'Friend Referral'),
        ('other', 'Other'),
    ]
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    
    refer_friends = models.BooleanField(default=False)
    referral_phones = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application from {self.full_name}"
