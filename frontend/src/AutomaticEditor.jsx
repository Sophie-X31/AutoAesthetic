import { useState } from "react";
import "./AutomaticEditor.css";

function AutomaticEditor() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [enhancedUrl, setEnhancedUrl] = useState(null);
  const [params, setParams] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
        return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setEnhancedUrl(null);
    setParams(null);
  };

  const handleEnhance = async () => {
    if (!selectedFile) return;

    setEnhancedUrl(null);
    setParams(null);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    const response = await fetch("http://localhost:8000/automatic-editor", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    setEnhancedUrl(`${data.image_url}?t=${Date.now()}`);
    setParams(data.params);
    setLoading(false);
  };

  const handleDownload = async () => {
    if (!enhancedUrl) return;

    const response = await fetch(enhancedUrl);
    const blob = await response.blob();

    const blobUrl = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = blobUrl;
    link.download = "enhanced_image.jpg";

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);

    URL.revokeObjectURL(blobUrl);
  };

  return (
    <main className="main">
      <div className="page-title-row">
        <h2>Automatic Editor</h2>

        {enhancedUrl && (
            <button
            className="download-button"
            onClick={handleDownload}
            >
            Download Enhanced Image
            </button>
        )}
      </div>

      <label className="upload-label">
        Choose Image
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
        />
      </label>

      {loading && (
        <div className="loading-box">
          <div className="spinner"></div>
          <p>Enhancing your image...</p>
        </div>
      )}

      {(previewUrl || enhancedUrl) && (
        <div className="image-comparison">
            {previewUrl && (
            <div className="image-card">
                <h3>Original Image</h3>

                <img
                    src={previewUrl}
                    alt="Original"
                    className="preview-image"
                />

                <div className="image-footer">
                    {params && (
                    <p className="score-text">
                        Original Score: {params.original_score.toFixed(3)}
                    </p>
                    )}

                    <button
                    className="enhance-button"
                    onClick={handleEnhance}
                    disabled={loading}
                    >
                    {loading ? "Enhancing..." : "Enhance"}
                    </button>
                </div>
                </div>
            )}

            {enhancedUrl && (
            <div className="image-card">
                <h3>Enhanced Image</h3>

                <img
                    src={enhancedUrl}
                    alt="Enhanced"
                    className="preview-image"
                />

                <div className="image-footer">
                    {params && (
                    <p className="score-text">
                        Final Score: {params.final_score.toFixed(3)}
                    </p>
                    )}
                </div>
            </div>
            )}
        </div>
      )}

      {params?.enhancements && (
        <div className="params-box">
          <h3>The following enhancements are recommended:</h3>

          <ul>
            {Object.entries(params.enhancements)
              .filter(([key]) => key !== "final_score")
              .map(([key, value]) => (
                <li key={key}>
                  <strong>{key}:</strong>{" "}
                  {typeof value === "number"
                    ? value.toFixed(3)
                    : value}
                </li>
              ))}
          </ul>
        </div>
      )}

      {params?.history && (
        <div className="params-box">
          <h3>Enhancement Steps</h3>

          <ol>
            {params.history.map((step) => (
              <li key={step.iteration}>
                {step.parameter} {step.change > 0 ? "+" : ""}
                {step.change.toFixed(2)}
              </li>
            ))}
          </ol>
        </div>
      )}
    </main>
  );
}

export default AutomaticEditor;