(function (tw_pyladies) {
    // data
    const mapUrl = {
        'aic': 'https://www.google.com/maps/search/?api=1&query=25.043494,121.559860&query_place_id=ChIJwd1FrMCrQjQRAnOWONioLcI',
        'tpewomen': 'https://www.google.com/maps/search/?api=1&query=25.033459,121.501280&query_place_id=ChIJaRFJC6-pQjQRx9I-a2QVtYI'
    };
    const days = ['日', '一', '二', '三', '四', '五', '六'];
    tw_pyladies.path = getPath();
    // handlerbars helper
    // 如果講師沒有給圖，放入預設圖
    Handlebars.registerHelper("setDefaultHeadShot", function(url) {
        if(!url || url == 'null') {
            return "../images/logos/twgirl_logo.png";
        }
        return url;
    });
    // 地圖 如果沒有url 地圖不用給連結
    Handlebars.registerHelper('setMapPageLink', function(url) {
        let result = "";
        if(!!url){
            url  = Handlebars.Utils.escapeExpression(url);
            result = new Handlebars.SafeString(`<div class="color-gray">詳細路線說明<a href="${url}" target="_blank"> <i class="fa fa-external-link-alt"></i></a></div>`);
        }
        return result;
    });
    // 地圖 如果沒有url GoogleMap 地圖不用給連結
    Handlebars.registerHelper('setGoogleMapLink', function(url) {
        let result = "";
        if(!!url){
            url  = Handlebars.Utils.escapeExpression(url);
            result = new Handlebars.SafeString(`<a href="${url}"><i class="fa fa-map-marked-alt"></i></a>`);
        }
        return result;
    });
    // 沒有資源的顯示
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
    // 報名 如果時間已過 就不用給連結
    Handlebars.registerHelper('setSignupLink', function(eventId, date) {
        let result = "";
        if(Date.parse(date) > Date.parse(new Date())){
            eventId  = Handlebars.Utils.escapeExpression(eventId);
            result = new Handlebars.SafeString(`<a class="sign-up-btn" href="/signup/signup.html?id=${eventId}">按此報名</a>`);
        }
        return result;
    });
    Handlebars.registerHelper('setCopyBtn', function(addr){
        let result = "";
        if(addr && addr != '未定'){
            result = new Handlebars.SafeString(`<a class="copy-btn" href="#"><i class="fa fa-clone"></i></a>`);
        }
        return result;
    });
    Handlebars.registerHelper('setAllEvent', function(events){
        let result = "";
        if(events.length < 4){
            result = new Handlebars.SafeString(`<div class="col-lg-3 col-md-6 item"><div class="topic-title">
                    <span>其他</span></div><div class="event-title"><a class="pink-link" href="/eventlist/events" target="_blank">所有活動</a></div></div>`);
            document.getElementById('eventlist_link').style.display = "none";
        }
        return result;
    });
    // Get Data
    // get pathname from url
    function getPath(){
        // let regex =  /\/fs\/([^&#]*).html/;
        // pathname = "/event/123"
        // let regex =  /(event|topic)\/([0-9]+)/;
        // result[1]: event
        // result[2]: 123 (id)
        // let results = regex.exec(window.location.pathname);
        // return !results ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
        if(window.location.pathname.indexOf('topic')>=0){
            return 'topic';
        }else if (window.location.pathname == "/"){
            return 'top';
        }else if (window.location.pathname.indexOf('signup')>=0){
            return 'signup';
        }else if (window.location.pathname.indexOf('speaker')>=0){
            return 'speaker';
        }else{
            return 'event';
        }
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
        // return axios.get(`/fakedata/definition.json`);
        return axios.get('/v1.0/api/definitions');
    }

    // API
    function getEvent() {
        let id = getUrlParameter('id') || 1,
            url;
        tw_pyladies.path = getPath();
        console.log(tw_pyladies.path )
        if(tw_pyladies.path === 'topic'){
            // url = `/fakedata/topic46.json`;
            url = `/v1.0/api/topic/${id}`;
        }else if(tw_pyladies.path === 'top'){
            // url = `/fakedata/top_info.json`;
            url = `/v1.0/api/events_from_distinct_topics`;
        }else if(tw_pyladies.path === 'signup'){
            // url = `/fakedata/apply_info.json`;
            url = `/v1.0/api/event/${id}/apply_info`;
        }else if(tw_pyladies.path === 'speaker'){
            // url = `/fakedata/speaker.json`;
            url = `/v1.0/api/speaker/${id}`;
        }else{
            // url = `/fakedata/event137.json`;
            url = `/v1.0/api/event/${id}`;
        }
        return axios.get(url);
    }
    axios.all([getDefinition(), getEvent()])
        .then(axios.spread(function (definition, event) {
            if(tw_pyladies.path === 'event'){
                axios.get(`/v1.0/api/topic/${event.data.data.topic_info.id}`).then(function(response){
                    eventTemplating(definition.data.data, event.data.data, response.data.data.freq);
                })
                .catch(function (error) {
                    window.location = '/error/error.html';
                });
            }else if(tw_pyladies.path === 'top'){
                topTemplating(definition.data.data, event.data.data);
            }else if(tw_pyladies.path === 'signup'){
                signupTemplating(definition.data.data, event.data.data)
            }else if(tw_pyladies.path === 'speaker'){
                console.log(event.data.data);
                speakerTemplating(definition.data.data, event.data.data)
            }else{
                topicTemplating(definition.data.data, event.data.data);
            }
            // template 完成後再處理 scroll 位置
            if(tw_pyladies.goScroll){
                tw_pyladies.goScroll();
            }
        }))
        .catch(function (error) {
            // window.location = '/error/error.html';
        });

    // template
    function topTemplating(definition, data) {
        //data processing
        data.events.forEach(event=>{
            event.day = days[new Date(event.event_info.date).getUTCDay()];
        })
        // template blocks
        const blocks = ['event'];
        renderHtml(blocks, data);
    }
    function eventTemplating(definition, data, freq) {
        let place = '';
        if(data.place_info.name.toLowerCase().indexOf('aic')>=0){
            place = 'aic';
        }else if(data.place_info.name.toLowerCase().indexOf('tpewomen')>=0){
            place = 'tpewomen';
        }
        //data processing
        data.hostName = definition.host[data.host];
        data.freqName = definition.freq[freq];
        data.levelName = definition.level[data.level];
        data.placeGoogleMap = !!place ? mapUrl[place] : '';
        data.day = days[new Date(data.date).getUTCDay()];
        data.tags = data.fields.map(field=> "#" + definition.field[field] + " ");
        data.eventId = getUrlParameter('id') || 1;
        if(data.speakers.length == 0){
            data.speakers.push({
                "id": -1, 
                "name": "待定", 
                "photo": null
            });
        }
        // template blocks
        const blocks = ['event-signup','event-header-content', 'event-time', 'event-content','event-tutor','event-material'];
        renderHtml(blocks, data);
        const copy_btn = document.querySelector('.copy-btn');
        if(copy_btn){
            copy_btn.addEventListener("click", function (e) {
                e.preventDefault();
                function SelectText(element) {
                    var range, selection;
                    if (document.body.createTextRange) {
                        range = document.body.createTextRange();
                        range.moveToElementText(element);
                        range.select();
                    } else if (window.getSelection) {
                        selection = window.getSelection();
                        range = document.createRange();
                        range.selectNodeContents(element);
                        selection.removeAllRanges();
                        selection.addRange(range);
                    }
                    document.execCommand("copy");
                }
                SelectText(this.previousElementSibling);
            }, false);
        }
    }
    function topicTemplating(definition, data) {
        //data processing
        data.hostName = definition.host[data.host];
        data.freqName = definition.freq[data.freq];
        data.tags = data.fields.map(field=>  "#" + definition.field[field] + " ");
        data.events.forEach(event=>{
            event.day = days[new Date(event.date).getUTCDay()];
        })
        // template blocks
        const blocks = ['event-header-content', 'event-time', 'event-content','event-tutor','event-material'];
        renderHtml(blocks, data);
    }
    function signupTemplating(definition, data) {
        //data processing
        const channel_urls = ['meetup.html', 'accupass.html'];
        data.apply.forEach((a, index)=>{
            a.start_day = days[new Date(a.start_time).getUTCDay()];
            a.start_date = a.start_time.split(" ")[0];
            a.start_time = a.start_time.split(" ")[1];

            a.end_day = days[new Date(a.end_time).getUTCDay()];
            a.end_date = a.end_time.split(" ")[0];
            a.end_time = a.end_time.split(" ")[1];
            a.eventId = definition.channel[a.channel];
            a.channelName = definition.channel[a.channel];
            a.channelNum = a.channel+1;
            a.channelIndex = index +1;
            a.channelUrl = channel_urls[a.channel];
            a.type = definition.type[a.type];
        })
        const blocks = ['event-menu-list', 'event-body'];
        // template blocks
        renderHtml(blocks, data);
    }
    
    function speakerTemplating(definition, data) {
        console.log('speaker data', data)
        //data processing
        data.tags = data.fields.map(field=>  "#" + definition.field[field] + " ");
        
        // template blocks
        const blocks = ['speaker-image', 'speaker-name', 'speaker-intro','speaker-topic'];
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