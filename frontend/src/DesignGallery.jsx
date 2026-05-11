import { useState } from "react";
import "./DesignGallery.css";

function DesignGallery() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [originalUrl, setOriginalUrl] = useState(null);
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null);
  const [currentFile, setCurrentFile] = useState(null);
  const [currentImageUrl, setCurrentImageUrl] = useState(null);
  const [generationCount, setGenerationCount] = useState(0);

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setSelectedFile(file);
    setCurrentFile(file);
    setOriginalUrl(URL.createObjectURL(file));
    setCurrentImageUrl(URL.createObjectURL(file));
    setOptions([]);
    setSelectedOption(null);
    setGenerationCount(0);
  };

  const handleGenerateOptions = async () => {
    if (!currentFile) return;

    let fileToSend = currentFile;

    if (options.length > 0 && selectedOption) {
        const imageResponse = await fetch(selectedOption.image_url);
        const blob = await imageResponse.blob();

        fileToSend = new File([blob], "current_image.jpg", {
        type: blob.type || "image/jpeg",
        });

        setCurrentFile(fileToSend);
        setCurrentImageUrl(selectedOption.image_url);
    }

    setOptions([]);
    setSelectedOption(null);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", fileToSend);

    const response = await fetch("http://localhost:8000/design-gallery", {
        method: "POST",
        body: formData,
    });

    const data = await response.json();

    setOptions(data.options);
    setGenerationCount((prev) => prev + 1);
    setLoading(false);
  };

  const handleDownload = async () => {
    if (!currentImageUrl) return;

    const response = await fetch(currentImageUrl);
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

  const gridItems = [...options];

    if (currentImageUrl && options.length > 0) {
    gridItems.splice(7, 0, {
        image_url: currentImageUrl,
        changed_param: "Current Image",
        direction: "",
        isOriginal: true,
    });
    }

  return (
    <main className="main">
        <div className="page-title-row">
        <h2>Design Gallery</h2>

        {generationCount >= 2 && currentImageUrl && (
            <button className="download-button" onClick={handleDownload}>
            Download Enhanced Image
            </button>
        )}
        </div>

        <input type="file" accept="image/*" onChange={handleFileChange} />

        {originalUrl && (
        <>
            <div className="comparison-section">
            <div className="comparison-card">
                <h3>Original Image</h3>
                <img
                src={originalUrl}
                alt="Original"
                className="original-image"
                />
            </div>

            {generationCount >= 2 && currentImageUrl && (
                <div className="comparison-card">
                <h3>Current Image</h3>
                <img
                    src={currentImageUrl}
                    alt="Current"
                    className="original-image"
                />
                </div>
            )}

            {selectedOption && (
                <div className="comparison-card">
                <h3>Selected Image</h3>
                <img
                    src={selectedOption.image_url}
                    alt={selectedOption.changed_param}
                    className="original-image"
                />
                <p>
                    {selectedOption.changed_param}:{" "}
                    {selectedOption.direction > 0 ? "+" : ""}
                    {selectedOption.direction}
                </p>
                </div>
            )}
            </div>

            <div className="center-button-container">
            <button
                className="generate-button"
                onClick={handleGenerateOptions}
                disabled={loading || (options.length > 0 && !selectedOption)}
            >
                {loading
                ? "Generating..."
                : options.length > 0
                ? "Select Enhancement"
                : "Generate Enhancement Options"}
            </button>
            </div>
        </>
        )}

        {loading && (
        <div className="loading-box">
            <div className="spinner"></div>
            <p>Generating enhancement options...</p>
        </div>
        )}

        {gridItems.length > 0 && (
        <div className="design-grid">
            {gridItems.map((item, index) => (
            <div
                key={index}
                className={
                item.isOriginal
                    ? "gallery-card original-grid-card"
                    : selectedOption?.image_url === item.image_url
                    ? "gallery-card selected-gallery-card"
                    : "gallery-card"
                }
                onClick={() => {
                if (!item.isOriginal) {
                    setSelectedOption(item);
                }
                }}
            >
                <img
                src={item.image_url}
                alt={item.changed_param}
                onError={() => {
                    console.log("Image failed to load:", item.image_url);
                }}
                />

                <p>
                {item.isOriginal
                    ? "Current Image"
                    : `${item.changed_param}: ${
                        item.direction > 0 ? "+" : ""
                    }${item.direction}`}
                </p>
            </div>
            ))}
        </div>
        )}
    </main>
    );
}

export default DesignGallery;