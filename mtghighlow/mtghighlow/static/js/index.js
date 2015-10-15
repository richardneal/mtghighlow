$('a[href*=#]').click(function(){return false;});

var animationEndEvent = "webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend";
var cs = new CardStack();

function CardStack() {
    var wrap = $('#cards');
    var q = new Queue();
    var currentcard;

    this.updatevisuals = function (newcard, lastcard, streak) {
        $('#displayprice').html(newcard.fakeprice);
        if (lastcard != null) {
            $('#fakepriceold').html(lastcard.fakeprice);
            $('#realpriceold').html(lastcard.realprice);
            $('#nameold').html(lastcard.cardname);
        }
        if (streak != null) {
            $('#streak').html(streak);
        }
    }

    this.init = function (cards) {
        this.updatevisuals(cards[0], null, null);
        this.currentcard = cards[0];
        for (var i = 0; i < cards.length; i++) {
            q.enqueue(cards[i]);
            wrap.append("<div class='card'><img alt='" + cards[i].cardname + "' src='" + cards[i].image + "' /><span><strong>" + cards[i].cardname + ", " + cards[i].image + "</strong></span></div>");
        }
        q.dequeue();
    }

    this.cycle = function (newcard, streak) {
        lastcard = this.currentcard;
        this.currentcard = q.dequeue();
        this.updatevisuals(this.currentcard, lastcard, streak);
        wrap.append("<div class='card'><img alt='" + newcard.cardname + "' src='" + newcard.image + "' /><span><strong>" + newcard.cardname + ", " + newcard.image + "</strong></span></div>");
        q.enqueue(newcard)
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
                    currentcard: cs.currentcard
                }, function (data) {
                    cs.cycle(data.newcard, data.streak);
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
