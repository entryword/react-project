import React from 'react';
import { createPortal } from 'react-dom';

const modalRoot = document.getElementById('modal');
export default class Modal extends React.Component {
    constructor(props) {
        super(props);
        this.el = document.createElement('div');
    }
    componentDidMount() {
        if (modalRoot.hasChildNodes())
            modalRoot.removeChild(modalRoot.lastChild);
        modalRoot.appendChild(this.el);
    }
    // 避免累積過多 memory leak
    componentWillUnmount() {
        if (modalRoot.hasChildNodes())
            modalRoot.removeChild(modalRoot.lastChild);
    }
    render() {
        return createPortal(this.props.children, this.el);
    }
}
