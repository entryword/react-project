import React, { Component } from 'react';
import axios from 'axios';

import SpeakerSearch from './Speakers/Search';
import SpeakerList from './Speakers/List';
import Filter from './Filter';
import FilterList from './FilterList';

import './Speakers.scss';

class Speakers extends Component {
    constructor(props) {
        super(props);
        this.state = {
            keyword: '',
            filterOpen: false,
            definitions: [],
            filters: {},
            filterReset: false,
            speakers: {
                count: 0,
                speakers: [],
            },
        };
        this.querySpeakers = {};
        this.querySpeakers = {
            count: 0,
            speakers: [],
        };
        // setTimeout(() => {
        //     if (!this.state.viewOptionOpen) {
        //         this.handdleSearchAll();
        //     }
        // }, 0);
    }
    filterspeakers(speakers, filters) {
        const processspeakers = {};
        const processFilters = {};
        Object.keys(filters).forEach(key => {
            if (filters[key].length > 0) {
                processFilters[key] = filters[key];
            }
        });
        processspeakers.speakers = speakers.speakers.filter(speaker => {
            let result = true;
            Object.keys(processFilters).forEach(key => {
                let filterResult = false;
                if (key === 'field') {
                    const filtered = processFilters[key].filter(k => {
                        return speaker['fields'].indexOf(parseInt(k, 10)) >= 0;
                    });
                    filterResult = filterResult || filtered.length > 0;
                } else {
                    filterResult =
                        filterResult ||
                        processFilters[key].indexOf(speaker[key] + '') >= 0;
                }
                result = result && filterResult;
            });
            return result;
        });
        processspeakers.count = processspeakers.speakers.length;
        this.setState({
            speakers: processspeakers,
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
                speakers: this.querySpeakers,
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
            this.filterspeakers(this.querySpeakers, this.state.filters);
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

    // query
    handleFind = () => {
        // 把 filter reset
        this.handleFilterReset();
        const opt = {
            keyword: this.state.keyword,
        };
        this.fetchSpeakersData(opt);
    };

    componentDidMount() {
        document.title = 'Speaker List 講師列表';
        document.getElementsByClassName('page-title')[0].innerText =
            'Speaker List 講師列表';
        document.getElementsByClassName('mobile-page-title')[0].innerText =
            'Speaker List 講師列表';
        this.fetchData();
        this.fetchSpeakersData();
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

    fetchSpeakersData(opt) {
        const keyword = (opt && opt.keyword) || '';
        const apiUrl = this.props.devMode
            ? './data/speakers.json'
            : '/v1.0/api/speakers';
        // 取得資料 setState走完，跑 filter處理資料
        axios
            .get(apiUrl, {
                params: {
                    keyword,
                },
            })
            .then(res => {
                // 儲存最原始資料，還沒經過 filter 處理
                this.querySpeakers = res.data.data;
                // console.log(res.data.data);
                // 判斷是否需要 filter 處理資料
                if (Object.keys(this.state.filters).length > 0) {
                    this.filterspeakers(this.querySpeakers, this.state.filters);
                } else {
                    this.setState({
                        speakers: res.data.data,
                    });
                }
            });
    }

    render() {
        const {
            speakers,
            definitions,
            filters,
            filterReset,
            filterOpen,
        } = this.state;
        return (
            <div>
                <div
                    className={`list-filter none-event ${
                        filterOpen ? '' : 'search-button-position'
                    }`}>
                    <SpeakerSearch
                        keyword={this.state.keyword}
                        handleQueryChange={this.handleQueryChange}
                        handleFind={this.handleFind}
                        handdleSearchAll={this.handdleSearchAll}
                    />
                    <Filter
                        isSpeakerPage={true}
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
                <SpeakerList speakers={speakers} definitions={definitions} />
            </div>
        );
    }
}

export default Speakers;
