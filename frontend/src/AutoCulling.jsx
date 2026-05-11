import { useState } from "react";
import "./AutoCulling.css";

function AutoCulling() {
  const [files, setFiles] = useState([]);
  const [previewItems, setPreviewItems] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files || []);

    setFiles(selectedFiles);
    setResults([]);

    setPreviewItems(
      selectedFiles.map((file) => ({
        filename: file.name,
        image_url: URL.createObjectURL(file),
      }))
    );
  };

  const handleRankImages = async () => {
    if (files.length === 0) return;

    setLoading(true);
    setResults([]);

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    const response = await fetch("http://localhost:8000/auto-culling", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    setResults(data.results);
    setLoading(false);
  };

  return (
    <main className="main">
      <h2>Auto Culling</h2>

      <label className="upload-label">
        Upload Folder of Images
        <input
          type="file"
          accept="image/*"
          multiple
          webkitdirectory=""
          directory=""
          onChange={handleFileChange}
        />
      </label>

      {previewItems.length > 0 && (
        <>
          <h3>Uploaded Images</h3>

          <div className="horizontal-scroll">
            {previewItems.map((item, index) => (
              <div className="culling-card" key={`${item.filename}-${index}`}>
                <img
                  src={item.image_url}
                  alt={item.filename}
                  className="culling-image"
                />
                <p className="filename">{item.filename}</p>
              </div>
            ))}
          </div>

          <button
            className="rank-button"
            onClick={handleRankImages}
            disabled={loading}
          >
            {loading ? "Ranking..." : "Rank Images"}
          </button>
        </>
      )}

      {loading && (
        <div className="loading-box">
          <div className="spinner"></div>
          <p>Ranking uploaded images...</p>
        </div>
      )}

      {results.length > 0 && (
        <>
          <h3>Ranked Images</h3>

          <div className="horizontal-scroll">
            {results.map((item, index) => (
              <div className="culling-card" key={item.filename}>
                <div className="rank-badge">#{index + 1}</div>

                <img
                  src={item.image_url}
                  alt={item.filename}
                  className="culling-image"
                />

                <p className="filename">{item.filename}</p>
                <p className="score">Score: {item.score.toFixed(3)}</p>
              </div>
            ))}
          </div>
        </>
      )}
    </main>
  );
}

export default AutoCulling;