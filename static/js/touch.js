var el = document.getElementById('menu-icon'),
    myTap = new Tap(el);

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

el.addEventListener('tap', mToggle, false);


// temperature dashboard toggle
var tempnum = document.getElementById('tempnum'),
    temp = new Tap(tempnum);

function tempToggle() {
	console.log($('#hum-img').css('display'));
	var tempState = $('#hum-img').css('display');
	
	if (tempState !== "none") {
		
		$('#hum-img').css({
			display:'none',
		});
		$('#worm_background').css( {
			display:'block',
		});
		$('#worm-container').css( {
			display:'block',
		});
		$('#temp-img').css( {
			display:'none',
		});
	}
	
	else {

		$('#hum-img').css( {
			display:'block',
		});
		$('#worm_background').css( {
			display:'none',
		});
		$('#worm-container').css( {
			display:'none',
		});
		$('#temp-img').css( {
			display:'none',
		});

	}
}

// tempnum.addEventListener('tap', tempToggle, false);


// humidity dashboard toggle
var humnum = document.getElementById('humnum'),
    hum = new Tap(humnum);

function humToggle() {
	console.log('toggle-hum');
}

// humnum.addEventListener('tap', humToggle, false);