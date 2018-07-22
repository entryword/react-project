(async () => {
    const footerTemplate = await templates.load('../templates/footer.html'),
        menuTemplage = await templates.load('../templates/menu.html');
    document.querySelector('footer').appendChild(footerTemplate.content.cloneNode(true));
    document.querySelector('.menu-content-side-bar').appendChild(menuTemplage.content.cloneNode(true));
})();