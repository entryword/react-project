import React, { Component } from 'react';
// import moment from "moment";

class List extends Component {
    render() {
        const eventData = this.props.events.events;

        const { definitions, order, handleOrder } = this.props;

        return (
            <div className="event-list-view">
                <h2 className="search-result">
                    共 {this.props.events.count} 筆搜尋結果
                    <span className="time-order" onClick={handleOrder}>
                        {order === 'asc' && (
                            <React.Fragment>
                                <span>開始日期 過去到未來</span>
                                <i className="fa fa-caret-up" />
                            </React.Fragment>
                        )}
                        {order === 'desc' && (
                            <React.Fragment>
                                <span>開始日期 未來到過去</span>
                                <i className="fa fa-caret-down" />
                            </React.Fragment>
                        )}
                    </span>
                </h2>
                {eventData.map(item => (
                    <section className="event-card" key={item.event.id}>
                        <header className="event-card-title">
                            <h3>
                                <a
                                    href={`/events/event.html?id=${
                                        item.event.id
                                    }`}
                                    rel="noopener noreferrer"
                                    target="_blank">
                                    {item.topic && item.topic.name}
                                </a>
                                -
                            </h3>
                            <h2>
                                <a
                                    href={`/events/event.html?id=${
                                        item.event.id
                                    }`}
                                    rel="noopener noreferrer"
                                    target="_blank">
                                    {item.event.title}
                                </a>
                            </h2>
                        </header>
                        <article className="event-card-content">
                            <p className="date">
                                {item.event.date} {item.event.start_time} ~{' '}
                                {item.event.end_time}
                                {item.event.place_info &&
                                    ` @ ${item.event.place_info.name}`}
                            </p>
                            <p className="level">
                                {definitions.level &&
                                    item.topic &&
                                    definitions.level[item.topic.level]}
                            </p>
                            <p className="tags">
                                {definitions.field &&
                                    item.event.field.map(
                                        field =>
                                            '#' + definitions.field[field] + ' '
                                    )}
                            </p>
                        </article>
                    </section>
                ))}
            </div>
        );
    }
}

export default List;
