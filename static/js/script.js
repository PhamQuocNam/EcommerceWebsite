// Set current date in the "Last Updated" field
document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Contact button functionality
document.getElementById('contact-btn').addEventListener('click', function() {
    // In a real implementation, this would link to a contact form or open a modal
    alert('Please email us at support@yourcompany.com or call (123) 456-7890');
});

// Accordion functionality for mobile (optional)
const policySections = document.querySelectorAll('.policy-section');
policySections.forEach(section => {
    const heading = section.querySelector('h2');
    const content = section.querySelector('.policy-content');
    
    heading.addEventListener('click', () => {
        content.style.display = content.style.display === 'none' ? 'block' : 'none';
    });
});

// Initialize all content as visible (for mobile toggle)
window.addEventListener('DOMContentLoaded', () => {
    if (window.innerWidth < 768) {
        document.querySelectorAll('.policy-content').forEach(content => {
            content.style.display = 'none';
        });
    }
});