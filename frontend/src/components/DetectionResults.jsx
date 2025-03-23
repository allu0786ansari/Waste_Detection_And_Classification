import React from "react";

const DetectionResults = ({ results }) => {
  return (
    <div>
      <h3>Detection Results:</h3>
      <pre>{JSON.stringify(results, null, 2)}</pre>
    </div>
  );
};

export default DetectionResults;
