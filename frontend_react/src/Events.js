import React, { Component } from 'react';
import axios from 'axios';
import moment from 'moment';

import Search from './Search';
import Calendar from './Calendar';
import List from './List';
import Filter from './Filter';
import FilterList from './FilterList';

import './react-big-calendar.css';

class Events extends Component {
    constructor(props) {
        super(props);
        this.state = {
            keyword: '',
            year: moment().year(),
            month: moment().month() + 1,
            filterOpen: false,
            viewOptionOpen:
                new URL(window.location.href).searchParams.get('m') ===
                    'false' || this.props.isMobile
                    ? false
                    : true,
            events: {
                count: 0,
                events: [],
            },
            definitions: [],
            order: 'asc',
            filters: {},
            filterReset: false,
        };
        this.queryEvent = {};
        setTimeout(() => {
            if (!this.state.viewOptionOpen) {
                this.handdleSearchAll();
            }
        }, 0);
    }

    filterEvents(events, filters) {
        const processEvents = {};
        const processFilters = {};
        Object.keys(filters).forEach(key => {
            if (filters[key].length > 0) {
                processFilters[key] = filters[key];
            }
        });
        processEvents.events = events.events.filter(event => {
            let result = true;
            Object.keys(processFilters).forEach(key => {
                let filterResult = false;
                if (key === 'level') {
                    filterResult =
                        filterResult ||
                        processFilters[key].indexOf(event.topic[key] + '') >= 0;
                } else if (key === 'field') {
                    const filtered = processFilters[key].filter(k => {
                        return event.event[key].indexOf(parseInt(k, 10)) >= 0;
                    });
                    filterResult = filterResult || filtered.length > 0;
                } else {
                    filterResult =
                        filterResult ||
                        processFilters[key].indexOf(event.event[key] + '') >= 0;
                }
                result = result && filterResult;
            });
            return result;
        });
        processEvents.count = processEvents.events.length;
        this.setState({
            events: processEvents,
        });
    }
    handleQueryChange = event => {
        this.setState({
            keyword: event.target.value,
        });
    };
    handleYearChange = event => {
        this.setState({
            year: event.target.value,
        });
    };
    handleMonthChange = event => {
        this.setState({
            month: event.target.value,
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
                events: this.queryEvent,
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
            this.filterEvents(this.queryEvent, this.state.filters);
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
    // change between calendar and list view
    handleviewOption = () => {
        this.setState(
            {
                viewOptionOpen: !this.state.viewOptionOpen,
            },
            () => {
                // ???????????? ?????????????????????
                if (this.state.viewOptionOpen) {
                    const opt = {
                        keyword: this.state.keyword,
                        year: this.state.year,
                        month: this.state.month,
                    };
                    this.fetchEventsData(opt);
                }
            }
        );
    };
    // change order
    handleOrder = e => {
        const newEvents = {
            count: this.state.events.count,
            events: this.state.events.events.reverse(),
        };
        this.setState({
            order: this.state.order === 'asc' ? 'desc' : 'asc',
            events: newEvents,
        });
    };
    // ??????????????????
    handdleSearchAll = () => {
        const opt = {
            keyword: this.state.keyword,
            year: 'all-year',
            month: 'all-month',
        };
        this.fetchEventsData(opt);
    };
    // query
    handleFind = () => {
        // ??? filter reset
        // this.handleFilterReset();
        const opt = {
            keyword: this.state.keyword,
            year: this.state.year,
            month: this.state.month,
        };
        this.fetchEventsData(opt);
    };
    changeViewOption = () => {};

    handleCalendarDate = date => {
        const year = moment(date).year();
        const month = moment(date).month() + 1;
        this.fetchEventsData({
            keyword: this.state.keyword,
            year,
            month,
        });
        this.setState({
            year,
            month,
        });
    };

    componentDidMount() {
        document.title = 'Event List ????????????';
        document.getElementsByClassName('page-title')[0].innerText =
            'Event List ????????????';
        document.getElementsByClassName('mobile-page-title')[0].innerText =
            'Event List ????????????';
        this.fetchData();
        this.fetchEventsData({});
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
    fetchEventsData(opt) {
        const now = `${moment().year()}-${moment().month() + 1}`;
        const keyword = opt.keyword || '';
        let date;
        if (opt.year === 'all-year' || opt.month === 'all-month') {
            date = null;
        } else {
            date = opt.year && opt.month ? `${opt.year}-${opt.month}` : now;
        }
        const sort = 'date';
        const order = 'asc';
        const apiUrl = this.props.devMode
            ? './data/events.json'
            : '/v1.0/api/events';
        // ???????????? setState???????????? filter????????????
        axios
            .get(apiUrl, {
                params: {
                    keyword,
                    date,
                    order,
                    sort,
                },
            })
            .then(res => {
                // ???????????????????????????????????? filter ??????
                this.queryEvent = res.data.data;
                // ?????????????????? filter ????????????
                if (Object.keys(this.state.filters).length > 0) {
                    this.filterEvents(this.queryEvent, this.state.filters);
                } else {
                    this.setState({
                        events: res.data.data,
                    });
                }
            });
    }

    render() {
        const {
            events,
            definitions,
            order,
            viewOptionOpen,
            filters,
            filterReset,
            filterOpen,
        } = this.state;
        const { isMobile } = this.props;
        return (
            <div>
                <div
                    className={`list-filter ${
                        filterOpen ? '' : 'search-button-position'
                    }`}>
                    <Search
                        keyword={this.state.keyword}
                        month={this.state.month}
                        year={this.state.year}
                        viewOptionOpen={this.state.viewOptionOpen}
                        handleQueryChange={this.handleQueryChange}
                        handleYearChange={this.handleYearChange}
                        handleMonthChange={this.handleMonthChange}
                        handleFind={this.handleFind}
                        handdleSearchAll={this.handdleSearchAll}
                    />
                    <Filter
                        definitions={definitions}
                        filterOpen={filterOpen}
                        handleFiler={this.handleFiler}
                        filters={filters}
                        filterReset={filterReset}
                    />
                    {!isMobile && (
                        <div className="view-box">
                            <div className="view-label">????????????</div>
                            <div>
                                <span
                                    className="view-button"
                                    onClick={this.handleviewOption}>
                                    <i
                                        className={`fa ${
                                            this.state.viewOptionOpen
                                                ? 'fa-calendar-alt'
                                                : 'fa-list-alt'
                                        }`}
                                    />
                                </span>
                            </div>
                        </div>
                    )}
                </div>
                {Object.keys(this.state.filters).length > 0 && (
                    <FilterList
                        filters={filters}
                        definitions={definitions}
                        handleFilterReset={this.handleFilterReset}
                    />
                )}
                {viewOptionOpen && (
                    <Calendar
                        handleCalendarDate={date => {
                            this.handleCalendarDate(date);
                        }}
                        events={events}
                        month={this.state.month}
                        year={this.state.year}
                    />
                )}
                {!viewOptionOpen && (
                    <List
                        events={events}
                        definitions={definitions}
                        order={order}
                        handleOrder={this.handleOrder}
                    />
                )}
            </div>
        );
    }
}

export default Events;
