import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./layout/Sidebar";
import Dashboard from "./pages/Dashboard";
import Control from "./pages/Control";
// import other pages here if needed

function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen overflow-hidden">
        <Sidebar />
        <div className="flex-1 overflow-auto bg-[#f4f7fe]">
          <Routes>
            <Route path="/" element={<Dashboard />} /> 
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/control" element={<Control />} />
            {/* Add more jsroutes here */}
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;

// import Sidebar from "./layout/Sidebar";
// import Dashboard from "./pages/Dashboard";

// function App() {
//   return (
//     <div className="flex h-screen overflow-hidden">
//       <Sidebar />
//       <div className="flex-1 overflow-auto bg-[#f4f7fe]">
//         <Dashboard />
//       </div>
//     </div>
//   );
// }

// export default App;