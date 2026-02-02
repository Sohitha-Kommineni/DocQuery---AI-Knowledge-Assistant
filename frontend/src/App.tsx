import { Route, Routes } from "react-router-dom";

import { Layout } from "./components/Layout";
import { Analytics } from "./pages/Analytics";
import { Chat } from "./pages/Chat";
import { Dashboard } from "./pages/Dashboard";
import { Documents } from "./pages/Documents";

const App = () => {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </Layout>
  );
};

export default App;
