import { useState } from "react";
import "./App.css";
import AutomaticEditor from "./AutomaticEditor";
import DesignGallery from "./DesignGallery";

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
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod
            tempor incididunt ut labore et dolore magna aliqua.
          </p>
          <br></br>
          

          <h3>Auto Culling</h3>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur nec dolor risus. Vivamus ex tellus, commodo vitae mauris ut,
            posuere imperdiet nibh. Integer nec pellentesque metus. Vivamus consequat massa ex, et sagittis ligula placerat id. Vivamus non 
            vulputate sapien. Quisque aliquet, nisl ac luctus faucibus, diam turpis interdum felis, in egestas velit nulla et justo. Donec sed 
            dignissim tortor. Ut consequat odio risus. Donec eu velit nisl. Fusce tellus ante, elementum non blandit nec, venenatis consectetur 
            elit. Vestibulum non massa erat. Nunc vehicula egestas hendrerit. Quisque vel euismod dolor. Duis tempor augue et velit tempus ullamcorper. 
            Mauris tempor pretium urna, eget laoreet neque dapibus eu.
          </p>

          <h3>Design Gallery</h3>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur nec dolor risus. Vivamus ex tellus, commodo vitae mauris ut,
            posuere imperdiet nibh. Integer nec pellentesque metus. Vivamus consequat massa ex, et sagittis ligula placerat id. Vivamus non 
            vulputate sapien. Quisque aliquet, nisl ac luctus faucibus, diam turpis interdum felis, in egestas velit nulla et justo. Donec sed 
            dignissim tortor. Ut consequat odio risus. Donec eu velit nisl. Fusce tellus ante, elementum non blandit nec, venenatis consectetur 
            elit. Vestibulum non massa erat. Nunc vehicula egestas hendrerit. Quisque vel euismod dolor. Duis tempor augue et velit tempus ullamcorper. 
            Mauris tempor pretium urna, eget laoreet neque dapibus eu.
          </p>

          <h3>Automatic Editor</h3>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur nec dolor risus. Vivamus ex tellus, commodo vitae mauris ut,
            posuere imperdiet nibh. Integer nec pellentesque metus. Vivamus consequat massa ex, et sagittis ligula placerat id. Vivamus non 
            vulputate sapien. Quisque aliquet, nisl ac luctus faucibus, diam turpis interdum felis, in egestas velit nulla et justo. Donec sed 
            dignissim tortor. Ut consequat odio risus. Donec eu velit nisl. Fusce tellus ante, elementum non blandit nec, venenatis consectetur 
            elit. Vestibulum non massa erat. Nunc vehicula egestas hendrerit. Quisque vel euismod dolor. Duis tempor augue et velit tempus ullamcorper. 
            Mauris tempor pretium urna, eget laoreet neque dapibus eu.
          </p>
        </main>
      )}

      {activeTab === "automatic-editor" && <AutomaticEditor />}
      {activeTab === "design-gallery" && <DesignGallery />}
    </div>
  );
}

export default App;