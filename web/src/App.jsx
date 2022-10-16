import React, { Component } from "react";
// import {hot} from 'react-hot-loader'
import './App.css';

import { CenteredTabs } from './component/Tabs';
import ViewPages from './page/ViewPages';
import DownloadsPage from './page/DownloadsPage'
import Users from "./page/Users";

import { eel } from "./function/eel.js";

class App extends Component {
  constructor(props) {
    super(props);
    eel.set_host("ws://localhost:8888");
    // eel.hello();
  }
  render() {
    return (
      <div>
        <CenteredTabs labels={[
          "Views", 
          "Downloads", 
          "Users", 
          "Logs",
        ]}>
          <ViewPages></ViewPages>
          <DownloadsPage></DownloadsPage>
          <Users></Users>
          <p>test</p>
        </CenteredTabs>
      </div>
    );
  }
}

export default App;
// export default process.env.NODE_ENV === "development" ? hot(module)(App) : App
