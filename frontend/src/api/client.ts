const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const tokenStorageKey = "docquery_token";

export const setToken = (token: string) => {
  localStorage.setItem(tokenStorageKey, token);
};

export const getToken = () => localStorage.getItem(tokenStorageKey);

export const apiFetch = async <T>(path: string, options?: RequestInit): Promise<T> => {
  const token = getToken();
  const response = await fetch(`${baseUrl}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options?.headers ?? {})
    }
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  return response.json() as Promise<T>;
};
