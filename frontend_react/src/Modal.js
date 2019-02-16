import React from "react";
import { createPortal } from "react-dom";

const modalRoot = document.getElementById("modal");
export default class Modal extends React.Component {
  constructor(props) {
    super(props);
    this.el = document.createElement("div");
  }
  componentDidMount() {
    modalRoot.appendChild(this.el);
  }
  // 避免累積過多 memory leak
  componentWillUnmount() {
    modalRoot.removeChild(this.el);
  }
  render() {
    return createPortal(this.props.children, this.el);
  }
}
