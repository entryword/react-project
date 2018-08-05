let fixedMenuOffset = -100;
let fixedItemOffset = -200;
let timeDurationOffset = 450;
const eventMenu =  document.querySelector('#event-menu-list').getBoundingClientRect();
let  timeOffset = -1 * (eventMenu.top + eventMenu.height + 30)  - window.scrollY;
if(window.innerWidth<768){
    fixedMenuOffset = -50;
    fixedItemOffset = -1 * (eventMenu.height + 50);
    timeOffset -= 20;
    timeDurationOffset = document.querySelector(".event-menu-header").getBoundingClientRect().height + 60;
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
const timeSession = new ScrollMagic.Scene({
    triggerElement: "#event-first-session",
    offset: timeOffset,
    duration: (document.querySelector('.event-first-session').getBoundingClientRect().height + timeDurationOffset)
})
    .setClassToggle("#event-first", "active")
    // .addIndicators()
    .addTo(controller);
const contentSession = new ScrollMagic.Scene({triggerElement: "#event-second-session",
    offset: fixedItemOffset,
    duration: document.querySelector('.event-second-session').getBoundingClientRect().height + 30})
    .setClassToggle("#event-second", "active")
    // .addIndicators()
    .addTo(controller);
const tutorSession = new ScrollMagic.Scene({triggerElement: "#event-tutor-session",
    offset: fixedItemOffset,
    duration: document.querySelector('.event-tutor-session').getBoundingClientRect().height + 30})
    .setClassToggle("#event-tutor", "active")
    // .addIndicators()
    .addTo(controller);
const materialSession = new ScrollMagic.Scene({triggerElement: "#event-material-session",
    offset: fixedItemOffset,
    duration: document.querySelector('.event-material-session').getBoundingClientRect().height + 30})
    .setClassToggle("#event-material", "active")
    // .addIndicators()
    .addTo(controller);
const retroSession = new ScrollMagic.Scene({triggerElement: "#event-retro-session",
    offset: fixedItemOffset,
    duration: document.querySelector('.event-retro-session').getBoundingClientRect().height + 30})
    .setClassToggle("#event-retro", "active")
    // .addIndicators()
    .addTo(controller);