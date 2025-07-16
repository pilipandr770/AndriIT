// Основные функции для сайта

// Функция для инициализации всплывающих подсказок Bootstrap
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Функция для инициализации всплывающих окон Bootstrap
function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Функция для обновления количества товаров в корзине
function updateCartQuantity(productId, quantity) {
    fetch('/shop/update_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `product_id=${productId}&quantity=${quantity}`
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Ошибка при обновлении корзины:', error);
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация компонентов Bootstrap
    initTooltips();
    initPopovers();
    
    // Обработчики событий для кнопок изменения количества товаров в корзине
    const quantityInputs = document.querySelectorAll('.cart-quantity-input');
    if (quantityInputs) {
        quantityInputs.forEach(input => {
            input.addEventListener('change', function() {
                const productId = this.dataset.productId;
                const quantity = this.value;
                updateCartQuantity(productId, quantity);
            });
        });
    }
    
    // Текущий год для футера
    const yearElement = document.querySelector('.current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
});