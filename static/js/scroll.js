// js/scroll.js

// Get the button element
const scrollToTopBtn = document.getElementById("scrollToTopBtn");

// Function to handle the scroll event
function scrollFunction() {
  // Show the button if the user scrolls down 20px from the top
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    scrollToTopBtn.classList.add("show");
  } else {
    scrollToTopBtn.classList.remove("show");
  }
}

// Function to scroll to the top of the document
function topFunction() {
  // Use smooth scrolling for a better user experience
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
}

// Add event listener for the scroll event on the window
window.onscroll = function() {
  scrollFunction();
};

// Add event listener for the button click
scrollToTopBtn.addEventListener("click", topFunction);