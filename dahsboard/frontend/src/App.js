import Sidebar from "./layout/Sidebar";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <div className="flex-1 overflow-auto bg-[#f4f7fe]">
        <Dashboard />
      </div>
    </div>
  );
}

export default App;