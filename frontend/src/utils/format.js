export const formatCount=value=>Number.isFinite(Number(value))?Number(value).toLocaleString():'—';
export const formatPercent=value=>Number.isFinite(Number(value))?`${(Number(value)*100).toFixed(1)}%`:'—';
export const formatTimestamp=value=>value?new Date(value).toLocaleString():'—';
