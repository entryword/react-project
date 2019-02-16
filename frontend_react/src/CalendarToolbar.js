import React, { Component } from 'react';
import moment from 'moment';

class CalendarToolbar extends Component {
    state = {
        selectedDate: moment().format('YYYY-MM'),
        prevDate: moment(moment().toDate())
            .subtract(1, 'month')
            .format('YYYY-MM'),
        nextDate: moment(moment().toDate())
            .add(1, 'month')
            .format('YYYY-MM'),
    };

    render() {
        const { selectedDate, prevDate, nextDate } = this.state;
        const { onNavigate } = this.props;
        const onPrev = () => {
            onNavigate('PREV');
            this.setState({
                prevDate: moment(prevDate)
                    .subtract(1, 'month')
                    .format('YYYY-MM'),
                nextDate: moment(nextDate)
                    .subtract(1, 'month')
                    .format('YYYY-MM'),
                selectedDate: moment(selectedDate)
                    .subtract(1, 'month')
                    .format('YYYY-MM'),
            });
        };
        const onNext = () => {
            onNavigate('NEXT');
            this.setState({
                prevDate: moment(prevDate)
                    .add(1, 'month')
                    .format('YYYY-MM'),
                nextDate: moment(nextDate)
                    .add(1, 'month')
                    .format('YYYY-MM'),
                selectedDate: moment(selectedDate)
                    .add(1, 'month')
                    .format('YYYY-MM'),
            });
        };
        return (
            <div className="calendar-toolbar">
                <span className="calendar-nav" onClick={onPrev}>
                    {prevDate}
                </span>
                <i className="fa fa-angle-left" onClick={onPrev} />
                <span className="calendar-now">{selectedDate}</span>
                <i className="fa fa-angle-right" onClick={onNext} />
                <span className="calendar-nav" onClick={onNext}>
                    {' '}
                    {nextDate}
                </span>
            </div>
        );
    }
}

export default CalendarToolbar;
