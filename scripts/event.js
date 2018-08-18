(function (tw_pyladies) {
    // data
    const mapUrl = {
        'aic': 'https://www.google.com/maps/search/?api=1&query=25.043494,121.559860&query_place_id=ChIJwd1FrMCrQjQRAnOWONioLcI',
        'tpewomen': 'https://www.google.com/maps/search/?api=1&query=25.033459,121.501280&query_place_id=ChIJaRFJC6-pQjQRx9I-a2QVtYI'
    };
    const placePage = {
        'aic': '/venue/aic.html',
        'tpewomen': '/venue/tpewomen.html'
    };
    const address = {
        'aic': '台北市信義區光復南路133號1樓',
        'tpewomen': '台北市萬華區艋舺大道 101 號'
    };
    const pathName = getPath();
    // handlerbars helper
    Handlebars.registerHelper("setDefaultHeadShout", function(url) {
        if(!url) {
            return "/images/logos/twgirl_logo.png";
        }
        return url;
    });
    // Get Data
    // get pathname from url
    function getPath(){
        let regex =  /\/events\/([^&#]*).html/;
        // pathname = "/event/123"
        // let regex =  /(event|topic)\/([0-9]+)/;
        // result[1]: event
        // result[2]: 123 (id)

        let results = regex.exec(window.location.pathname);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }
    //get id from url
    // ref: https://github.com/WebReflection/url-search-params
    function getUrlParameter(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(window.location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }
    function getDefinition() {
        return axios.get('/data/definition.json');
    }

    function getEvent() {
        let id = getUrlParameter('id');
        let url = `/data/${pathName}.json`;
        return axios.get(url);
    }
    axios.all([getDefinition(), getEvent()])
        .then(axios.spread(function (definition, event) {
            if(pathName === 'event'){
                eventTemplating(definition.data, event.data);
            }else{
                topicTemplating(definition.data, event.data);
            }
            tw_pyladies.goScroll();
        }))
        .catch(function (error) {
            console.log(error)
        });

    // template
    function eventTemplating(definition, data) {
        let place = data.place_info.name.toLowerCase() === 'aic' ? 'aic': 'tpewomen';
        //data processing
        data.hostName = definition.host[data.host];
        data.levelName = definition.level[data.level];
        data.placeAddress = address[place];
        data.placePage = placePage[place];
        data.placeMap = mapUrl[place];
        data.tags = data.fields.map(field=> "#" + definition.field[field] + " ");
        // template
        const blocks = ['event-header-content', 'event-time', 'event-content','event-tutor','event-material'];
        for(let i=0, len = blocks.length;i<len;i++){
            //Grab the inline template
            let template = document.getElementById(blocks[i] + '-template').innerHTML;
            //Compile the template
            let compiled_template = Handlebars.compile(template);
            //Render the data into the template
            let rendered = compiled_template(data);
            //Overwrite the contents of #target with the renderer HTML
            document.getElementById(blocks[i]).innerHTML = rendered;
        }
    }
    function topicTemplating(definition, data) {
        //data processing
        data.hostName = definition.host[data.host];
        data.freqName = definition.freq[data.freq];
        data.levelName = definition.level[data.level];
        data.tags = data.fields.map(field=> "#" + definition.field[field] + " ");
        // template
        const blocks = ['event-header-content', 'event-time', 'event-content','event-tutor','event-material'];
        for(let i=0, len = blocks.length;i<len;i++){
            //Grab the inline template
            let template = document.getElementById(blocks[i] + '-template').innerHTML;
            //Compile the template
            let compiled_template = Handlebars.compile(template);
            //Render the data into the template
            let rendered = compiled_template(data);
            //Overwrite the contents of #target with the renderer HTML
            document.getElementById(blocks[i]).innerHTML = rendered;
        }
    }
})(tw_pyladies);