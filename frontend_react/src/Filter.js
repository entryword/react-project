import React, { Component } from 'react';

class Filter extends Component {
    state = {
        status: {},
        time: {},
        level: {},
        field: {},
        weekday: {},
        close: {
            status: false,
            time: false,
            level: false,
            field: false,
            weekday: false,
        },
    };
    filterName = ['status', 'time', 'level', 'field', 'weekday'];
    // 選項
    processFilter = () => {
        this.filterName.forEach(filter => {
            this.props.filters[filter] = Object.keys(this.state[filter]).reduce(
                (prev, item) => {
                    if (this.state[filter][item]) {
                        return (prev = [...prev, item]);
                    }
                    return prev;
                },
                []
            );
        });
    };
    // checheck box action
    handleChange = (event, itemName) => {
        const target = event.target;
        const value = target.checked;
        const name = target.name;
        this.setState(
            {
                [itemName]: { ...this.state[itemName], [name]: value },
            },
            this.processFilter
        );
    };
    // 開合
    handleAccordion = itemName => {
        this.setState({
            close: {
                ...this.state.close,
                [itemName]: !this.state.close[itemName],
            },
        });
    };
    resetFilter = definitions => {
        const state = {};
        this.filterName.forEach(filter => {
            state[filter] = {};
            for (let l in definitions[filter]) {
                state[filter][l] = false;
            }
        });
        this.setState({
            ...state,
        });
    };

