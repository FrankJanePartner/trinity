// ── Form interaction helpers ──
  function selectRadio(el, name) {
    document.querySelectorAll(`[name="${name}"]`).forEach(i => i.closest('.radio-item').classList.remove('selected'));
    el.classList.add('selected');
    el.querySelector('input').checked = true;
  }
  function toggleCheck(el) {
    el.classList.toggle('selected');
    el.querySelector('input').checked = el.classList.contains('selected');
  }
  function showReferField(show) {
    document.getElementById('referNumbers').classList.toggle('show', show);
  }

  // ── Backend submission via Fetch to Django ──
  async function submitForm() {
    // Validate required text fields
    const textFields = [
      { id: 'fullName', label: 'Full Name' },
      { id: 'phone', label: 'Phone Number' },
      { id: 'email', label: 'Email Address' },
      { id: 'password', label: 'Password' },
      { id: 'location', label: 'City / State' },
      { id: 'challenge', label: 'Biggest Challenge' },
    ];
    let valid = true;
    for (const field of textFields) {
      const el = document.getElementById(field.id);
      if (!el.value.trim()) {
        el.classList.add('error'); el.focus();
        el.addEventListener('input', () => el.classList.remove('error'), { once: true });
        alert(`Please fill in: ${field.label}`);
        return;
      }
    }
    // Validate radios
    const radioNames = ['involvement', 'experience', 'attend', 'ethics', 'source', 'refer'];
    for (const name of radioNames) {
      if (!document.querySelector(`[name="${name}"]:checked`)) {
        alert('Please complete all required selections.');
        return;
      }
    }
    // Validate checkboxes (interests)
    const interests = [...document.querySelectorAll('[name="interest"]:checked')].map(i => i.value);
    if (interests.length === 0) {
      alert('Please select at least one area of real estate interest.');
      return;
    }

    // Show loading
    const btn = document.getElementById('submitBtn');
    document.getElementById('submitText').style.display = 'none';
    document.getElementById('spinner').style.display = 'block';
    btn.disabled = true;

    // Gather data using FormData for Django compatibility
    const formData = new FormData();
    formData.append('full_name', document.getElementById('fullName').value.trim());
    formData.append('phone_number', document.getElementById('phone').value.trim());
    formData.append('email', document.getElementById('email').value.trim());
    formData.append('password', document.getElementById('password').value.trim());
    formData.append('city_state', document.getElementById('location').value.trim());
    
    formData.append('involvement', document.querySelector('[name="involvement"]:checked').value);
    formData.append('experience', document.querySelector('[name="experience"]:checked').value);
    
    interests.forEach(val => formData.append('interests', val));
    
    formData.append('challenge', document.getElementById('challenge').value.trim());
    
    if (document.querySelector('[name="attend"]:checked').value === 'yes') {
        formData.append('will_attend_all', 'on');
    }
    if (document.querySelector('[name="ethics"]:checked').value === 'yes') {
        formData.append('will_follow_ethics', 'on');
    }
    
    formData.append('source', document.querySelector('[name="source"]:checked').value);
    
    if (document.querySelector('[name="refer"]:checked').value === 'yes') {
        formData.append('refer_friends', 'on');
    }
    
    formData.append('referral_phones', document.getElementById('referPhones')?.value?.trim() || '');

    try {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const res = await fetch('/api/register/', {
        method: 'POST',
        headers: { 
            'X-CSRFToken': csrfToken
        },
        body: formData
      });
      
      const result = await res.json();
      
      if (res.ok && result.status === 'success') {
        showSuccess();
      } else {
        console.error('Signup failed:', result);
        alert(result.message || 'There was an error with your registration. Please check your details and try again.');
        // Reset button
        document.getElementById('submitText').style.display = 'block';
        document.getElementById('spinner').style.display = 'none';
        btn.disabled = false;
      }
    } catch (e) {
      console.error('Submission error:', e);
      alert('An error occurred. Please try again later.');
      // Reset button
      document.getElementById('submitText').style.display = 'block';
      document.getElementById('spinner').style.display = 'none';
      btn.disabled = false;
    }
  }

  function showSuccess() {
    document.getElementById('successOverlay').classList.add('show');
    document.body.style.overflow = 'hidden';
    // Reset button
    document.getElementById('submitText').style.display = 'block';
    document.getElementById('spinner').style.display = 'none';
    document.getElementById('submitBtn').disabled = false;
  }

  // Close overlay on backdrop click
  document.getElementById('successOverlay').addEventListener('click', function(e) {
    if (e.target === this) {
      this.classList.remove('show');
      document.body.style.overflow = '';
    }
  });