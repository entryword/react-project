import React, { Component } from 'react';

import BigCalendar from 'react-big-calendar';
import moment from 'moment';
import 'moment/locale/zh-tw';
import Modal from './Modal';
import CalendarToolbar from './CalendarToolbar';

class Calendar extends Component {
    state = {
        defaultDate: moment().toDate(),
        selectedId: 0,
    };
    processEventList = dataList => {
        const process = dataList.map(item => ({
            id: item.event.id,
            title: item.event.title,
            start: moment(
                `${item.event.date} ${item.event.start_time}`
            ).toDate(),
            end: moment(`${item.event.date} ${item.event.start_time}`).toDate(),
            date: item.event.date,
            start_time: item.event.start_time,
            end_time: item.event.end_time,
            field: item.event.field,
            place_info: item.event.place_info,
            status: item.event.status,
            time: item.event.time,
            weekday: item.event.weekday,
            topic: item.topic,
        }));
        return process;
    };
    handleDateClick = event => {
        this.setState({
            selectedId: parseInt(event.currentTarget.dataset.id, 10),
        });
    };
    toggleModal = () => {
        this.setState({
            selectedId: 0,
        });
    };

    onNavigate = (date, view) => {
        this.props.handleCalendarDate(moment(date).format('YYYY-M'));
    };

    render() {
        const eventsList = this.props.events
            ? this.processEventList(this.props.events.events)
            : [];
        const { defaultDate, selectedId } = this.state;
        const date = moment(`${this.props.year}-${this.props.month}`).toDate();
        const localizer = BigCalendar.momentLocalizer(moment);
        const EventComponent = item => {
            return (
                <div className="eventCell">
                    <div onClick={this.handleDateClick} data-id={item.event.id}>
                        {item.title}
                    </div>
                    {selectedId === item.event.id && (
                        <Modal>
                            <h3>
                                活動
                                <button
                                    className="modal-btn"
                                    onClick={this.toggleModal}>
                                    <i className="fa fa-times" />
                                </button>
                            </h3>
                            <h4>
                                <a
                                    href={`/events/event.html?id=${
                                        item.event.id
                                    }`}
                                    rel="noopener noreferrer"
                                    target="_blank">
                                    {item.event.title}
                                </a>
                            </h4>
                            <p className="modal-date">
                                {item.event.date} {item.event.start_time}~
                                {item.event.end_time}
                            </p>
                            {item.event.place_info && (
                                <p className="modal-place">
                                    @ {item.event.place_info.name}
                                </p>
                            )}
                        </Modal>
                    )}
                </div>
            );
        };

        return (
            <div className="calendar-view">
                <h2 className="search-result">
                    共 {this.props.events.count} 筆搜尋結果
                </h2>
                <BigCalendar
                    localizer={localizer}
                    events={eventsList}
                    views={['month']}
                    step={30}
                    startAccessor="start"
                    date={date}
                    defaultDate={defaultDate}
                    endAccessor="end"
                    onView={this.onView}
                    onNavigate={this.onNavigate}
                    components={{
                        event: EventComponent,
                        toolbar: CalendarToolbar,
                    }}
                />
            </div>
        );
    }
}

export default Calendar;
