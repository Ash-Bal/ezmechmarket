
var slideIndex = 1;
showSlides(slideIndex, album);

// Next/previous controls
function plusSlides(n, album) {
  showSlides(slideIndex += n, album);
}

// Thumbnail image controls
function currentSlide(n, album) {
  showSlides(slideIndex = n, album);
}

function showSlides(n, album) {
  var i;
  var slides = document.getElementsByClassName(album);
//   var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
//   for (i = 0; i < dots.length; i++) {
//       dots[i].className = dots[i].className.replace(" active", "");
//   }
  slides[slideIndex-1].style.display = "block";
//   dots[slideIndex-1].className += " active";
} 
