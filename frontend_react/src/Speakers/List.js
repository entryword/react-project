import React, { Component } from 'react';
// import moment from "moment";

class SpeakerList extends Component {
    render() {
        const speakerData = this.props.speakers.speakers;

        const { definitions, order, handleOrder } = this.props;

        return (
            <div className="event-list-view">
                <h2 className="search-result">
                    共 {this.props.speakers.count} 筆搜尋結果
                    {/* <span className="time-order" onClick={handleOrder}>
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
                    </span> */}
                </h2>
                <div className="speaker-list">
                    {speakerData.map(speaker => (
                        <a
                            key={speaker.id}
                            className="event-card"
                            href={`/events/speaker.html?id=${speaker.id}`}
                            rel="noopener noreferrer"
                            target="_blank">
                            <section key={speaker.id}>
                                <header className="event-card-title">
                                    <div className="speaker-image">
                                        <img
                                            src={
                                                speaker.photo ||
                                                'https://tw.pyladies.com/images/logos/twgirl_logo.png'
                                            }
                                            alt={speaker.name}
                                        />
                                    </div>
                                    <h3 className="speaker-name">
                                        {speaker.name}
                                    </h3>
                                    <h4 className="speaker-title">
                                        {speaker.title}
                                    </h4>
                                </header>
                                <article className="event-card-content">
                                    <p className="tags">
                                        {definitions.field &&
                                            speaker.fields.map(
                                                field =>
                                                    '#' +
                                                    definitions.field[field] +
                                                    ' '
                                            )}
                                    </p>
                                </article>
                            </section>
                        </a>
                    ))}
                </div>
            </div>
        );
    }
}

export default SpeakerList;
