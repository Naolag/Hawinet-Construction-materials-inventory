import type{ReactNode}from"react";
export default function MetricCard({label,value,note,icon}:{label:string;value:string;note?:string;icon?:ReactNode}){return <div className="hawinet-metric-card">{icon&&<span>{icon}</span>}<small>{label}</small><strong>{value}</strong>{note&&<em>{note}</em>}</div>}
