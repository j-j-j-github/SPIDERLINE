document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const status = urlParams.get('status');

    if (status === 'success' || status === 'error') {
        showCustomToast(status);
        // Clean URL
        window.history.replaceState({}, document.title, window.location.pathname);
    }
});

function showCustomToast(type) {
    // Inject CSS for the toast
    if (!document.getElementById('custom-toast-style')) {
        const style = document.createElement('style');
        style.id = 'custom-toast-style';
        style.innerHTML = `
            .custom-toast-container {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 99999;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .custom-toast {
                background-color: #ffffff;
                color: #111111;
                padding: 16px 24px;
                border-radius: 8px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
                display: flex;
                align-items: center;
                gap: 16px;
                font-family: 'Poppins', sans-serif;
                font-weight: 500;
                font-size: 15px;
                transform: translateX(120%);
                opacity: 0;
                transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.4s ease;
                border-left: 5px solid transparent;
            }
            .custom-toast.show {
                transform: translateX(0);
                opacity: 1;
            }
            .custom-toast.success {
                border-left-color: #10b981; /* Emerald Green */
            }
            .custom-toast.error {
                border-left-color: #e31837; /* Primary Red */
            }
            .custom-toast-icon {
                font-size: 20px;
            }
            .custom-toast.success .custom-toast-icon {
                color: #10b981;
            }
            .custom-toast.error .custom-toast-icon {
                color: #e31837;
            }
            .custom-toast-close {
                margin-left: auto;
                cursor: pointer;
                color: #999;
                font-size: 18px;
                transition: color 0.2s;
            }
            .custom-toast-close:hover {
                color: #111;
            }
        `;
        document.head.appendChild(style);
    }

    // Create container if it doesn't exist
    let container = document.querySelector('.custom-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'custom-toast-container';
        document.body.appendChild(container);
    }

    // Create the toast
    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`;
    
    let iconClass = type === 'success' ? 'fa-solid fa-check-circle' : 'fa-solid fa-circle-exclamation';
    let message = type === 'success' ? 'Form submitted successfully! We will get back to you.' : 'There was an error submitting your form.';

    toast.innerHTML = `
        <i class="${iconClass} custom-toast-icon"></i>
        <span>${message}</span>
        <i class="fa-solid fa-xmark custom-toast-close"></i>
    `;

    container.appendChild(toast);

    // Trigger animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 50);

    // Close button functionality
    toast.querySelector('.custom-toast-close').addEventListener('click', () => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    });

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 400);
        }
    }, 5000);
}
