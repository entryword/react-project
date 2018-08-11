(async () => {
    const footerTemplate = await templates.load('../templates/footer.html'),
        menuTemplage = await templates.load('../templates/menu.html');
    document.querySelector('footer').appendChild(footerTemplate.content.cloneNode(true));
<<<<<<< HEAD
=======
    document.querySelector('.menu-content-top-nav').appendChild(menuTemplage.content.cloneNode(true));
>>>>>>> a6ee26f4aab65184f77bf17e552f1c427089f44e
    document.querySelector('.menu-content-side-bar').appendChild(menuTemplage.content.cloneNode(true));
})();