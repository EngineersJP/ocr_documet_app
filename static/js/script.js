$(window).on('load', function(){
	$('.loading').fadeOut();
});
function loading(){
  $('.loading').fadeIn();
  $('.main-content').fadeOut();       
}
$(function() {
  const hum = $('#hamburger, .close')
  const nav = $('.sp-nav')
  hum.on('click', function(){
     nav.toggleClass('toggle');
  });
});