document.addEventListener("DOMContentLoaded", function () {
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
      } else {
          // Allow default behavior for other links (like /roadmap/)
          window.location.href = targetId;
      }
  }
});

function handleMenu(){
  console.log("Clicked");
}