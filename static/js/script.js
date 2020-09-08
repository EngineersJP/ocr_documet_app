$(window).on('load', function(){
	$('.loading').fadeOut();
});
function loading(){
  $('.loading').fadeIn();
  $('.main-content').fadeOut();       
}