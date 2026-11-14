import type{InputHTMLAttributes}from"react";
export default function Input(props:InputHTMLAttributes<HTMLInputElement>){return <input className={"hawinet-input "+(props.className??"")} {...props}/>}
