// script.js

document.addEventListener("DOMContentLoaded", () => {
    // Animate on scroll (simple fade-in and slide-in)
    const animatedElements = document.querySelectorAll(".animate-fadein, .animate-slidein");
  
    const animateOnScroll = () => {
      animatedElements.forEach((el) => {
        const rect = el.getBoundingClientRect();
        if (rect.top <= window.innerHeight - 100) {
          el.classList.add("visible");
        }
      });
    };
  
    animateOnScroll(); // run on page load
    window.addEventListener("scroll", animateOnScroll);
  
    // Toggle password visibility
    const passwordFields = document.querySelectorAll("input[type='password']");
    passwordFields.forEach((field) => {
      const toggleBtn = document.createElement("span");
      toggleBtn.textContent = "👁️";
      toggleBtn.classList.add("toggle-password");
      toggleBtn.style.cursor = "pointer";
      toggleBtn.style.marginLeft = "8px";
      field.parentNode.insertBefore(toggleBtn, field.nextSibling);
  
      toggleBtn.addEventListener("click", () => {
        field.type = field.type === "password" ? "text" : "password";
      });
    });
  });
  