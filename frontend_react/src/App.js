import React, { Component } from 'react';
import axios from 'axios';
import moment from 'moment';

import Search from './Search';
import Calendar from './Calendar';
import List from './List';
import Filter from './Filter';
import FilterList from './FilterList';

import './react-big-calendar.css';
import './App.scss';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            keyword: '',
            year: moment().year(),
            month: moment().month() + 1,
            filterOpen: false,
            viewOptionOpen: (new URL(window.location.href).searchParams.get('m') === 'false')? false:true,
            events: {
                count: 0,
                events: [],
            },
            definitions: [],
            places: [],
            order: 'asc',
            filters: {},
            filterReset: false,
        };
        this.queryEvent = {};
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
                if (key === 'place') {
                    filterResult =
                        filterResult ||
                        processFilters[key].indexOf(
                            event.event.place_info.name
                        ) >= 0;
                } else if (key === 'level') {
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
        this.setState({
            viewOptionOpen: !this.state.viewOptionOpen,
        });
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
    // query
    handleFind = () => {
        // 把 filter reset
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
        this.fetchData();
        this.fetchEventsData({});
        this.fetchPlacesData();
    }

    fetchData() {
        const apiUrl = '/v1.0/api/definitions';
        // const apiUrl = `http://localhost:5555/v1.0/api/definitions`;
        // const apiUrl = `./data/definitions.json`;
        axios.get(apiUrl).then(res => {
            this.setState({
                definitions: res.data.data,
            });
        });
    }
    fetchEventsData(opt) {
        const now = `${moment().year()}-${moment().month() + 1}`;
        const keyword = opt.keyword || '';
        const date = opt.year && opt.month ? `${opt.year}-${opt.month}` : now;
        const sort = 'date';
        const order = 'asc';
        const apiUrl = '/v1.0/api/events';
        // const apiUrl = 'http://localhost:5555/v1.0/api/events';
        // const apiUrl = `./data/events.json`;
        // 取得資料 setState走完，跑 filter處理資料
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
                // 儲存最原始資料，還沒經過 filter 處理
                this.queryEvent = res.data.data;
                // 判斷是否需要 filter 處理資料
                if (Object.keys(this.state.filters).length > 0) {
                    this.filterEvents(this.queryEvent, this.state.filters);
                } else {
                    this.setState({
                        events: res.data.data,
                    });
                }
            });
    }
    fetchPlacesData() {
        const apiUrl = '/v1.0/api/places';
        // const apiUrl = `http://localhost:5555/v1.0/api/places`;
        // const apiUrl = `./data/places.json`;
        axios.get(apiUrl).then(res => {
            this.setState({
                places: res.data.data.places,
            });
        });
    }

    render() {
        const {
            events,
            definitions,
            places,
            order,
            viewOptionOpen,
            filters,
            filterReset,
        } = this.state;
        return (
            <div>
                <div className="list-filter">
                    <Search
                        keyword={this.state.keyword}
                        month={this.state.month}
                        year={this.state.year}
                        handleQueryChange={this.handleQueryChange}
                        handleYearChange={this.handleYearChange}
                        handleMonthChange={this.handleMonthChange}
                        handleFind={this.handleFind}
                    />
                    <Filter
                        definitions={definitions}
                        places={places}
                        filterOpen={this.state.filterOpen}
                        handleFiler={this.handleFiler}
                        filters={filters}
                        filterReset={filterReset}
                    />
                    <div className="view-box">
                        <div className="view-label">顯示模式</div>
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

export default App;
