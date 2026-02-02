import { useEffect, useState } from "react";

import { apiFetch } from "../api/client";
import { Table } from "../components/Table";

type QueryLog = {
  id: number;
  question: string;
  response_time_ms: number;
  confidence: number;
  created_at: string;
};

export const Analytics = () => {
  const [logs, setLogs] = useState<QueryLog[]>([]);

  useEffect(() => {
    apiFetch<QueryLog[]>("/queries")
      .then(setLogs)
      .catch(() => setLogs([]));
  }, []);

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-700">Query History</h2>
        <p className="text-xs text-slate-500 mt-1">
          Review response time, confidence, and usage across recent questions.
        </p>
      </div>

      <Table
        headers={["Question", "Confidence", "Response Time", "Timestamp"]}
        rows={logs.map((log) => [
          log.question,
          `${Math.round(log.confidence * 100)}%`,
          `${log.response_time_ms}ms`,
          new Date(log.created_at).toLocaleString()
        ])}
      />
    </div>
  );
};
