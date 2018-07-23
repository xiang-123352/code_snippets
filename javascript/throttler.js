(function() {

'use strict';

// throttled value before window event starts
var throttled;

// Delay function calls to 66ms (frame rate: 15fps)
var delay = 66;

// Declare empty variable for later use
var resizeTimeout;

// Grab body element
var body = document.querySelector('body');

// Create element
var viewportDimensions = document.createElement('div');

// Style element
viewportDimensions.style.position = 'fixed';
viewportDimensions.style.right = 0;
viewportDimensions.style.top = 0;
viewportDimensions.style.padding = '16px';
viewportDimensions.style.zIndex = 3;
viewportDimensions.style.fontSize = '22px';

// Add div element inside body element
body.appendChild(viewportDimensions);

// window.resize callback function
function getViewportDimensions() {

  var width = window.innerWidth;
  var height = window.innerHeight;

  viewportDimensions.textContent = width + 'px' + ' x ' + height + 'px';
  viewportDimensions.style.display = 'block';

  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(removeViewportDimensions, 3000);
}

// Called from getViewportDimensions()
function removeViewportDimensions() {
  viewportDimensions.style.display = 'none';
}

function throttler() {
  // Only run code if’s block if we’re not throttled
  if (!throttled) {
    // Callback: the function we want to throttle
    getViewportDimensions();
    // We're currently throttled!
    throttled = true;
    // Reset throttled variable back to false after delay
    setTimeout(function() {
    throttled = false;
    }, delay);
  }
}

// Listen to resize event, and run throttler()
window.addEventListener('resize', throttler);

// End of IFFE wrapper
})();
