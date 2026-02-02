import { useState } from "react";

import { apiFetch } from "../api/client";

type Citation = {
  document_id: number;
  document_name: string;
  snippet: string;
};

type QueryResponse = {
  answer: string;
  citations: Citation[];
  confidence: number;
  response_time_ms: number;
};

export const Chat = () => {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<QueryResponse[]>([]);
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const response = await apiFetch<QueryResponse>("/queries/ask", {
        method: "POST",
        body: JSON.stringify({ question })
      });
      setHistory((prev) => [response, ...prev]);
      setQuestion("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-700">Ask a Question</h2>
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          className="mt-3 w-full rounded border border-slate-200 p-3 text-sm"
          rows={4}
          placeholder="Example: What is the onboarding policy for contractors?"
        />
        <button
          onClick={ask}
          disabled={loading}
          className="mt-4 rounded-md bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-60"
        >
          {loading ? "Thinking..." : "Submit Question"}
        </button>
      </div>

      <div className="space-y-4">
        {history.map((item, idx) => (
          <div key={`${idx}-${item.answer}`} className="rounded-lg border border-slate-200 bg-white p-6">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-700">Answer</p>
              <span className="text-xs text-slate-500">
                {item.response_time_ms}ms · Confidence {Math.round(item.confidence * 100)}%
              </span>
            </div>
            <p className="mt-3 text-sm text-slate-800">{item.answer}</p>
            <div className="mt-4">
              <p className="text-xs font-semibold text-slate-500">Sources</p>
              <ul className="mt-2 space-y-2">
                {item.citations.length === 0 ? (
                  <li className="text-xs text-slate-500">No citations available.</li>
                ) : (
                  item.citations.map((citation) => (
                    <li key={`${citation.document_id}-${citation.snippet}`} className="text-xs text-slate-600">
                      <span className="font-semibold">{citation.document_name}</span> —{" "}
                      <span>{citation.snippet}</span>
                    </li>
                  ))
                )}
              </ul>
            </div>
          </div>
        ))}
        {history.length === 0 ? (
          <div className="rounded-lg border border-dashed border-slate-200 bg-slate-50 p-6 text-sm text-slate-500">
            Ask a question to see citation-backed answers here.
          </div>
        ) : null}
      </div>
    </div>
  );
};
