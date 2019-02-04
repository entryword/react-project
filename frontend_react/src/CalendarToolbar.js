import React, { Component } from "react";
import moment from "moment";

class CalendarToolbar extends Component {
  state = {
    selectedDate: moment().format("YYYY-MM"),
    prevDate: moment(moment().toDate())
      .subtract("month", 1)
      .format("YYYY-MM"),
    nextDate: moment(moment().toDate())
      .add("month", 1)
      .format("YYYY-MM")
  };

  render() {
    const { selectedDate, prevDate, nextDate } = this.state;
    const { onNavigate } = this.props;
    const onPrev = () => {
      console.log("prev");
      onNavigate("PREV");
      this.setState({
        prevDate: moment(prevDate)
          .subtract("month", 1)
          .format("YYYY-MM"),
        nextDate: moment(nextDate)
          .subtract("month", 1)
          .format("YYYY-MM"),
        selectedDate: moment(selectedDate)
          .subtract("month", 1)
          .format("YYYY-MM")
      });
    };
    const onNext = () => {
      console.log("next");
      onNavigate("NEXT");
      this.setState({
        prevDate: moment(prevDate)
          .add("month", 1)
          .format("YYYY-MM"),
        nextDate: moment(nextDate)
          .add("month", 1)
          .format("YYYY-MM"),
        selectedDate: moment(selectedDate)
          .add("month", 1)
          .format("YYYY-MM")
      });
    };
    return (
      <div className="calendar-toolbar">
        <span className="calendar-nav" onClick={onPrev}>
          {prevDate}
        </span>
        <i className="fa fa-angle-left" />
        <span className="calendar-now">{selectedDate}</span>
        <i className="fa fa-angle-right" />
        <span className="calendar-nav" onClick={onNext}>
          {" "}
          {nextDate}
        </span>
      </div>
    );
  }
}

export default CalendarToolbar;
