import React, { Component } from 'react';
import Query from '../Query';

class SpeakerSearch extends Component {
    render() {
        const { handleQueryChange, handleFind, keyword } = this.props;
        return (
            <div className="search-box none-event">
                <div className="search-label">搜尋</div>
                <Query
                    value={keyword}
                    onChange={handleQueryChange}
                    placeholder="講師關鍵字"
                />
                <div className="search-button none-event">
                    <button className="btn pyladies-btn" onClick={handleFind}>
                        <span className="text">搜尋講師</span>{' '}
                        <i className="fa fa-search" />
                    </button>
                </div>
            </div>
        );
    }
}

export default SpeakerSearch;
