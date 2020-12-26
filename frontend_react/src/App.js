import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect,
} from 'react-router-dom';

import Events from './Events';
import Topics from './Topics';
import Speakers from './Speakers';

import './Events.scss';

export default function App() {
    const isMobile = window.innerWidth < 768;
    return (
        <Router>
            <Switch>
                {/* dev router */}
                <Route path="/events">
                    <Events devMode={true} isMobile={isMobile} />
                </Route>
                <Route path="/topics">
                    <Topics devMode={true} />
                </Route>
                <Route path="/speakers">
                    <Speakers devMode={true} />
                </Route>
                {/* production router */}
                <Route path="/eventlist/events">
                    <Events devMode={false} isMobile={isMobile} />
                </Route>
                <Route path="/eventlist/topics">
                    <Topics devMode={false} />
                </Route>
                <Route path="/eventlist/speakers">
                    <Speakers devMode={false} />
                </Route>
            </Switch>
        </Router>
    );
}
