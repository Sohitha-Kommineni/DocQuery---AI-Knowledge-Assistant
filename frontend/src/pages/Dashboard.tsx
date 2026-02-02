import { useEffect, useState } from "react";

import { apiFetch } from "../api/client";
import { StatCard } from "../components/StatCard";
import { Table } from "../components/Table";

type AnalyticsOverview = {
  document_count: number;
  query_count: number;
  recent_questions: string[];
  frequent_questions: string[];
  unanswered_questions: string[];
};

export const Dashboard = () => {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);

  useEffect(() => {
    apiFetch<AnalyticsOverview>("/analytics/overview")
      .then(setOverview)
      .catch(() => {
        setOverview({
          document_count: 0,
          query_count: 0,
          recent_questions: [],
          frequent_questions: [],
          unanswered_questions: []
        });
      });
  }, []);

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        <StatCard label="Uploaded Documents" value={overview?.document_count ?? "--"} />
        <StatCard label="Queries This Week" value={overview?.query_count ?? "--"} />
        <StatCard label="Unanswered Questions" value={overview?.unanswered_questions.length ?? "--"} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div>
          <h2 className="mb-3 text-sm font-semibold text-slate-700">Recent Questions</h2>
          <Table
            headers={["Question"]}
            rows={(overview?.recent_questions ?? ["No questions yet"]).map((q) => [q])}
          />
        </div>
        <div>
          <h2 className="mb-3 text-sm font-semibold text-slate-700">Top Questions</h2>
          <Table
            headers={["Question"]}
            rows={(overview?.frequent_questions ?? ["No questions yet"]).map((q) => [q])}
          />
        </div>
      </div>
    </div>
  );
};
