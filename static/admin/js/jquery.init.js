/*global jQuery:false*/
'use strict';
/* Puts the included jQuery into our own namespace using noConflict and passing
 * it 'true'. This ensures that the included jQuery doesn't pollute the global
 * namespace (i.e. this preserves pre-existing values for both window.$ and
 * window.jQuery).
 */

// Verifica se jQuery já está definido antes de tentar usá-lo
if (typeof jQuery !== 'undefined') {
  window.django = {jQuery: jQuery.noConflict(true)};
} else {
  // Carrega jQuery se não estiver disponível
  document.write('<script src="/static/admin/js/vendor/jquery/jquery.js"></script>');
  // Tenta novamente após o carregamento
  window.addEventListener('load', function() {
    if (typeof jQuery !== 'undefined') {
      window.django = {jQuery: jQuery.noConflict(true)};
    }
  });
}
