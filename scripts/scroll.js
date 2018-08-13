(function () {
    // top nav
    let fixedMenuOffset = -100;
    // nav + menu list + spacing (人工決定)
    let fixedItemOffset = -200;
    // nav + header image + spacing (人工決定)
    let timeDurationOffset = 450;
    // nav + menu list
    let anchorMenuOffset = 184;
    const blocks = ['event-first', 'event-second', 'event-third','event-fourth','event-fifth'];
    const eventMenu = document.querySelector('#event-menu-list').getBoundingClientRect();
    let timeOffset = -1 * (eventMenu.top + eventMenu.height + 30) - window.scrollY;
    // 手機版
    if (window.innerWidth < 768) {
        fixedMenuOffset = -50;
        fixedItemOffset = -1 * (eventMenu.height + 50);
        timeOffset -= 20;
        timeDurationOffset = document.querySelector(".event-menu-header").getBoundingClientRect().height + 60;
        anchorMenuOffset = 154;
    }
    // ScrollMagic
    const controller = new ScrollMagic.Controller({
        globalSceneOptions: {
            triggerHook: 'onLeave'
        }
    });
    //  fixed event menu
    const scene = new ScrollMagic.Scene({offset: fixedMenuOffset, triggerElement: "#event-menu-list"})
        .setPin("#event-menu-list", {pushFollowers: false})
        .addTo(controller);
    // event menu class
    for(let i=0, len=blocks.length;i<len;i++){
        let duration, offset;
        if(i===0){
            duration = document.querySelector('.'+ blocks[i] +'-session').getBoundingClientRect().height + timeDurationOffset;
            offset = timeOffset;
        }else{
            duration = document.querySelector('.'+ blocks[i] +'-session').getBoundingClientRect().height + 30;
            offset = fixedItemOffset;
        }
        new ScrollMagic.Scene({
            triggerElement: "#"+blocks[i]+"-session",
            offset: offset,
            duration: duration
        })
            .setClassToggle("#"+ blocks[i] , "active")
            // .addIndicators()
            .addTo(controller);
    }

// 定義 scrollTo function
    controller.scrollTo(function (newpost) {
        let top = newpost - anchorMenuOffset;
        window.scrollTo({
            top: top,
            behavior: "smooth"
        });
    });

    document.querySelector('.event-menu-list').addEventListener("click", function (e) {
        for (let target = e.target; target && target !== this; target = target.parentNode) {
            if (target.matches('li')) {
                handler.call(target, e);
                break;
            }
        }
    }, false);

    function handler(e) {
        let id = "#" + e.target.id + "-session";
        controller.scrollTo(id);
    }
})();