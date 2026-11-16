import type{ButtonHTMLAttributes}from"react";
type Props=ButtonHTMLAttributes<HTMLButtonElement>&{variant?:"primary"|"secondary"|"ghost"|"danger";size?:"sm"|"md"};
export default function Button({variant="secondary",size="md",className="",...props}:Props){return <button className={["hawinet-button","hawinet-button-"+variant,"hawinet-button-"+size,className].filter(Boolean).join(" ")} {...props}/>}