$('a[href*=#]').click(function(){return false;});

var animationEndEvent = "webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend";
var cs = new CardStack();

function CardStack() {
    var wrap = $('#cards');
    var lastcard;

    this.updatevisuals = function (streak, currentcard, beststreak, result) {
        if (this.lastcard != null) {
            $('#fakepriceold').html('$' + formatNumber(this.lastcard.fakeprice));
            $('#realpriceold').html('$' + formatNumber(this.lastcard.realprice));
            if ((this.lastcard.cardname).length > 17)
                this.lastcard.cardname = (this.lastcard.cardname).substring(0, 17) + '...';
            $('#nameold').html(this.lastcard.cardname);
        }
        if (streak != null) {
            $('#score').html(streak);
        }
        if (beststreak != null) {
            $('#beststreak').html('TOP: ' + beststreak)
        }
        if (currentcard != null) {
            $('#displayprice').html('$' + formatNumber(currentcard.fakeprice));
            $('#cardname').html(currentcard.cardname)
            $('#setname').html(currentcard.cardsetfull)
            $('#rarity').html(currentcard.rarity)
            this.lastcard = currentcard;
        }
        if (result != null) {
            if (result == 'correct') {
                $('#correct').html('CORRECT');
                $('#correct').removeClass('wrong').removeClass('lucky').addClass('correct')
            } else if (result == 'wrong') {
                $('#correct').html('WRONG');
                $('#correct').removeClass('correct').removeClass('lucky').addClass('wrong')
            } else if (result == 'lucky') {
                $('#correct').html('LUCKY')
                $('#correct').removeClass('wrong').removeClass('correct').addClass('lucky')
            } else if (result == 'notlucky') {
                $('#correct').html('NOT LUCKY')
                $('#correct').removeClass('correct').removeClass('lucky').addClass('wrong')
            } else if (result == 'tricked') {
                $('#correct').html('TRICKED')
                $('#correct').removeClass('wrong').removeClass('correct').addClass('lucky')
            } else if (result == 'error') {
                $('#correct').html('ERROR')
                $('#correct').removeClass('correct').removeClass('wrong').removeClass('lucky')
            }
        }
    }

    this.init = function (cards) {
        this.updatevisuals(null, cards[0]);
        for (var i = 0; i < cards.length; i++) {
            wrap.append("<div class='magiccard'><img alt='" + cards[i].cardname + "' src='" + cards[i].image + "' /></div>");
        }
    }

    this.cycle = function (newcard, streak, currentcard, beststreak, correct) {
        this.updatevisuals(streak, currentcard, beststreak, correct);
        wrap.append("<div class='magiccard'><img alt='" + newcard.cardname + "' src='" + newcard.image + "' /></div>");
    }
};

var App = {
    yesButton: $('#higher'),
    noButton: $('#lower'),
    luckyButton: $('#displayprice'),
    blocked: false,
    like: function (liked) {
        this.choice = liked;
        var animate = null
        if (liked == 'higher') {
            animate = 'animateYes';
        } else if (liked == 'lower') {
            animate = 'animateNo';
        } else if (liked = 'lucky') {
            animate = 'animateLucky'
        }
        var self = this;
        if(!this.blocked){
            this.blocked = true;
            $('.magiccard').eq(0).addClass(animate).one(animationEndEvent, function(){
                $(this).remove();
                $.getJSON($SCRIPT_ROOT + '/newcard', {
                    choice: self.choice,
                }, function (data) {
                    cs.cycle(data.newcard, data.streak, data.currentcard, data.beststreak, data.correct);
                });
                self.blocked = false;
            });
        }
    }
};

App.yesButton.on('click', function(){
    App.like('higher');
});

App.noButton.on('click', function(){
    App.like('lower');
});

App.luckyButton.on('click', function () {
    App.like('lucky')
})

$(document).keydown(function(e) {
    if(e.which == 39){
        App.like('higher');
    } else if (e.which == 37){
        App.like('lower');
    } else if (e.which == 38) {
        App.like('lucky');
    }
});

function initcardstack(cards) {
    var cardsobj = JSON.parse(cards);
    cs.init(cardsobj);
};

$(document).ready(function(){
});

function formatNumber(num) {
    if (num != null)
        return num.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,')
    else
        return -1
}