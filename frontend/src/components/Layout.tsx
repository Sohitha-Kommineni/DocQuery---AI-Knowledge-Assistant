import { NavLink } from "react-router-dom";

const navItems = [
  { label: "Dashboard", to: "/" },
  { label: "Documents", to: "/documents" },
  { label: "Ask AI", to: "/chat" },
  { label: "Analytics", to: "/analytics" }
];

export const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="flex">
        <aside className="w-64 bg-white border-r border-slate-200 min-h-screen px-6 py-8">
          <div className="text-lg font-semibold text-slate-900">DocQuery Enterprise</div>
          <p className="text-xs text-slate-500 mt-1">Knowledge Assistant</p>
          <nav className="mt-8 space-y-2">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `block rounded-md px-3 py-2 text-sm ${
                    isActive ? "bg-slate-900 text-white" : "text-slate-600 hover:bg-slate-100"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </aside>
        <main className="flex-1 p-10">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-2xl font-semibold">Enterprise Knowledge Hub</h1>
              <p className="text-sm text-slate-500">
                Secure retrieval and AI insights across trusted documents.
              </p>
            </div>
            <button className="rounded-md bg-slate-900 px-4 py-2 text-sm text-white">
              Ask a Question
            </button>
          </div>
          {children}
        </main>
      </div>
    </div>
  );
};
