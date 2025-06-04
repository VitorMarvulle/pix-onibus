function showNotification(message, type = 'info') {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        ${message}
        <span class="notification-close">&times;</span>
    `;

    container.appendChild(notification);

    // Add close button functionality
    const closeButton = notification.querySelector('.notification-close');
    closeButton.addEventListener('click', () => {
        notification.style.animation = 'fadeOut 0.5s ease-in-out forwards';
        setTimeout(() => {
            notification.remove();
        }, 500);
    });

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'fadeOut 0.5s ease-in-out forwards';
            setTimeout(() => {
                notification.remove();
            }, 500);
        }
    }, 5000);
}