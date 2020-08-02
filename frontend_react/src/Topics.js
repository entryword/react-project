import React, { Component } from 'react';
import axios from 'axios';

import TopicSearch from './Topics/Search';
import TopicList from './Topics/List';
import Filter from './Filter';
import FilterList from './FilterList';

class Topics extends Component {
    constructor(props) {
        super(props);
        this.state = {
            keyword: '',
            filterOpen: false,
            definitions: [],
            places: [],
            order: 'asc',
            filters: {},
            filterReset: false,
            topics: {
                count: 0,
                topics: [],
            },
        };
        this.queryTopics = {};
        this.queryTopics = {
            count: 0,
            topics: [],
        };
        // setTimeout(() => {
        //     if (!this.state.viewOptionOpen) {
        //         this.handdleSearchAll();
        //     }
        // }, 0);
    }
    filterEvents(topics, filters) {
        const processEvents = {};
        const processFilters = {};
        Object.keys(filters).forEach(key => {
            if (filters[key].length > 0) {
                processFilters[key] = filters[key];
            }
        });
        processEvents.topics = topics.topics.filter(topic => {
            let result = true;
            Object.keys(processFilters).forEach(key => {
                let filterResult = false;
                if (key === 'level') {
                    filterResult =
                        filterResult ||
                        processFilters[key].indexOf(topic[key] + '') >= 0;
                } else if (key === 'field') {
                    const filtered = processFilters[key].filter(k => {
                        return topic['fields'].indexOf(parseInt(k, 10)) >= 0;
                    });
                    filterResult = filterResult || filtered.length > 0;
                } else {
                    filterResult =
                        filterResult ||
                        processFilters[key].indexOf(topic[key] + '') >= 0;
                }
                result = result && filterResult;
            });
            return result;
        });
        processEvents.count = processEvents.topics.length;
        this.setState({
            topics: processEvents,
        });
    }

    handleQueryChange = event => {
        this.setState({
            keyword: event.target.value,
        });
    };

    // reset filter
    resetFilter() {
        this.setState({
            filterReset: false,
        });
    }
    handleFilterReset = () => {
        this.setState(
            {
                filterReset: true,
                topics: this.queryTopics,
                filters: {},
            },
            this.resetFilter
        );
    };
    // filter action
    processFilter() {
        if (
            Object.keys(this.state.filters).length > 0 &&
            !this.state.filterOpen
        ) {
            this.filterEvents(this.queryTopics, this.state.filters);
        }
    }

    handleFiler = () => {
        this.setState(
            {
                filterOpen: !this.state.filterOpen,
            },
            this.processFilter
        );
    };

    // change order
    handleOrder = e => {
        const newEvents = {
            count: this.state.topics.count,
            topics: this.state.topics.topics.reverse(),
        };
        this.setState({
            order: this.state.order === 'asc' ? 'desc' : 'asc',
            topics: newEvents,
        });
    };
    // 搜尋全部活動
    // handdleSearchAll = () => {
    //     const opt = {
    //         keyword: this.state.keyword,
    //         year: 'all-year',
    //         month: 'all-month',
    //     };
    //     this.fetchTopicsData(opt);
    // };
    // query
    handleFind = () => {
        // 把 filter reset
        this.handleFilterReset();
        const opt = {
            keyword: this.state.keyword,
            // year: this.state.year,
            // month: this.state.month,
        };
        this.fetchTopicsData(opt);
    };

    componentDidMount() {
        document.title = 'Topic List 主題列表';
        document.getElementsByClassName('page-title')[0].innerText =
            'Topic List 主題列表';
        document.getElementsByClassName('mobile-page-title')[0].innerText =
            'Topic List 主題列表';
        this.fetchData();
        this.fetchTopicsData();
    }

    fetchData() {
        const apiUrl = this.props.devMode
            ? './data/definitions.json'
            : '/v1.0/api/definitions';
        axios.get(apiUrl).then(res => {
            this.setState({
                definitions: res.data.data,
            });
        });
    }

    fetchTopicsData(opt) {
        const keyword = (opt && opt.keyword) || '';
        const sort = 'date';
        const order = 'asc';
        const apiUrl = this.props.devMode
            ? './data/topics.json'
            : '/v1.0/api/topics';
        // 取得資料 setState走完，跑 filter處理資料
        // console.log(apiUrl);
        axios
            .get(apiUrl, {
                params: {
                    keyword,
                    order,
                    sort,
                },
            })
            .then(res => {
                // 儲存最原始資料，還沒經過 filter 處理
                this.queryTopics = res.data.data;
                // 判斷是否需要 filter 處理資料
                if (Object.keys(this.state.filters).length > 0) {
                    this.filterEvents(this.queryTopics, this.state.filters);
                } else {
                    this.setState({
                        topics: res.data.data,
                    });
                }
            });
    }

    render() {
        const {
            topics,
            definitions,
            order,
            filters,
            filterReset,
            filterOpen,
        } = this.state;
        // console.log(topics);
        return (
            <div>
                <div
                    className={`list-filter none-event ${
                        filterOpen ? '' : 'search-button-position'
                    }`}>
                    <TopicSearch
                        keyword={this.state.keyword}
                        handleQueryChange={this.handleQueryChange}
                        handleFind={this.handleFind}
                        z
                        handdleSearchAll={this.handdleSearchAll}
                    />
                    <Filter
                        isTopicPage={true}
                        definitions={definitions}
                        filterOpen={filterOpen}
                        handleFiler={this.handleFiler}
                        filters={filters}
                        filterReset={filterReset}
                    />
                </div>
                {Object.keys(this.state.filters).length > 0 && (
                    <FilterList
                        filters={filters}
                        definitions={definitions}
                        handleFilterReset={this.handleFilterReset}
                    />
                )}

                <TopicList
                    topics={topics}
                    definitions={definitions}
                    order={order}
                    handleOrder={this.handleOrder}
                />
            </div>
        );
    }
}

export default Topics;
