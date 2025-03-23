import React from "react";
import Upload from "./components/Upload";

const App = () => {
  return (
    <div>
      <h1>Litter Detection App</h1>
      <Upload type="image" />
      <Upload type="video" />
    </div>
  );
};

export default App;
