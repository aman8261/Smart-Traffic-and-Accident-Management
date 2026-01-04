document.addEventListener('DOMContentLoaded', function () {
    const emergencyStatus = document.getElementById('emergency-status');
    const accidentStatus = document.getElementById('accident-status');

    // Simulate emergency vehicle detection
    setInterval(() => {
        if (emergencyStatus.textContent === 'No Emergency Vehicle') {
            emergencyStatus.textContent = 'Ambulance Detected';
            emergencyStatus.style.backgroundColor = '#ea4335'; // Red
        } else {
            emergencyStatus.textContent = 'No Emergency Vehicle';
            emergencyStatus.style.backgroundColor = '#4285f4'; // Blue
        }
    }, 5000); // Change status every 5 seconds

    // Simulate accident detection
    setInterval(() => {
        if (accidentStatus.textContent === 'No Accident') {
            accidentStatus.textContent = 'Accident Detected';
        } else {
            accidentStatus.textContent = 'No Accident';
        }
    }, 7000); // Change status every 7 seconds
});