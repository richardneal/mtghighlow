$('a[href*=#]').click(function(){return false;});

var animationEndEvent = "webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend";
var cs = new CardStack();

function CardStack() {
    var wrap = $('#cards');
    var lastcard;

    this.updatevisuals = function (streak, currentcard, beststreak, correct) {
        if (this.lastcard != null) {
            $('#fakepriceold').html('$' + this.lastcard.fakeprice);
            $('#realpriceold').html('$' + this.lastcard.realprice);
            if ((this.lastcard.cardname).length > 17)
                this.lastcard.cardname = (this.lastcard.cardname).substring(0, 17) + '...';
            $('#nameold').html(this.lastcard.cardname);
        }
        if (streak != null) {
            $('#score').html(streak);
            $('#beststreak').html('TOP: ' + beststreak)
        }
        if (currentcard != null) {
            $('#displayprice').html('$' + currentcard.fakeprice);
            this.lastcard = currentcard;
        }
        if (correct != null) {
            if (correct) {
                $('#correct').html('CORRECT');
                $('#correct').removeClass('wrong').addClass('correct')
            } else {
                $('#correct').html('WRONG');
                $('#correct').removeClass('correct').addClass('wrong')
            }
        }
    }

    this.init = function (cards) {
        this.updatevisuals(null, cards[0]);
        for (var i = 0; i < cards.length; i++) {
            wrap.append("<div class='card'><img alt='" + cards[i].cardname + "' src='" + cards[i].image + "' /><span><strong>" + cards[i].cardname + ", " + cards[i].cardset + "</strong></span></div>");
        }
    }

    this.cycle = function (newcard, streak, currentcard, beststreak, correct) {
        this.updatevisuals(streak, currentcard, beststreak, correct);
        wrap.append("<div class='card'><img alt='" + newcard.cardname + "' src='" + newcard.image + "' /><span><strong>" + newcard.cardname + ", " + newcard.cardset + "</strong></span></div>");
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
                    cs.cycle(data.newcard, data.streak, data.currentcard, data.beststreak, data.correct);
                });
                self.blocked = false;
            });
        }
    }
};

App.yesButton.on('click', function(){
    App.like(true);
});

App.noButton.on('click', function(){
    App.like(false);
});

$(document).keydown(function(e) {
    if(e.which == 39){
        App.like(true);
    } else if (e.which == 37){
        App.like(false);
    }
});

function initcardstack(cards) {
    var cardsobj = JSON.parse(cards);
    cs.init(cardsobj);
};

$(document).ready(function(){
});
