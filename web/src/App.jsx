import React, { Component } from "react";
import './App.css';

import { CenteredTabs } from './component/Tabs';
import ViewPages from './page/ViewPages';
import DownloadsPage from './page/DownloadsPage'

import { eel } from "./function/eel.js";

class App extends Component {
  constructor(props) {
    super(props);
    eel.set_host("ws://localhost:8888");
    eel.hello();
  }
  render() {
    return (
      <div>
        <CenteredTabs labels={["Views", "Downloads", "Logs"]}>
          <ViewPages></ViewPages>
          <DownloadsPage></DownloadsPage>
          <p>test</p>
        </CenteredTabs>
      </div>
    );
  }
}

export default App;
