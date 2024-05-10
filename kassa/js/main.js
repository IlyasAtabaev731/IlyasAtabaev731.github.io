$(document).ready(function () {
    $(function () {
        let tg = window.Telegram.WebApp;
        tg.expand();
        
        $('.show_second_cont').click(function(){
            $('.main_cont1').css('display', 'none');
            $('.main_cont2').css('display','block');
        });

        $('.show_first_cont').click(function(){
            $('.main_cont1').css('display', 'block');
            $('.main_cont2').css('display','none');
        });

        $('#skipButton').click(function(){
            window.location.href = "https://ilyasatabaev731.github.io/game";
        })

        $('#workButton').click(function(){
            window.location.href = "https://ilyasatabaev731.github.io/game";
        })
        
    });

    $(function () {
        new WOW().init();
    });

    $(function(){
        $(".main_cont1").on("swipeleft", swipeHandler);
        $(".main_cont1").on("swiperight", swipeHandler);
        $(".main_cont2").on("swipeleft", swipeHandler2);
        $(".main_cont2").on("swiperight", swipeHandler2);
      
        function swipeHandler(event) {
        //   $(event.target).removeClass("right left");
          $('.main_cont1').css('display', 'none');
          $('.main_cont2').css('display','block');
          event.type == 'swipeleft' ? $(event.target).addClass("left") : $(event.target).addClass("right");
        }

        function swipeHandler2(event) {
            //   $(event.target).removeClass("right left");
              $('.main_cont1').css('display', 'block');
              $('.main_cont2').css('display','none');
              event.type == 'swipeleft' ? $(event.target).addClass("left") : $(event.target).addClass("right");
        }
    })

});


