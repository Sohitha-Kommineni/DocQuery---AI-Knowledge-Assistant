import { useEffect, useState } from "react";

import { apiFetch } from "../api/client";
import { Table } from "../components/Table";

type DocumentItem = {
  id: number;
  name: string;
  file_type: string;
  uploaded_at: string;
  tags?: string | null;
  access_level: string;
};

export const Documents = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [tags, setTags] = useState("");
  const [accessLevel, setAccessLevel] = useState("public");

  const loadDocuments = () => {
    apiFetch<DocumentItem[]>("/documents")
      .then(setDocuments)
      .catch(() => setDocuments([]));
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const upload = async () => {
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    form.append("tags", tags);
    form.append("access_level", accessLevel);

    const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";
    await fetch(`${baseUrl}/documents/upload`, {
      method: "POST",
      body: form,
      headers: {
        Authorization: `Bearer ${localStorage.getItem("docquery_token") || ""}`
      }
    });
    setFile(null);
    setTags("");
    loadDocuments();
  };

  return (
    <div className="space-y-8">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-700">Upload Document</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <input
            type="file"
            className="rounded border border-slate-200 p-2 text-sm"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
          <input
            type="text"
            placeholder="Tags (HR, Legal, Finance)"
            value={tags}
            onChange={(event) => setTags(event.target.value)}
            className="rounded border border-slate-200 p-2 text-sm"
          />
          <select
            value={accessLevel}
            onChange={(event) => setAccessLevel(event.target.value)}
            className="rounded border border-slate-200 p-2 text-sm"
          >
            <option value="public">Public</option>
            <option value="department">Department</option>
            <option value="admin_only">Admin Only</option>
          </select>
        </div>
        <button
          onClick={upload}
          className="mt-4 rounded-md bg-slate-900 px-4 py-2 text-sm text-white"
        >
          Upload & Ingest
        </button>
      </div>

      <div>
        <h2 className="mb-3 text-sm font-semibold text-slate-700">Documents</h2>
        <Table
          headers={["Name", "Type", "Access", "Tags", "Uploaded"]}
          rows={documents.map((doc) => [
            doc.name,
            doc.file_type,
            doc.access_level,
            doc.tags ?? "--",
            new Date(doc.uploaded_at).toLocaleDateString()
          ])}
        />
      </div>
    </div>
  );
};
