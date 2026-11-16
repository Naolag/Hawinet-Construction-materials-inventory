import type{ReactNode}from"react";
export default function Dropdown({label,children}:{label:ReactNode;children:ReactNode}){return <details className="hawinet-dropdown"><summary>{label}</summary><div className="hawinet-dropdown-menu">{children}</div></details>}
