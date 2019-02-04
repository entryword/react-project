import React, { Component } from "react";
import Query from "./Query";
import Month from "./Month";
import Year from "./Year";

class Search extends Component {
  render() {
    return (
      <div className="search-box">
        <div className="search-label">Search</div>

        <Query
          value={this.props.query}
          onChange={this.props.handleQueryChange}
        />
        <div className="search-label-year-month">Year-Month</div>
        <Year
          value={this.props.year}
          onChange={this.props.handleYearChange}
          onBlur={this.props.handleYearChange}
        />
        <Month
          value={this.props.month}
          onChange={this.props.handleMonthChange}
          onBlur={this.props.handleMonthChange}
        />
        <div className="search-button">
          <button className="btn pyladies-btn" type="submit">
            Find Events <i className="fa fa-search" />
          </button>
        </div>
      </div>
    );
  }
}

export default Search;
