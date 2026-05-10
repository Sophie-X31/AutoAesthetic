export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold tracking-tight">
            AutoAesthetic
          </h1>

          {/* Hamburger Menu */}
          <button className="flex flex-col justify-center gap-1.5 hover:opacity-80 transition-opacity">
            <span className="w-7 h-0.5 bg-white rounded"></span>
            <span className="w-7 h-0.5 bg-white rounded"></span>
            <span className="w-7 h-0.5 bg-white rounded"></span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-12">
        <h2 className="text-4xl font-bold mb-6">
          Welcome
        </h2>

        <div className="space-y-6 text-lg leading-8 text-gray-700">
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
          </p>

          <p>
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </p>

          <p>
            Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris.
          </p>
        </div>
      </main>
    </div>
  );
}
