import React, { Component} from "react";

import Topic from './Topic';
import Utterance from './Utterance';
import '../App.css';

export default class Main extends Component {
  render() {
    return (
      <main className="content main-frame">
      <h1 className="text-black text-uppercase text-center my-4">Small Data</h1>
        <div className="mx-auto p-0">

            <Topic currentTopic={this.props.currentTopic}/>
            <Utterance newUtterance={this.props.newUtterance}/>

        </div>
      </main>
    );
  }
}
