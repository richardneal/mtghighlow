$('a[href*=#]').click(function(){return false;});

var animationEndEvent = "webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend";

var Person = {
	wrap: $('#people'),
	people: [ 
		{name: 'Stone Rain', set: 'SET', img: "http://magiccards.info/scans/en/fnmp/10.jpg"},
	],
	add: function(){
		var random = this.people[Math.floor(Math.random() * this.people.length)];
		this.wrap.append("<div class='person'><img alt='" + random.name + "' src='" + random.img + "' /><span><strong>" + random.name + ", " + random.set + "</strong></span></div>");
	}
};

var App = {
	yesButton: $('.button.yes .trigger'),
	noButton: $('.button.no .trigger'),
	blocked: false,
	like: function(liked){
		var animate = liked ? 'animateYes' : 'animateNo';
		var self = this;
		if(!this.blocked){
		  this.blocked = true;
		  	$('.person').eq(0).addClass(animate).one(animationEndEvent, function(){
	   			$(this).remove();
				Person.add();
				self.blocked = false;
			});
		}
	}
};

var Phone = {
	wrap: $('#phone'),
	clock: $('.clock'),
	updateClock: function(){
		var date = new Date();
		var hours = date.getHours();
		var min = date.getMinutes();
     hours = (hours < 10 ? "0" : "") + hours;
		min = (min < 10 ? "0" : "") + min;
		var str = hours + ":" + min;
		this.clock.text(str);
	}
}
  
App.yesButton.on('mousedown', function(){
	App.like(true);
});

App.noButton.on('mousedown', function(){
	App.like(false);
});

$(document).ready(function(){
  Phone.updateClock(); 
  setInterval('Phone.updateClock()', 1000);
  Person.add();
  Person.add();
});