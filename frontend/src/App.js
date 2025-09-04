import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import CyberAirwaysLanding from "./components/CyberAirwaysLanding";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<CyberAirwaysLanding />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;