    // 處理 parent 非同步傳來的資訊
    componentDidUpdate(prevProps) {
        const { definitions, filterReset } = this.props;
        if (definitions !== prevProps.definitions) {
            this.resetFilter(definitions);
        }
        if (filterReset !== prevProps.filterReset) {
            if (filterReset) {
                this.resetFilter(definitions);
            }
        }
    }
    render() {
        const {
            definitions,
            filterOpen,
            handleFiler,
            isTopicPage,
            isSpeakerPage,
        } = this.props;
        const { status, time, level, field, weekday, close } = this.state;
        return (
            <React.Fragment>
                <div className="fitler-box">
                    <div className="filter-label">篩選器</div>
                    <div>
                        <span className="filter-button" onClick={handleFiler}>
                            {filterOpen ? 'Close' : 'Open'}
                            <i
                                className={`fa ${
                                    filterOpen ? 'fa-caret-up' : 'fa-caret-down'
                                }`}
                            />
                        </span>
                    </div>
                </div>
                <div
                    className={`filter-container 
                        ${filterOpen ? '' : 'hide'}  
                        ${isTopicPage ? 'topic-filter' : ''}
                        ${isSpeakerPage ? 'speaker-filter' : ''}`}>
                    {!isTopicPage && !isSpeakerPage && (
                        <React.Fragment>
                            <div className="filter-column">
                                <div className="filter-item">
                                    <h4
                                        onClick={() => {
                                            this.handleAccordion('status');
                                        }}>
                                        <i
                                            className={`fa ${
                                                close.status
                                                    ? 'fa-caret-up'
                                                    : 'fa-caret-down'
                                            }`}
                                        />
                                        By Status
                                    </h4>
                                    <div
                                        className={`${
                                            close.status ? 'hide' : ''
                                        }`}>
                                        {definitions.status &&
                                            Object.keys(definitions.status).map(
                                                l => (
                                                    <div
                                                        className="form-check"
                                                        key={l}>
                                                        <input
                                                            className="form-check-input"
                                                            type="checkbox"
                                                            id={`status${l}`}
                                                            name={l}
                                                            checked={
                                                                status[l] ||
                                                                false
                                                            }
                                                            onChange={event =>
                                                                this.handleChange(
                                                                    event,
                                                                    'status'
                                                                )
                                                            }
                                                        />
                                                        <label
                                                            className="form-check-label"
                                                            htmlFor={`status${l}`}>
                                                            {
                                                                definitions
                                                                    .status[l]
                                                            }
                                                        </label>
                                                    </div>
                                                )
                                            )}
                                    </div>
                                </div>
                                <div className="filter-item">
                                    <h4
                                        onClick={() => {
                                            this.handleAccordion('weekday');
                                        }}>
                                        <i
                                            className={`fa ${
                                                close.weekday
                                                    ? 'fa-caret-up'
                                                    : 'fa-caret-down'
                                            }`}
                                        />
                                        By Weekday
                                    </h4>
                                    <div
                                        className={`${
                                            close.weekday ? 'hide' : ''
                                        }`}>
                                        {definitions.weekday &&
                                            Object.keys(
                                                definitions.weekday
                                            ).map(l => (
                                                <div
                                                    className="form-check"
                                                    key={l}>
                                                    <input
                                                        className="form-check-input"
                                                        type="checkbox"
                                                        id={`weekday${l}`}
                                                        name={l}
                                                        checked={
                                                            weekday[l] || false
                                                        }
                                                        onChange={event =>
                                                            this.handleChange(
                                                                event,
                                                                'weekday'
                                                            )
                                                        }
                                                    />
                                                    <label
                                                        className="form-check-label"
                                                        htmlFor={`weekday${l}`}>
                                                        {definitions.weekday[l]}
                                                    </label>
                                                </div>
                                            ))}
                                    </div>
                                </div>
                            </div>
                            <div className="filter-column">
                                <div className="filter-item">
                                    <h4
                                        onClick={() => {
                                            this.handleAccordion('time');
                                        }}>
                                        <i
                                            className={`fa ${
                                                close.time
                                                    ? 'fa-caret-up'
                                                    : 'fa-caret-down'
                                            }`}
                                        />
                                        By Time
                                    </h4>
                                    <div
                                        className={`${
                                            close.time ? 'hide' : ''
                                        }`}>
                                        {definitions.time &&
                                            Object.keys(definitions.time).map(
                                                l => (
                                                    <div
                                                        className="form-check"
                                                        key={l}>
                                                        <input
                                                            className="form-check-input"
                                                            type="checkbox"
                                                            id={`time${l}`}
                                                            name={l}
                                                            checked={
                                                                time[l] || false
                                                            }
                                                            onChange={event =>
                                                                this.handleChange(
                                                                    event,
                                                                    'time'
                                                                )
                                                            }
                                                        />
                                                        <label
                                                            className="form-check-label"
                                                            htmlFor={`time${l}`}>
                                                            {
                                                                definitions
                                                                    .time[l]
                                                            }
                                                        </label>
                                                    </div>
                                                )
                                            )}
                                    </div>
                                </div>
                            </div>
                        </React.Fragment>
                    )}
                    {!isSpeakerPage && (
                        <div className="filter-column">
                            <div className="filter-item">
                                <h4
                                    onClick={() => {
                                        this.handleAccordion('level');
                                    }}>
                                    <i
                                        className={`fa ${
                                            close.level
                                                ? 'fa-caret-up'
                                                : 'fa-caret-down'
                                        }`}
                                    />
                                    By Level
                                </h4>
                                <div className={`${close.level ? 'hide' : ''}`}>
                                    {definitions.level &&
                                        Object.keys(definitions.level).map(
                                            l => (
                                                <div
                                                    className="form-check"
                                                    key={l}>
                                                    <input
                                                        className="form-check-input"
                                                        type="checkbox"
                                                        id={`level${l}`}
                                                        name={l}
                                                        checked={
                                                            level[l] || false
                                                        }
                                                        onChange={event =>
                                                            this.handleChange(
                                                                event,
                                                                'level'
                                                            )
                                                        }
                                                    />
                                                    <label
                                                        className="form-check-label"
                                                        htmlFor={`level${l}`}>
                                                        {definitions.level[l]}
                                                    </label>
                                                </div>
                                            )
                                        )}
                                </div>
                            </div>
                        </div>
                    )}
                    <div className="filter-column">
                        <div className="filter-item">
                            <h4
                                onClick={() => {
                                    this.handleAccordion('field');
                                }}>
                                <i
                                    className={`fa ${
                                        close.field
                                            ? 'fa-caret-up'
                                            : 'fa-caret-down'
                                    }`}
                                />
                                By Field
                            </h4>
                            <div className={`${close.field ? 'hide' : ''}`}>
                                {definitions.field &&
                                    Object.keys(definitions.field).map(l => (
                                        <div className="form-check" key={l}>
                                            <input
                                                className="form-check-input"
                                                type="checkbox"
                                                id={`field${l}`}
                                                name={l}
                                                checked={field[l] || false}
                                                onChange={event =>
                                                    this.handleChange(
                                                        event,
                                                        'field'
                                                    )
                                                }
                                            />
                                            <label
                                                className="form-check-label"
                                                htmlFor={`field${l}`}>
                                                {definitions.field[l]}
                                            </label>
                                        </div>
                                    ))}
                            </div>
                        </div>
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default Filter;
