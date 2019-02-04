import React, { Component } from "react";

import moment from "moment";
import "moment/locale/zh-tw";

import Search from "./Search";
import Calendar from "./Calendar";
import List from "./List";

import "./react-big-calendar.css";
import "./App.scss";

class App extends Component {
  state = {
    query: "",
    year: "2019",
    month: "1",
    filterOpen: false,
    viewOptionOpen: true,
    events: {
      count: 0,
      events: []
    },
    definitions: [],
    order: "asc"
  };
  handleQueryChange = event => {
    this.setState({
      query: event.target.value
    });
  };
  handleYearChange = event => {
    this.setState({
      year: event.target.value
    });
  };
  handleMonthChange = event => {
    this.setState({
      month: event.target.value
    });
  };
  handleFiler = () => {
    this.setState({
      filterOpen: !this.state.filterOpen
    });
  };
  handleviewOption = () => {
    this.setState({
      viewOptionOpen: !this.state.viewOptionOpen
    });
  };
  handleOrder = e => {
    this.setState({
      order: this.state.order === "asc" ? "desc" : "asc"
    });
  };
  changeViewOption = () => {};
  componentDidMount() {
    this.fetchData();
    this.fetchEventsData();
  }

  async fetchData() {
    const response = await fetch("./data/definitions.json");
    const data = await response.json();
    console.log(data);
    this.setState({
      definitions: data.data
    });
  }
  async fetchEventsData() {
    const response = await fetch("./data/events.json");
    const data = await response.json();
    console.log(data);
    this.setState({
      events: data.data
    });
  }

  render() {
    const { events, definitions, order, viewOptionOpen } = this.state;
    return (
      <div>
        <div className="list-filter">
          <Search
            query={this.state.query}
            month={this.state.month}
            year={this.state.year}
            handleQueryChange={this.handleQueryChange}
            handleYearChange={this.handleYearChange}
            handleMonthChange={this.handleMonthChange}
          />
          <div className="fitler-box">
            <div className="filter-label">Filter</div>
            <div>
              <span className="filter-button" onClick={this.handleFiler}>
                {this.state.filterOpen ? "Close" : "Open"}
                <i
                  className={`fa ${
                    this.state.filterOpen ? "fa-caret-up" : "fa-caret-down"
                  }`}
                />
              </span>
            </div>
          </div>
          <div className="view-box">
            <div className="view-label">View As</div>
            <div>
              <span className="filter-button" onClick={this.handleviewOption}>
                <i
                  className={`fa ${
                    this.state.viewOptionOpen
                      ? "fa-calendar-alt"
                      : "fa-list-alt"
                  }`}
                />
                <i className="fa fa-caret-down" />
              </span>
            </div>
          </div>
        </div>
        {/* <div>Month: {this.state.month}</div> */}
        {viewOptionOpen && <Calendar events={events} />}
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
