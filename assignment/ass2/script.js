document.addEventListener('DOMContentLoaded', function() {
    // Variables
    let isDragging = false;
    let rotationSpeed = 0;
    let rotation = 0;
    const image = document.getElementById('currentImage');
    const friction = 0.97;

    // Navbar smooth scrolling
    document.querySelectorAll('#navbar a:not(.cv-item a)').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    document.getElementById("backToTopRight").addEventListener("click", scrollToTop);    

    window.onload = function() {
        if (window.innerWidth <= 600) {
            document.getElementById('mobileAlert').style.display = 'block';
        }
    }

    // Project details toggle
    const toggleIcons = document.querySelectorAll('.toggle-icon');
    toggleIcons.forEach(icon => {
        const detail = icon.nextElementSibling.nextElementSibling; 
        detail.classList.remove('open'); // 기본 상태를 닫힌 상태로 설정
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');

        icon.addEventListener('click', function () {
            detail.classList.toggle('open');
            icon.classList.toggle('fa-chevron-down');
            icon.classList.toggle('fa-chevron-up');
        });
    });

    
    // Image link popup
    const imageLinks = document.querySelectorAll('.image-link');
    imageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            window.open(link.href, 'ImagePopup', 'width=600,height=600');
        });
    });
});




