import React from 'react';

function Query(props) {
    return (
        <input
            type="text"
            className="form-control search-query"
            onChange={props.onChange}
            id="query"
            value={props.value}
            placeholder="Topic/Keyword"
            maxLength="30"
        />
    );
}

export default Query;
