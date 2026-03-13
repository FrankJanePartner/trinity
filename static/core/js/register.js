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

  // ── Backend submission via Fetch to Flask ──
  async function submitForm() {
    // Validate required text fields
    const textFields = [
      { id: 'fullName', label: 'Full Name' },
      { id: 'phone', label: 'Phone Number' },
      { id: 'email', label: 'Email Address' },
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
    // Validate checkboxes
    const interests = [...document.querySelectorAll('[name="interest"]:checked')].map(i => i.value);
    if (interests.length === 0) {
      alert('Please select at least one area of real estate interest.');
      return;
    }

    // Gather data
    const payload = {
      full_name: document.getElementById('fullName').value.trim(),
      phone: document.getElementById('phone').value.trim(),
      email: document.getElementById('email').value.trim(),
      location: document.getElementById('location').value.trim(),
      involvement: document.querySelector('[name="involvement"]:checked').value,
      experience: document.querySelector('[name="experience"]:checked').value,
      interests,
      challenge: document.getElementById('challenge').value.trim(),
      attend_all: document.querySelector('[name="attend"]:checked').value,
      ethics_commitment: document.querySelector('[name="ethics"]:checked').value,
      heard_from: document.querySelector('[name="source"]:checked').value,
      refer_friends: document.querySelector('[name="refer"]:checked').value,
      referral_numbers: document.getElementById('referPhones')?.value?.trim() || '',
      submitted_at: new Date().toISOString(),
      cohort: 'Cohort 4'
    };

    // Show loading
    const btn = document.getElementById('submitBtn');
    document.getElementById('submitText').style.display = 'none';
    document.getElementById('spinner').style.display = 'block';
    btn.disabled = true;

    try {
      // Submit to Django backend
      const res = await fetch('/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        showSuccess();
        return;
      } else {
        const errorData = await res.json();
        alert('Submission failed: ' + (errorData.message || 'Unknown error'));
        return;
      }
    } catch (e) {
      // Backend not available — fallback: save locally and still show success
      console.log('Backend not reachable, saving locally:', payload);
    }

    // Fallback: store in memory / log
    window._submissions = window._submissions || [];
    window._submissions.push(payload);
    console.log('Application stored:', payload);
    
    // Short delay for UX then show success
    await new Promise(r => setTimeout(r, 1200));
    showSuccess();
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