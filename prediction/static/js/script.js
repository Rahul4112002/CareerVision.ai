

// First, let's update the JavaScript to ensure it works properly
document.addEventListener("DOMContentLoaded", function () {
    // Define handleMenu function first - make it globally available
    window.handleMenu = function() {
      var nav = document.querySelector('nav');
      
      if (nav.classList.contains('hidden')) {
        // Show the menu
        nav.classList.remove('hidden');
        nav.classList.add('flex', 'flex-col', 'absolute', 'top-full', 'left-0', 'right-0', 'bg-white', 'p-4', 'shadow-md', 'border-t', 'border-gray-200', 'z-50');
        
        // Adjust the spacing between nav items for mobile view
        var navLinks = document.querySelectorAll('.nav-link');
        for (var i = 0; i < navLinks.length; i++) {
          navLinks[i].classList.add('py-2');
        }
      } else {
        // Hide the menu
        nav.classList.add('hidden');
        nav.classList.remove('flex', 'flex-col', 'absolute', 'top-full', 'left-0', 'right-0', 'bg-white', 'p-4', 'shadow-md', 'border-t', 'border-gray-200', 'z-50');
      }
    };
    
    // Add direct event listener to menu button instead of relying on onclick attribute
    var menuButton = document.querySelector('button[type="button"]');
    if (menuButton) {
      menuButton.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent document click from immediately closing the menu
        handleMenu();
      });
    }
  
    // Your existing smooth scroll functionality
    var scrollLinks = document.querySelectorAll(".nav-link");
    for (var i = 0; i < scrollLinks.length; i++) {
      scrollLinks[i].addEventListener("click", smoothScroll);
    }
  
    function smoothScroll(event) {
      var targetId = this.getAttribute("href");
  
      // Check if the target is a hash link
      if (targetId.startsWith('#')) {
        event.preventDefault(); // Prevent default only for hash links
        var targetPosition = document.querySelector(targetId).offsetTop;
        window.scrollTo({
          top: targetPosition,
          behavior: "smooth",
        });
        
        // Close mobile menu after clicking a link (if mobile view)
        if (window.innerWidth < 1024) {
          var nav = document.querySelector('nav');
          if (!nav.classList.contains('hidden')) {
            handleMenu();
          }
        }
      }
    }
    
    // Close the menu when clicking outside
    document.addEventListener('click', function(event) {
      var nav = document.querySelector('nav');
      var menuButton = document.querySelector('button[type="button"]');
      
      if (!nav.contains(event.target) && !menuButton.contains(event.target) && !nav.classList.contains('hidden') && window.innerWidth < 1024) {
        handleMenu();
      }
    });
    
    // Handle resize events
    window.addEventListener('resize', function() {
      var nav = document.querySelector('nav');
      
      if (window.innerWidth >= 1024) {
        nav.classList.remove('flex-col', 'absolute', 'top-full', 'left-0', 'right-0', 'bg-white', 'p-4', 'shadow-md', 'border-t', 'border-gray-200');
        nav.classList.add('flex', 'gap-12');
        
        var navLinks = document.querySelectorAll('.nav-link');
        for (var i = 0; i < navLinks.length; i++) {
          navLinks[i].classList.remove('py-2');
        }
      } else if (!nav.classList.contains('hidden') && !nav.classList.contains('flex-col')) {
        nav.classList.add('hidden');
      }
    });
  });