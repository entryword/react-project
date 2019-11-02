import React, { Component } from 'react';
import Query from './Query';
import Month from './Month';
import Year from './Year';

class Search extends Component {
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
        return (
            <div className="search-box">
                <div className="search-label">搜尋</div>
                <Query value={keyword} onChange={handleQueryChange} />
                <div className="search-label-year-month">
                    年份-月份
                    {!viewOptionOpen && (
                        <span
                            className="search-all pyladies-btn"
                            onClick={handdleSearchAll}>
                            搜尋全部活動
                        </span>
                    )}
                </div>
                <Year
                    value={year}
                    onChange={handleYearChange}
                    onBlur={handleYearChange}
                />
                <Month
                    value={month}
                    onChange={handleMonthChange}
                    onBlur={handleMonthChange}
                />
                <div className="search-button">
                    <button className="btn pyladies-btn" onClick={handleFind}>
                        <span className="text">搜尋活動</span>{' '}
                        <i className="fa fa-search" />
                    </button>
                </div>
            </div>
        );
    }
}

export default Search;
