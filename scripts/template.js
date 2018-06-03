(async () => {
    const footerTemplate = await templates.load('../templates/footer.html')
    document.querySelector('footer').appendChild(footerTemplate.content.cloneNode(true));
})();