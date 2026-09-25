import React from 'react';

export default function MetricCard({icon,label,value,change,tone}){
  return <article className="metric"><div className={`metric-icon ${tone}`}>{icon}</div><span className="metric-label">{label}</span><strong>{value}</strong><small>{change}</small></article>;
}
