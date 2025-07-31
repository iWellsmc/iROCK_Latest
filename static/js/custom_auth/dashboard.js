document.addEventListener('DOMContentLoaded', function () {
  // Function to hide elements with the class 'grid-view' on page load
  function hideGridViewOnLoad() {
    var gridViewElements = document.querySelectorAll('.pa');

    gridViewElements.forEach(function (element) {
      element.style.display = 'none'; // Set the display property to 'none' to hide the element
    });
  }

  // Call the function when the DOM is fully loaded
  hideGridViewOnLoad();
});
document.addEventListener("DOMContentLoaded", function () {
  // Get all buttons and corresponding sections
  const buttons = document.querySelectorAll("[data-id]");
  const sections = document.querySelectorAll(".list-view > .col-6 > div");

  // Hide all sections initially using CSS class
  sections.forEach(function (section) {
    section.classList.add("hidden");
  });

  // Add click event listeners to buttons
  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      // Hide all sections using CSS class
      sections.forEach(function (section) {
        section.classList.add("hidden");
      });

      // Get the data-id attribute value of the clicked button
      const dataId = button.getAttribute("data-id");

      // Show the corresponding section based on data-id
      const targetSection = document.querySelector("." + dataId);
      if (targetSection) {
        targetSection.classList.remove("hidden");
      }
    });
  });
});