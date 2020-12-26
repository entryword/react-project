import React, { Component } from 'react';
// import moment from "moment";

class TopicList extends Component {
    render() {
        const topicData = this.props.topics.topics || [];

        const { definitions, order, handleOrder } = this.props;

        return (
            <div className="event-list-view">
                <h2 className="search-result">
                    共 {this.props.topics.count} 筆搜尋結果
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
                {topicData.map(topic => (
                    <section className="event-card" key={topic.id}>
                        <header className="event-card-title">
                            <h3>
                                <a
                                    href={`/events/topic.html?id=${topic.id}`}
                                    rel="noopener noreferrer"
                                    target="_blank">
                                    {topic.name}
                                </a>
                            </h3>
                            <h2>
                                <a
                                    href={`/events/event.html?id=${topic.id}`}
                                    rel="noopener noreferrer"
                                    target="_blank">
                                    {topic.title}
                                </a>
                            </h2>
                        </header>
                        <article className="event-card-content">
                            <p className="sub-title">
                                {definitions.host[topic.host]} -{' '}
                                {definitions.freq[topic.freq]}
                            </p>
                            <p className="sub-title">
                                {definitions.level &&
                                    definitions.level[topic.level]}
                            </p>
                            <p className="tags">
                                {definitions.field &&
                                    topic.fields.map(
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

export default TopicList;
