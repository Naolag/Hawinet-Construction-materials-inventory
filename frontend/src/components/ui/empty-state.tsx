import type{ReactNode}from"react";
export default function EmptyState({title,description,action}:{title:string;description?:string;action?:ReactNode}){return <div className="hawinet-empty-state"><strong>{title}</strong>{description&&<p>{description}</p>}{action}</div>}
