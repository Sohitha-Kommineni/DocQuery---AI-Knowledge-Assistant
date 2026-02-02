export const Table = ({
  headers,
  rows
}: {
  headers: string[];
  rows: Array<Array<string | number>>;
}) => {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
          <tr>
            {headers.map((header) => (
              <th key={header} className="px-4 py-3 font-medium">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {rows.map((row, idx) => (
            <tr key={`${idx}-${row[0]}`} className="text-slate-700">
              {row.map((cell, cellIdx) => (
                <td key={`${idx}-${cellIdx}`} className="px-4 py-3">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
