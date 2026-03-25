import axios from 'axios';

const http = axios.create({
  baseURL: (import.meta as any).env?.VITE_API_BASE ?? '/api',
});

// ── USER ──────────────────────────────────────────────────────────────
export const userApi = {
  getAll: () => http.get('/user').then(r => r.data),
  create: (d: { userid: string; username: string; pwd: string }) => http.post('/user', d),
  update: (id: string, d: { username: string; pwd: string }) => http.put(`/user/${id}`, d),
  remove: (id: string) => http.delete(`/user/${id}`),
};

// ── CUST ──────────────────────────────────────────────────────────────
export const custApi = {
  getAll: () => http.get('/cust').then(r => r.data),
  create: (d: { cust_code: string; cust_name: string; remark: string }) => http.post('/cust', d),
  update: (id: string, d: { cust_name: string; remark: string }) => http.put(`/cust/${id}`, d),
  remove: (id: string) => http.delete(`/cust/${id}`),
};

// ── FACT ──────────────────────────────────────────────────────────────
export const factApi = {
  getAll: () => http.get('/fact').then(r => r.data),
  create: (d: { fact_code: string; fact_name: string; remark: string }) => http.post('/fact', d),
  update: (id: string, d: { fact_name: string; remark: string }) => http.put(`/fact/${id}`, d),
  remove: (id: string) => http.delete(`/fact/${id}`),
};

// ── ITEM ──────────────────────────────────────────────────────────────
export const itemApi = {
  getAll: () => http.get('/item').then(r => r.data),
  create: (d: { item_code: string; item_name: string; fact_code: string }) => http.post('/item', d),
  update: (id: string, d: { item_name: string; fact_code: string }) => http.put(`/item/${id}`, d),
  remove: (id: string) => http.delete(`/item/${id}`),
};
