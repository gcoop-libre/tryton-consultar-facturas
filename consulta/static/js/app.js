/**
 * The COPYRIGHT file at the top level of this repository contains
 * the full copyright notices and license terms.
 */
$(window).bind("pageshow", function() {
  $('form').get(0).reset(); //clear form data on page load
});
