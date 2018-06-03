/*! 
https://gist.github.com/olanod/ede8befb771057bb004c4f57be591640/
*/
const templates = Object.create(null, {
    load: {
        value: async function(fileName) {
        const url = new URL(fileName,
            document.currentScript && document.currentScript.src || location.href);
        if (url in this) return this[url]
        // fetch and parse template as string
        let template = await fetch(url);
        template = await template.text();
        template = new DOMParser().parseFromString(template, 'text/html').querySelector('template');
        if (!template) throw new TypeError('No template element found')
        document.head.append(template)
        this[url] = template
        return template
        }
    }
    });