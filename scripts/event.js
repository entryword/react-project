(function (tw_pyladies) {
    // data
    const mapUrl = {
        'aic': 'https://www.google.com/maps/search/?api=1&query=25.043494,121.559860&query_place_id=ChIJwd1FrMCrQjQRAnOWONioLcI',
        'tpewomen': 'https://www.google.com/maps/search/?api=1&query=25.033459,121.501280&query_place_id=ChIJaRFJC6-pQjQRx9I-a2QVtYI'
    };
    const days = ['日', '一', '二', '三', '四', '五', '六'];
    tw_pyladies.path = getPath();
    // handlerbars helper
    // 如果講書沒有給圖，放入預設圖
    Handlebars.registerHelper("setDefaultHeadShout", function(url) {
        if(!url) {
            return "/images/logos/twgirl_logo.png";
        }
        return url;
    });
    // 地圖 如果沒有url 地圖不用給連結
    Handlebars.registerHelper('setMapPageLink', function(url) {
        let result = "";
        if(!!url){
            url  = Handlebars.Utils.escapeExpression(url);
            result = new Handlebars.SafeString(`<a href="${url}"><i class="fa fa-external-link-alt"></i></a>`);
        }
        return result;
    });
    // 地圖 如果沒有url GoogleMap 地圖不用給連結
    Handlebars.registerHelper('setGoogleMapLink', function(url) {
        let result = "";
        if(!!url){
            url  = Handlebars.Utils.escapeExpression(url);
            result = new Handlebars.SafeString(`<a href="${url}"><i class="fa fa-clone"></i></a>`);
        }
        return result;
    });
    Handlebars.registerHelper('noResources', function(slides, resources) {
        let result = "";
        if(!slides && !resources){
            result = "尚無資源";
        }
        if(slides.length === 0 && resources.length===0){
            result = "尚無資源";
        }
        return result;
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
        return !results ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
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
        return axios.get('../data/definition.json');
    }

    // TODO: 確認 API URL
    function getEvent() {
        let id = getUrlParameter('id'), url;
        if(tw_pyladies.path === 'topic'){
            url = '../data/topic.json';
        }else{
            url = '../data/event.json';
        }

        return axios.get(url);
    }
    axios.all([getDefinition(), getEvent()])
        .then(axios.spread(function (definition, event) {
            if(tw_pyladies.path === 'event'){
                eventTemplating(definition.data.data, event.data.data);
            }else{
                topicTemplating(definition.data.data, event.data.data);
            }
            // template 完成後再處理 scroll 位置
            tw_pyladies.goScroll();
        }))
        .catch(function (error) {
            console.log(error)
        });

    // template
    function eventTemplating(definition, data) {
        let place = '';
        if(data.place_info.name.toLowerCase().indexOf('aic')>=0){
            place = 'aic';
        }else if(data.place_info.name.toLowerCase().indexOf('tpewomen')>=0){
            place = 'tpewomen';
        }
        //data processing
        data.hostName = definition.host[data.host];
        data.levelName = definition.level[data.level];
        data.placeGoogleMap = !!place ? mapUrl[place] : '';
        data.day = days[new Date(data.date).getUTCDay()];
        data.tags = data.fields.map(field=> "#" + definition.field[field] + " ");
        // template blocks
        const blocks = ['event-header-content', 'event-time', 'event-content','event-tutor','event-material'];
        renderHtml(blocks, data);
    }
    function topicTemplating(definition, data) {
        //data processing
        data.hostName = definition.host[data.host];
        data.freqName = definition.freq[data.freq];
        data.levelName = definition.level[data.level];
        data.tags = data.fields.map(field=> "#" + definition.field[field] + " ");
        data.events.forEach(event=>{
            event.day = days[new Date(event.date).getUTCDay()];
        })
        // template blocks
        const blocks = ['event-header-content', 'event-time', 'event-content','event-tutor','event-material'];
        renderHtml(blocks, data);
    }

    function renderHtml(blocks, data){
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