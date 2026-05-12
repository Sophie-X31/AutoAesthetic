import { useState } from "react";
import "./App.css";
import AutomaticEditor from "./AutomaticEditor";
import DesignGallery from "./DesignGallery";
import AutoCulling from "./AutoCulling";

function App() {
  const [activeTab, setActiveTab] = useState(null);

  return (
    <div className="app">
      <header className="header">
        <button
          className="logo-button"
          onClick={() => setActiveTab(null)}
        >
          AutoAesthetic
        </button>
      </header>

      <nav className="tabs">
        <button
          className={activeTab === "auto-culling" ? "tab active" : "tab"}
          onClick={() => setActiveTab("auto-culling")}
        >
          Auto Culling
        </button>

        <button
          className={activeTab === "design-gallery" ? "tab active" : "tab"}
          onClick={() => setActiveTab("design-gallery")}
        >
          Design Gallery
        </button>

        <button
          className={activeTab === "automatic-editor" ? "tab active" : "tab"}
          onClick={() => setActiveTab("automatic-editor")}
        >
          Automatic Editor
        </button>
      </nav>

      {activeTab === null && (
        <main className="main">
          <h2>Welcome to AutoAesthetic!</h2>

          <p>
            AutoAesthetic is an interactive photography assistant designed to help beginner photographers improve both their photo selection and editing workflows. The platform combines machine learning, aesthetic prediction models, and image enhancement techniques to provide users with automated recommendations and visual feedback while they learn photography concepts. By simplifying complex editing and culling tasks, AutoAesthetic helps users focus more on creativity and storytelling rather than technical barriers.
          </p>
          <br></br>
          

          <h3>Auto Culling</h3>
          <p>
            AutoAesthetic is an interactive photography assistant designed to help beginner photographers improve both their photo selection and editing workflows. The platform combines machine learning, aesthetic prediction models, and image enhancement techniques to provide users with automated recommendations and visual feedback while they learn photography concepts. By simplifying complex editing and culling tasks, AutoAesthetic helps users focus more on creativity and storytelling rather than technical barriers.
          </p>

          <h3>Design Gallery</h3>
          <p>
            The Design Gallery provides an interactive editing experience that helps users visually explore how different image adjustments affect the final result. The system generates multiple enhancement variations by independently modifying parameters such as brightness, contrast, saturation, sharpness, shadows, highlights, and temperature. Users can compare these options side-by-side, select preferred edits, and iteratively generate new variations based on their choices. This workflow allows beginners to experiment with editing techniques while developing a better understanding of how specific adjustments influence the aesthetic quality and mood of an image.
          </p>

          <h3>Automatic Editor</h3>
          <p>
            The Automatic Editor streamlines the photo editing process by automatically generating an optimized version of an uploaded image. Using an iterative optimization process, the system evaluates potential edits and progressively adjusts image parameters to maximize the predicted aesthetic quality score. The final enhanced image is displayed alongside the original image, and the recommended editing steps are listed in the order they were applied. While the Design Gallery focuses on interactive learning and exploration, the Automatic Editor prioritizes efficiency by automatically selecting the strongest combination of edits for the user.
          </p>
        </main>
      )}

      {activeTab === "automatic-editor" && <AutomaticEditor />}
      {activeTab === "design-gallery" && <DesignGallery />}
      {activeTab === "auto-culling" && <AutoCulling />}
    </div>
  );
}

export default App;