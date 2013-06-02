$('#menu-icon').on('tap', mToggle);

function mToggle() {
	var mState = $('nav ul').css('display');
	console.log(mState);
	if (mState==="none") {
		console.log('toggle display');
		$('nav ul').css({
			display:'block',
		})
	}
	else {
		$('nav ul').css({
			display:'none',
		})
	}
}