Element.addMethods({
  viewable: function(el) {
    // INIT
    el = $(el);
    var scroll = document.viewport.getScrollOffsets();
    var viewport = document.viewport.getDimensions();
    var offsets = el.cumulativeOffset();
    var dimensions = el.getDimensions();
    
    // Sanity check
    if (el.getStyle('display') == 'none' || el.getStyle('visibility') == 'hidden') return 0;
    
    // Fix offsets based on scroll
    offsets.top = offsets.top - scroll.top;
    offsets.left = offsets.left - scroll.left;
    
    // Build visible dimensions
    var visible_dimensions = {width: dimensions.width, height: dimensions.height};
    
    // Top
    if (offsets.top < 0) {
      if (Math.abs(offsets.top) > dimensions.height) return 0; // Sanity check
      else {
        visible_dimensions.height -= Math.abs(offsets.top);
      }
    }
    
    // Left
    if (offsets.left < 0) {
      if (Math.abs(offsets.left) > dimensions.width) return 0; // Sanity check
      else {
        visible_dimensions.width -= Math.abs(offsets.left);
      }
    }
    
    // Bottom
    var bottomPos = offsets.top + dimensions.height;
    if (bottomPos > viewport.height) {
      var diff = bottomPos - viewport.height;
      if (diff > dimensions.height) return 0; // Sanity check
      else {
        visible_dimensions.height -= diff;
      }
    }
    
    // Right
    var rightPos = offsets.left + dimensions.width;
    if (rightPos > viewport.width) {
      var diff = rightPos - viewport.width;
      if (diff > dimensions.width) return 0; // Sanity check
      else {
        visible_dimensions.width -= diff;
      }
    }
    
    // Return
    return (visible_dimensions.width * visible_dimensions.height) / (dimensions.width * dimensions.height);
  }
});
