import React, { Component } from 'react';
import Query from './Query';
import Month from './Month';
import Year from './Year';

class Search extends Component {
    state = {
        time:
            new URL(window.location.href).searchParams.get('m') === 'false'
                ? 'all'
                : 'period',
        disabledTime:
            new URL(window.location.href).searchParams.get('m') === 'false',
    };
    handleSwitchSearch = event => {
        const value = event.target.value;
        this.setState({
            time: value,
            disabledTime: value === 'all',
        });
    };
    shouldComponentUpdate(nextProps, nextState) {
        // 日曆切換到 日期區間 而且年代月份不要 disabled
        if (nextProps.viewOptionOpen) {
            nextState.time = 'period';
            nextState.disabledTime = false;
        }
        return true;
    }
    render() {
        const {
            handleQueryChange,
            handleYearChange,
            handleMonthChange,
            handleFind,
            handdleSearchAll,
            keyword,
            year,
            month,
            viewOptionOpen,
        } = this.props;
        const { disabledTime } = this.state;
        return (
            <div className="search-box">
                <div className="search-label">搜尋</div>
                <Query value={keyword} onChange={handleQueryChange} />
                <div className="search-label-year-month">
                    <div className="form-check form-check-inline">
                        <input
                            type="radio"
                            id="time-period"
                            className="form-check-input"
                            name="time"
                            value="period"
                            checked={this.state.time === 'period'}
                            onChange={this.handleSwitchSearch}
                        />
                        <label
                            className="form-check-label"
                            htmlFor="time-period">
                            年份-月份
                        </label>
                    </div>
                    <div className="form-check form-check-inline">
                        <input
                            type="radio"
                            id="time-all"
                            className="form-check-input"
                            name="time"
                            value="all"
                            checked={this.state.time === 'all'}
                            disabled={viewOptionOpen}
                            onChange={this.handleSwitchSearch}
                        />
                        <label className="form-check-label" htmlFor="time-all">
                            全部時間{disabledTime}
                        </label>
                    </div>
                </div>
                <Year
                    value={year}
                    onChange={handleYearChange}
                    onBlur={handleYearChange}
                    disabledTime={disabledTime}
                />
                <Month
                    value={month}
                    onChange={handleMonthChange}
                    onBlur={handleMonthChange}
                    disabledTime={disabledTime}
                />
                <div className="search-button">
                    {this.state.time === 'period' && (
                        <button
                            className="btn pyladies-btn"
                            onClick={handleFind}>
                            <span className="text">搜尋活動</span>{' '}
                            <i className="fa fa-search" />
                        </button>
                    )}
                    {this.state.time === 'all' && (
                        <button
                            className="btn pyladies-btn"
                            onClick={handdleSearchAll}>
                            <span className="text">搜尋活動</span>{' '}
                            <i className="fa fa-search" />
                        </button>
                    )}
                </div>
            </div>
        );
    }
}

export default Search;
