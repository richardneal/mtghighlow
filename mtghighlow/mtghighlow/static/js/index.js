$('a[href*=#]').click(function(){return false;});

var animationEndEvent = "webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend";
var cs = new CardStack();

function CardStack() {
    var wrap = $('#cards');
    var last_card;

    this.updatevisuals = function (streak, current_card, best_streak, result) {
        if (this.last_card != null) {
            $('#fakepriceold').html('$' + formatNumber(this.last_card.fake_price));
            $('#realpriceold').html('$' + formatNumber(this.last_card.real_price));
            if ((this.last_card.name).length > 17)
                this.last_card.name = (this.last_card.name).substring(0, 17) + '...';
            $('#nameold').html(this.last_card.name);
        }

        if (current_card != null) {
            $('#displayprice').html('$' + formatNumber(current_card.fake_price));
            $('#cardname').html(current_card.name)
            $('#setname').html(current_card.set_full)
            $('#rarity').html(current_card.rarity)
            this.last_card = current_card;
        }

        if (result != null) {
            switch (result) {
                case 'Correct':
                    $('#correct').html('CORRECT');
                    $('#correct').removeClass('wrong').removeClass('lucky').addClass('correct')
                    break
                case 'Incorrect':
                    $('#correct').html('WRONG');
                    $('#correct').removeClass('correct').removeClass('lucky').addClass('wrong')
                    break
                case 'Lucky':
                    $('#correct').html('LUCKY')
                    $('#correct').removeClass('wrong').removeClass('correct').addClass('lucky')
                    break
                case 'Unlucky':
                    $('#correct').html('NOT LUCKY')
                    $('#correct').removeClass('correct').removeClass('lucky').addClass('wrong')
                    break
                case 'Tricked':
                    $('#correct').html('TRICKED')
                    $('#correct').removeClass('wrong').removeClass('correct').addClass('lucky')
                    break
                case 'Error':
                default:
                    $('#correct').html('ERROR')
                    $('#correct').removeClass('correct').removeClass('wrong').removeClass('lucky')
                    break
            }
        }

        if (streak != null) {
            $('#correct').append(' (' + streak)
        }

        if (best_streak != null) {
            $('#correct').append('/' + best_streak + ')')
        }
    }

    this.init = function (cards) {
        this.updatevisuals(null, cards[0]);
        for (var i = 0; i < cards.length; i++) {
            wrap.append("<div class='magiccard'><img alt='" + cards[i].name + "' src='" + cards[i].image + "' /></div>");
        }
    }

    this.cycle = function (new_card, streak, current_card, best_streak, correct) {
        this.updatevisuals(streak, current_card, best_streak, correct);
        wrap.append("<div class='magiccard'><img alt='" + new_card.name + "' src='" + new_card.image + "' /></div>");
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
                    cs.cycle(data.new_card, data.current_streak_length, data.current_card, data.best_streak_length, data.correct);
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