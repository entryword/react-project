import React, { Component } from 'react';
import moment from 'moment';

class CalendarToolbar extends Component {
    render() {
        const { onNavigate, date } = this.props;
        const selectedDate = moment(date).format('YYYY-MM');
        const prevDate = moment(moment(date).toDate())
            .subtract(1, 'month')
            .format('YYYY-MM');
        const nextDate = moment(moment(date).toDate())
            .add(1, 'month')
            .format('YYYY-MM');
        const onPrev = () => {
            onNavigate('PREV');
        };
        const onNext = () => {
            onNavigate('NEXT');
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
