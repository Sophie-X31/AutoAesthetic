import "./AutomaticEditor.css";
import { useState } from "react";

function AutomaticEditor() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [enhancedUrl, setEnhancedUrl] = useState(null);
  const [params, setParams] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setEnhancedUrl(null);
    setParams(null);
  };

  const handleEnhance = async () => {
    if (!selectedFile) return;

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

  return (
    <main className="main">
      <h2>Automatic Editor</h2>

      <input type="file" accept="image/*" onChange={handleFileChange} />

      {previewUrl && (
        <div>
          <h3>Original Image</h3>
          <img src={previewUrl} alt="Original" className="preview-image" />
        </div>
      )}

      <button className="enhance-button" onClick={handleEnhance}>
        {loading ? "Enhancing..." : "Enhance"}
      </button>

      {enhancedUrl && (
        <div>
          <h3>Enhanced Image</h3>
          <img src={enhancedUrl} alt="Enhanced" className="preview-image" />
        </div>
      )}

      {params && (
        <div className="params-box">
          <h3>Enhancements Made</h3>
          <ul>
            {Object.entries(params).map(([key, value]) => (
              <li key={key}>
                <strong>{key}:</strong> {value}
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}

export default AutomaticEditor;