import type{ReactNode}from"react";
export default function StatusBadge({children,tone="neutral"}:{children:ReactNode;tone?:"neutral"|"success"|"warning"|"danger"|"info"}){return <span className={"hawinet-status-badge tone-"+tone}>{children}</span>}
