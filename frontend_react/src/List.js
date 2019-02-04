import React, { Component } from "react";
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
            {order === "asc" && (
              <React.Fragment>
                <span>開始時間新到舊</span>
                <i className="fa fa-caret-down" />
              </React.Fragment>
            )}
            {order === "desc" && (
              <React.Fragment>
                <span>開始時間舊到新</span>
                <i className="fa fa-caret-up" />
              </React.Fragment>
            )}
          </span>
        </h2>
        {eventData.map(item => (
          <section className="event-card" key={item.event.id}>
            <header className="event-card-title">
              <h3>{item.topic && item.topic.name + " -"}</h3>
              <h2>{item.event.title}</h2>
            </header>
            <article className="event-card-content">
              <p className="date">
                {item.event.date} {item.event.start_time} ~{" "}
                {item.event.end_time}
                {item.event.place_info && ` @ ${item.event.place_info.name}`}
              </p>
              <p className="level">
                {definitions.level &&
                  item.topic &&
                  definitions.level[item.topic.level]}
              </p>
              <p className="tags">
                {definitions.field &&
                  item.event.fields.map(
                    field => "#" + definitions.field[field] + " "
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
