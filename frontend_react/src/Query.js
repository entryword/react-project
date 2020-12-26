import React from 'react';

function Query(props) {
    return (
        <input
            type="text"
            className="form-control search-query"
            onChange={props.onChange}
            id="query"
            value={props.value}
            placeholder={props.placeholder || '主題/關鍵字/名字'}
            maxLength="30"
        />
    );
}

export default Query;
