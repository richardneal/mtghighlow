$('a[href*=#]').click(function(){return false;});

var animationEndEvent = "webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend";
var cs = new CardStack();

function CardStack() {
    var wrap = $('#cards');
    var lastcard;

    this.updatevisuals = function (streak, currentcard) {
        if (this.lastcard != null) {
            $('#fakepriceold').html(this.lastcard.fakeprice);
            $('#realpriceold').html(this.lastcard.realprice);
            $('#nameold').html(this.lastcard.cardname);
        }
        if (streak != null) {
            $('#score').html(streak);
        }
        if (currentcard != null) {
            $('#displayprice').html(currentcard.fakeprice);
            this.lastcard = currentcard;
        }
    }

    this.init = function (cards) {
        this.updatevisuals(null, cards[0]);
        for (var i = 0; i < cards.length; i++) {
            wrap.append("<div class='card'><img alt='" + cards[i].cardname + "' src='" + cards[i].image + "' /><span><strong>" + cards[i].cardname + ", " + cards[i].image + "</strong></span></div>");
        }
    }

    this.cycle = function (newcard, streak, currentcard) {
        this.updatevisuals(streak, currentcard);
        wrap.append("<div class='card'><img alt='" + newcard.cardname + "' src='" + newcard.image + "' /><span><strong>" + newcard.cardname + ", " + newcard.image + "</strong></span></div>");
    }
};

var App = {
    yesButton: $('.button.yes .trigger'),
    noButton: $('.button.no .trigger'),
    blocked: false,
    like: function (liked) {
        this.higher = liked;
        var animate = liked ? 'animateYes' : 'animateNo';
        var self = this;
        if(!this.blocked){
            this.blocked = true;
            $('.card').eq(0).addClass(animate).one(animationEndEvent, function(){
                $(this).remove();
                $.getJSON($SCRIPT_ROOT + '/newcard', {
                    higher: self.higher,
                }, function (data) {
                    cs.cycle(data.newcard, data.streak, data.currentcard);
                });
                self.blocked = false;
            });
        }
    }
};

App.yesButton.on('mousedown', function(){
    App.like(true);
});

App.noButton.on('mousedown', function(){
    App.like(false);
});

function initcardstack(cards) {
    var cardsobj = JSON.parse(cards)
    cs.init(cardsobj);
};

$(document).ready(function(){
});
