document.addEventListener('DOMContentLoaded', function() {
    // FAQ Accordion functionality
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            // Close all other items
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });
            
            // Toggle current item
            item.classList.toggle('active');
        });
    });

    // Contact form submission
    const contactForm = document.getElementById('contactForm');
    const successModal = document.getElementById('successModal');
    const closeModal = document.querySelector('.close-modal');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Here you would typically send the form data to your server
            // For demonstration, we'll just show the success modal
            
            // Simulate form submission delay
            setTimeout(() => {
                // Reset form
                contactForm.reset();
                
                // Show success modal
                successModal.style.display = 'flex';
            }, 1000);
        });
    }
    
    // Close modal handlers
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            successModal.style.display = 'none';
        });
    }
    
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', () => {
            successModal.style.display = 'none';
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === successModal) {
            successModal.style.display = 'none';
        }
    });

    // Contact option buttons functionality
    const emailBtn = document.getElementById('email-btn');
    const callBtn = document.getElementById('call-btn');
    const chatBtn = document.getElementById('chat-btn');
    
    if (emailBtn) {
        emailBtn.addEventListener('click', () => {
            window.location.href = 'mailto:support@yourcompany.com';
        });
    }
    
    if (callBtn) {
        callBtn.addEventListener('click', () => {
            window.location.href = 'tel:+18001234567';
        });
    }
    
    if (chatBtn) {
        chatBtn.addEventListener('click', () => {
            alert('Live chat would open in a real implementation. This is a demo.');
            // In a real implementation, this would open your chat widget
        });
    }
});