"use client";

import * as React from "react"
import { createPortal } from "react-dom"
type Variant = { id: string; values: Record<string,string>; active: boolean }
type Product = { id: string; name: string; brand: string; category: string; qty: number; unit: string; price: number | null; active: boolean; description: string; variants: Variant[] }
type Attr = { name: string; values: string[]; required: boolean }
interface Props { style?: React.CSSProperties; accent?: string; textColor?: string; muted?: string; surface?: string; borderColor?: string; initialScreen?: string; products?: any[] }
const initial: Product[] = [
 {id:"PRD-001",name:"Portland Cement",brand:"Dangote",category:"Cement",qty:248,unit:"bags",price:1250,active:true,description:"General-purpose Portland cement for structural concrete, masonry and construction. Store in a dry, covered area.",variants:[{id:"VAR-001",values:{Grade:"42.5R",Weight:"50 kg"},active:true},{id:"VAR-002",values:{Grade:"32.5R",Weight:"50 kg"},active:true}]},
 {id:"PRD-002",name:"Reinforcement Steel Bar",brand:"Habesha Steel",category:"Steel",qty:120,unit:"pieces",price:1850,active:true,description:"Deformed reinforcement steel for concrete structures.",variants:[{id:"VAR-003",values:{Diameter:"12 mm",Length:"12 m"},active:true},{id:"VAR-004",values:{Diameter:"16 mm",Length:"12 m"},active:false},{id:"VAR-005",values:{Diameter:"20 mm",Length:"12 m"},active:true}]},
 {id:"PRD-003",name:"Interior Emulsion Paint",brand:"Kadisco",category:"Paint",qty:32,unit:"buckets",price:4200,active:true,description:"Water-based interior emulsion paint with a smooth, durable finish.",variants:[{id:"VAR-006",values:{Color:"White",Volume:"20 L"},active:true},{id:"VAR-007",values:{Color:"Ivory",Volume:"20 L"},active:true}]},
 {id:"PRD-004",name:"Binding Wire",brand:"Abyssinia",category:"Steel",qty:45,unit:"kg",price:195,active:true,description:"Annealed binding wire for tying reinforcement.",variants:[]},
 {id:"PRD-005",name:"Common Nails",brand:"EKOS",category:"Hardware",qty:60,unit:"kg",price:210,active:true,description:"General-purpose construction nails.",variants:[{id:"VAR-008",values:{Size:"3 inch"},active:true}]},
 {id:"PRD-006",name:"Ceramic Floor Tile",brand:"Ethiopian Ceramics",category:"Finishes",qty:0,unit:"boxes",price:2850,active:false,description:"Ceramic floor tiles for residential interiors.",variants:[]},
 {id:"PRD-007",name:"PVC Water Pipe",brand:"RAINBOW",category:"Plumbing",qty:80,unit:"pieces",price:680,active:true,description:"Durable PVC pipe for water installations.",variants:[]},
 {id:"PRD-008",name:"Washed Sand",brand:"Local supply",category:"Aggregates",qty:12,unit:"m³",price:3200,active:true,description:"Clean washed sand for concrete and mortar.",variants:[]},
 {id:"PRD-009",name:"Gypsum Board",brand:"Siniat",category:"Finishes",qty:0,unit:"sheets",price:950,active:false,description:"Interior gypsum board for partition walls and ceilings.",variants:[]},
 {id:"PRD-010",name:"Crushed Aggregate",brand:"Local supply",category:"Aggregates",qty:18,unit:"m³",price:3800,active:true,description:"Crushed stone aggregate for concrete applications.",variants:[]}
]
const baseAttrs:Record<string,Attr[]> = {
 Cement:[{name:"Grade",values:["32.5R","42.5R","52.5R"],required:true},{name:"Weight",values:["25 kg","50 kg"],required:true}],
 Steel:[{name:"Diameter",values:["8 mm","10 mm","12 mm","16 mm","20 mm"],required:true},{name:"Length",values:["6 m","12 m"],required:true}],
 Paint:[{name:"Color",values:["White","Ivory","Grey"],required:true},{name:"Volume",values:["4 L","20 L"],required:true}],
 Hardware:[{name:"Size",values:["2 inch","3 inch","4 inch"],required:true}],
 Finishes:[],Plumbing:[],Aggregates:[]
}
const PreviewContext=React.createContext(false)
const money=(v:number|null|undefined)=>v==null?"Not set":"ETB "+v.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2})
const normal=(s:string)=>s.trim().toLowerCase()
function Button({children,onClick,primary=false,danger=false,disabled=false,type="button",style={}}:any){
 const [hover,setHover]=React.useState(false)
 return <button type={type} onClick={onClick} disabled={disabled} onMouseEnter={()=>setHover(true)} onMouseLeave={()=>setHover(false)} style={{font:"inherit",fontSize:12,lineHeight:"20px",padding:"9px 15px",borderRadius:8,border:"1px solid "+(primary?"var(--p-accent)":"var(--p-line)"),background:primary?"var(--p-accent)":hover?"var(--p-bg)":"var(--p-surface)",color:primary?"white":danger?"#1E293B":"var(--p-ink)",cursor:disabled?"not-allowed":"pointer",opacity:disabled?.45:1,whiteSpace:"nowrap",transition:"background .15s, opacity .15s",...style}}>{children}</button>
}
function Badge({active}:any){return <span style={{display:"inline-flex",alignItems:"center",gap:6,padding:"4px 9px",borderRadius:6,fontSize:11,color:active?"#2563EB":"var(--p-muted)",background:active?"rgba(22,152,117,.08)":"var(--p-bg)",whiteSpace:"nowrap"}}><span style={{width:5,height:5,borderRadius:"50%",background:"currentColor"}}/>{active?"Active":"Inactive"}</span>}
function Modal({title,subtitle,children,onClose,nested=false,footer}:any){
 const ref=React.useRef<HTMLDivElement>(null)
 const embedded=React.useContext(PreviewContext)
 React.useEffect(()=>{
  if(embedded)return;
  const previous=document.activeElement as HTMLElement
  const old=document.body.style.overflow;document.body.style.overflow="hidden"
  const timer=setTimeout(()=>ref.current?.focus(),0)
  function key(e:KeyboardEvent){
   const dialogs=document.querySelectorAll('[role="dialog"]');if(dialogs[dialogs.length-1]!==ref.current)return;
   if(e.key==="Escape"){e.preventDefault();e.stopImmediatePropagation();onClose()}
   if(e.key==="Tab"){const els=ref.current?.querySelectorAll<HTMLElement>('button:not(:disabled),input,select,textarea,[tabindex="0"]');if(!els?.length)return;const first=els[0],last=els[els.length-1];if(e.shiftKey&&(document.activeElement===first||document.activeElement===ref.current)){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}
  }
  document.addEventListener("keydown",key,true)
  return()=>{clearTimeout(timer);document.body.style.overflow=old;document.removeEventListener("keydown",key,true);previous?.focus()}
 },[onClose])
 if(typeof document==="undefined")return null
 const modalContent=<div onMouseDown={e=>{if(e.target===e.currentTarget)onClose()}} style={{position:embedded?"absolute":"fixed",inset:0,zIndex:nested?10002:10000,background:"rgba(24,35,56,.4)",display:"flex",alignItems:embedded?"flex-start":"center",justifyContent:"center",padding:embedded?"24px 16px":16,fontFamily:'"Varela Round",sans-serif',color:"var(--p-ink,#1E293B)",fontSize:13,...themeFallback}}>
 <div ref={ref} tabIndex={-1} role="dialog" aria-modal="true" aria-label={title} style={{width:"100%",maxWidth:nested?440:580,maxHeight:"90dvh",background:"var(--p-surface)",borderRadius:16,border:"1px solid var(--p-line)",boxShadow:"0 24px 80px rgba(24,35,56,.18)",overflow:"auto",outline:"none"}}>
  <div style={{display:"flex",gap:16,justifyContent:"space-between",alignItems:"start",padding:24,borderBottom:"1px solid var(--p-line)"}}><div><h2 style={{fontSize:20,fontWeight:400,margin:"0 0 6px"}}>{title}</h2><p style={{color:"var(--p-muted)",fontSize:12,lineHeight:1.6,margin:0}}>{subtitle}</p></div><Button onClick={onClose} style={{padding:"5px 10px"}}>Close</Button></div>
  <div style={{padding:24,display:"flex",flexDirection:"column",gap:18}}>{children}</div>
  {footer&&<div style={{padding:"16px 24px",borderTop:"1px solid var(--p-line)",display:"flex",justifyContent:"flex-end",gap:10,flexWrap:"wrap"}}>{footer}</div>}
 </div></div>
 return embedded?modalContent:createPortal(modalContent,document.body)
}
const themeFallback:any={"--p-bg":"#F8FAFC","--p-surface":"#FFFFFF","--p-ink":"#1E293B","--p-muted":"#64748B","--p-line":"#E2E8F0","--p-accent":"#2563EB"}
const inputStyle:React.CSSProperties={font:"inherit",fontSize:13,width:"100%",minWidth:0,border:"1px solid var(--p-line)",borderRadius:8,padding:"11px 12px",background:"var(--p-surface)",color:"var(--p-ink)",outlineOffset:2,boxSizing:"border-box"}
function Field({label,error,hint,children}:any){return <label style={{display:"flex",flexDirection:"column",gap:8,fontSize:12}}><span>{label}</span>{children}{error?<span role="alert" style={{color:"#1E293B",fontSize:11}}>{error}</span>:hint?<span style={{color:"var(--p-muted)",fontSize:11,lineHeight:1.6}}>{hint}</span>:null}</label>}
function Empty({title,description,action}:any){return <div style={{padding:"64px 24px",textAlign:"center",display:"flex",flexDirection:"column",alignItems:"center",gap:12}}><div style={{width:44,height:44,borderRadius:12,background:"var(--p-bg)",border:"1px solid var(--p-line)",display:"grid",placeItems:"center",color:"var(--p-muted)",fontSize:18}}>P</div><h3 style={{margin:0,fontWeight:400,fontSize:17}}>{title}</h3><p style={{margin:0,color:"var(--p-muted)",fontSize:12,lineHeight:1.7,maxWidth:310}}>{description}</p>{action}</div>}
function ProductForm({product,onSave,onClose,categories,products=[]}:any){
 const [form,setForm]=React.useState({name:product?.name||"",category:product?.category||"",brand:product?.brand||"",description:product?.description||"",withVariants:false})
 const [errors,setErrors]=React.useState<any>({})
 const update=(key:string,value:any)=>setForm(f=>({...f,[key]:value}))
 const save=()=>{const e:any={};if(!form.name.trim())e.name="Enter a product name.";else if(products.some((p:Product)=>p.id!==product?.id&&normal(p.name)===normal(form.name)))e.name="A product with this name already exists.";if(!form.category)e.category="Choose a category.";setErrors(e);if(!Object.keys(e).length)onSave({...form,name:form.name.trim(),brand:form.brand.trim(),description:form.description.trim()})}
 return <Modal title={product?"Edit Product":"Add Product"} subtitle="Define the parent product. Stock is managed separately." onClose={onClose} footer={<><Button onClick={onClose}>Cancel</Button><Button primary onClick={save}>{product?"Save Changes":"Add Product"}</Button></>}>
 <Field label="Product Name *" error={errors.name}><input style={{...inputStyle,borderColor:errors.name?"#1E293B":"var(--p-line)"}} value={form.name} onChange={e=>{update("name",e.target.value);setErrors((x:any)=>({...x,name:""}))}} placeholder="e.g. Portland Cement" aria-required="true" aria-invalid={!!errors.name}/></Field>
 <Field label="Category *" error={errors.category} hint={product?.variants?.length?"Category is locked because this product already has variants.":undefined}><select disabled={!!product?.variants?.length} style={{...inputStyle,borderColor:errors.category?"#1E293B":"var(--p-line)",opacity:product?.variants?.length ? 0.6 : 1,cursor:product?.variants?.length?"not-allowed":"pointer"}} value={form.category} onChange={e=>{update("category",e.target.value);setErrors((x:any)=>({...x,category:""}))}} aria-required="true" aria-invalid={!!errors.category}><option value="">Select a category</option>{categories.map((c:string)=><option key={c}>{c}</option>)}</select></Field>
 <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(190px,1fr))",gap:16}}><Field label="Brand (optional)"><input style={inputStyle} value={form.brand} onChange={e=>update("brand",e.target.value)} placeholder="e.g. Dangote"/></Field></div>
 <Field label="Description (optional)"><textarea style={{...inputStyle,minHeight:90,resize:"vertical"}} value={form.description} onChange={e=>update("description",e.target.value)} placeholder="Add useful product information…"/></Field>
 {!product&&<label style={{display:"flex",gap:10,alignItems:"start",padding:14,borderRadius:10,background:"var(--p-bg)",fontSize:12,lineHeight:1.6}}><input type="checkbox" checked={form.withVariants} onChange={e=>update("withVariants",e.target.checked)} style={{accentColor:"var(--p-accent)",marginTop:3}}/><span>Add variants after creating this product<span style={{display:"block",color:"var(--p-muted)",fontSize:11}}>Optional. You can also add variants later.</span></span></label>}
 </Modal>
}
function VariantForm({product,variant,attrs,onCreateAttribute,onSave,onClose}:any){
 const [values,setValues]=React.useState<Record<string,string>>({...variant?.values})
 const [active,setActive]=React.useState(variant?.active??true)
 const [error,setError]=React.useState("")
 const save=()=>{if(!attrs.length){setError("Create at least one category attribute first.");return}if(attrs.some((a:Attr)=>a.required&&!values[a.name])){setError("Complete all required attributes.");return}
 if(!Object.values(values).some(Boolean)){setError("Select at least one attribute value.");return}
 const signature=(x:any)=>Object.entries(x).filter(([,v])=>!!v).sort(([a],[b])=>a.localeCompare(b)).map(([k,v])=>normal(k)+"="+normal(String(v))).join("|")
 if(product.variants.some((v:Variant)=>v.id!==variant?.id&&signature(v.values)===signature(values))){setError("This combination already exists. Choose different attribute values.");return}
 onSave({values,active})}
 return <Modal title={variant?"Edit Variant":"Add Variant"} subtitle={product.name+" · "+product.brand+" · "+product.category} onClose={onClose} footer={<><Button onClick={onClose}>Cancel</Button><Button primary onClick={save}>{variant?"Save Changes":"Add Variant"}</Button></>}>
 <div style={{fontSize:12,color:"var(--p-muted)",lineHeight:1.7}}>Attributes are configured for the {product.category.toLowerCase()} category. The variant is identified automatically by its selected values.</div>
 {attrs.map((a:Attr)=><Field key={a.name} label={a.name+(a.required?" *":" (optional)")}><select style={inputStyle} value={values[a.name]||""} onChange={e=>{setValues(v=>({...v,[a.name]:e.target.value}));setError("")}}><option value="">Select {a.name.toLowerCase()}</option>{a.values.map(v=><option key={v}>{v}</option>)}</select></Field>)}
 <Button onClick={onCreateAttribute} style={{alignSelf:"start",color:"var(--p-accent)"}}>+ Create Attribute</Button>
 {variant&&<Field label="Status"><select style={inputStyle} value={active?"Active":"Inactive"} onChange={e=>setActive(e.target.value==="Active")}><option>Active</option><option>Inactive</option></select></Field>}
 {error&&<div role="alert" style={{padding:12,borderRadius:8,background:"#EFF6FF",color:"#1E293B",fontSize:12,lineHeight:1.6}}>{error}</div>}
 </Modal>
}
function AttributeForm({attrs,onSave,onClose}:any){
 const [name,setName]=React.useState(""),[values,setValues]=React.useState(""),[error,setError]=React.useState("")
 function save(){const parts=values.split(/[,\n]/).map(s=>s.trim()).filter(Boolean);if(!name.trim()||!parts.length){setError("Attribute name and at least one value are required.");return}if(new Set(parts.map(normal)).size!==parts.length){setError("Remove duplicate attribute values.");return}const existing=attrs.find((a:Attr)=>normal(a.name)===normal(name));const merged=existing?[...existing.values,...parts.filter((part:string)=>!existing.values.some(value=>normal(value)===normal(part)))]:parts;if(existing&&merged.length===existing.values.length){setError("Those values already exist for this attribute.");return}onSave({name:existing?.name||name.trim(),values:merged,required:existing?.required??false})}
 return <Modal title="Create Attribute" subtitle="Add an optional attribute to this product’s category." onClose={onClose} nested footer={<><Button onClick={onClose}>Cancel</Button><Button primary onClick={save}>Create Attribute</Button></>}>
 <Field label="Attribute Name *"><input style={{...inputStyle,borderColor:error?"#1E293B":"var(--p-line)"}} value={name} onChange={e=>{setName(e.target.value);setError("")}} placeholder="e.g. Finish"/></Field>
 <Field label="Attribute Values *" hint="Separate values with commas or put each value on a new line."><textarea style={{...inputStyle,minHeight:100}} value={values} onChange={e=>{setValues(e.target.value);setError("")}} placeholder="Matte, Satin, Gloss"/></Field>
 {values.trim()&&<div style={{display:"flex",gap:6,flexWrap:"wrap"}}>{values.split(/[,\n]/).map(s=>s.trim()).filter(Boolean).map((s,i)=><span key={i} style={{padding:"5px 9px",background:"var(--p-bg)",borderRadius:6,fontSize:11}}>{s}</span>)}</div>}
 {error&&<p role="alert" style={{margin:0,color:"#1E293B",fontSize:12,lineHeight:1.6}}>{error}</p>}
 </Modal>
}

/**
 * @framerSupportedLayoutWidth any
 * @framerSupportedLayoutHeight auto
 */
export default function ProductsWorkspace(props:Props){
 const {initialScreen="Products"}=props
 const root=React.useRef<HTMLDivElement>(null)
 const [width,setWidth]=React.useState(928)
 const [products,setProducts]=React.useState<Product[]>(()=>props.products?.length?props.products.map((p,i)=>({...initial[i%initial.length],...p,id:p.id||"PRD-"+(i+1),variants:initial[i%initial.length].variants})):initial)
 const [attrs,setAttrs]=React.useState(baseAttrs)
 const [query,setQuery]=React.useState(""),[category,setCategory]=React.useState("All categories")
 const [page,setPage]=React.useState(1)
 const [selected,setSelected]=React.useState<string|null>(initialScreen==="Products"?null:initialScreen==="No Variants"||initialScreen==="Delete Confirmation"?"PRD-006":"PRD-001")
 const [view,setView]=React.useState(initialScreen==="Product Variants"||initialScreen==="Add Variant"||initialScreen==="Edit Variant"||initialScreen==="Create Attribute"||initialScreen==="No Variants"?"variants":"products")
 const [dialog,setDialog]=React.useState<string|null>(initialScreen==="Add Product"?"add":initialScreen==="Product Details"?"details":initialScreen==="Edit Product"?"edit":["Add Variant","Edit Variant","Create Attribute"].includes(initialScreen)?"variant":initialScreen==="Delete Confirmation"?"delete":null)
 const [variantId,setVariantId]=React.useState<string|null>(initialScreen==="Edit Variant"?"VAR-001":null)
 const [attributeOpen,setAttributeOpen]=React.useState(initialScreen==="Create Attribute")
 const [menu,setMenu]=React.useState<string|null>(null),[toast,setToast]=React.useState("")
 const [variantQuery,setVariantQuery]=React.useState(""),[variantStatus,setVariantStatus]=React.useState("All statuses")
 const [demoState,setDemoState]=React.useState(initialScreen==="Loading"?"Loading":initialScreen==="Empty Products"?"Empty":initialScreen==="No Results"?"No results":"Default")
 React.useEffect(()=>{if(!root.current)return;const observer=new ResizeObserver(entries=>setWidth(entries[0].contentRect.width));observer.observe(root.current);return()=>observer.disconnect()},[])
 React.useEffect(()=>{if(!toast)return;const timer=setTimeout(()=>setToast(""),4500);return()=>clearTimeout(timer)},[toast])
 const product=products.find(p=>p.id===selected)||products[0]
 const filtered=products.filter(p=>p.active&&(p.name+" "+p.brand).toLowerCase().includes(query.trim().toLowerCase())&&(category==="All categories"||p.category===category))
 const display=demoState==="Empty"||demoState==="No results"?[]:filtered
 const categories=Object.keys(attrs)
 const narrow=width<570
 const pageSize=narrow?4:7
 const pageCount=Math.max(1,Math.ceil(display.length/pageSize)),currentPage=Math.min(page,pageCount)
 const visible=display.slice((currentPage-1)*pageSize,currentPage*pageSize)
 const rowStyle:React.CSSProperties={padding:"18px 14px",borderBottom:"1px solid var(--p-line)",textAlign:"left",verticalAlign:"middle",fontWeight:400,fontSize:12}
 const panel:React.CSSProperties={background:"var(--p-surface)",border:"1px solid var(--p-line)",borderRadius:14,overflow:"hidden"}
 const select=(value:string,onChange:any,options:string[],label:string)=><select aria-label={label} value={value} onChange={onChange} style={{...inputStyle,width:"auto",minWidth:140,padding:"10px 12px",fontSize:12}}>{options.map(v=><option key={v}>{v}</option>)}</select>
 const notify=(s:string)=>setToast(s)
 const clear=()=>{setQuery("");setCategory("All categories");setPage(1);setDemoState("Default")}
 const open=(type:string,p:Product)=>{setSelected(p.id);setDialog(type);setMenu(null)}
 const toggle=(p:Product)=>{setProducts(old=>old.map(x=>x.id===p.id?{...x,active:!x.active}:x));setMenu(null);notify(p.name+(!p.active?" activated.":" deactivated."))}
 const variants=(p:Product)=>{setSelected(p.id);setView("variants");setDialog(null);setMenu(null);setVariantQuery("");setVariantStatus("All statuses")}
 const close=React.useCallback(()=>setDialog(null),[])
 const closeAttribute=React.useCallback(()=>setAttributeOpen(false),[])
 const v=product?.variants.find(v=>v.id===variantId)
 const listVariants=(product?.variants||[]).filter(v=>Object.values(v.values).join(" ").toLowerCase().includes(variantQuery.toLowerCase())&&(variantStatus==="All statuses"||(variantStatus==="Active")===v.active))
 const theme:any={"--p-bg":"#F8FAFC","--p-surface":props.surface||"#FFFFFF","--p-ink":props.textColor||"#1E293B","--p-muted":props.muted||"#64748B","--p-line":props.borderColor||"#E2E8F0","--p-accent":props.accent||"#2563EB"}
 return <PreviewContext.Provider value={initialScreen!=="Products"}><div ref={root} style={{...theme,position:"relative",fontFamily:'"Varela Round",sans-serif',fontSize:13,color:"var(--p-ink)",width:"100%",boxSizing:"border-box",minHeight:800,...props.style}}>
 <div style={{display:"flex",flexDirection:"column",gap:24}}>
 {view==="products"?<>
 <header style={{display:"flex",justifyContent:"space-between",gap:20,alignItems:narrow?"start":"center",flexWrap:"wrap"}}><div><h1 style={{fontSize:28,fontWeight:400,margin:"0 0 10px"}}>Products</h1><p style={{fontSize:12,color:"var(--p-muted)",margin:0,lineHeight:1.7}}>Manage your construction materials and product variants.</p></div><Button primary onClick={()=>{setDialog("add");setSelected(null)}}>Add Product</Button></header>
 <section aria-label="Product summary" style={{display:"grid",gridTemplateColumns:"1fr",gap:12}}>
 {[["Total Products",products.filter(p=>p.active).length,"Active parent products in your catalog"]].map(([label,value,note])=><div key={label} style={{...panel,padding:narrow?14:20,display:"flex",flexDirection:"row",alignItems:"center",justifyContent:"space-between",gap:12}}><span style={{fontSize:12,color:"var(--p-muted)"}}>{label}</span><span style={{fontSize:28,color:"var(--p-accent)"}}>{demoState==="Empty"?0:value}</span><span style={{fontSize:11,color:"var(--p-muted)",display:narrow?"none":"block"}}>{note}</span></div>)}
 </section>
 <section style={panel} aria-label="Product catalog">
 
 <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",gap:12,padding:narrow?"16px 14px 12px":"20px 20px 16px",flexWrap:"wrap"}}><div><h2 style={{fontWeight:400,fontSize:17,margin:0}}>Product catalog <span style={{marginLeft:8,fontSize:11,padding:"4px 8px",background:"var(--p-bg)",borderRadius:6,color:"var(--p-muted)"}}>{demoState==="Empty"?0:products.filter(p=>p.active).length}</span></h2><p style={{fontSize:11,color:"var(--p-muted)",margin:"8px 0 0"}}>Parent products only. Manage variants from each product.</p></div><span style={{fontSize:10,color:"var(--p-muted)",border:"1px solid var(--p-line)",padding:"5px 8px",borderRadius:5}}>SAMPLE DATA</span></div>
 <div style={{padding:narrow?"0 14px 14px":"0 20px 20px",display:"flex",flexDirection:narrow?"column":"row",gap:10,flexWrap:"wrap"}}><input aria-label="Search products" placeholder="Search products or brands…" value={query} onChange={e=>{setQuery(e.target.value);setPage(1)}} style={{...inputStyle,flex:narrow?"1 1 auto":"1 1 210px",width:narrow?"100%":"auto",fontSize:12}}/>{select(category,(e:any)=>{setCategory(e.target.value);setPage(1)},["All categories",...categories],"Category")}<Button onClick={clear} style={{color:"var(--p-accent)",borderColor:"transparent"}}>Clear filters</Button></div>
 {(query||category!=="All categories")&&<p aria-live="polite" style={{padding:"0 20px",fontSize:11,color:"var(--p-muted)"}}>{display.length} matching products</p>}
 {demoState==="Loading"?<div role="status" style={{padding:30}}><p style={{color:"var(--p-muted)"}}>Loading products…</p>{[0,1,2,3,4].map(i=><div key={i} style={{height:36,background:"var(--p-bg)",borderRadius:6,marginBottom:12}}/>)}</div>:!display.length?<Empty title={demoState==="Empty"||!products.length?"No products yet":"No products found"} description={demoState==="Empty"||!products.length?"Create your first parent product to start organizing your catalog.":"Try a different search term or clear the filters."} action={<Button primary onClick={demoState==="Empty"||!products.length?()=>setDialog("add"):clear}>{demoState==="Empty"||!products.length?"Add Product":"Clear filters"}</Button>}/>:narrow?<div style={{display:"flex",flexDirection:"column",gap:10,padding:"0 12px 12px"}}>{visible.map(p=><article key={p.id} style={{border:"1px solid var(--p-line)",borderRadius:12,padding:14,background:"var(--p-surface)",display:"flex",flexDirection:"column",gap:12}}><div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",gap:10}}><div style={{minWidth:0}}><button onClick={()=>open("details",p)} style={{font:"inherit",fontSize:14,fontWeight:600,background:"none",border:0,padding:0,color:"var(--p-ink)",cursor:"pointer",textAlign:"left",lineHeight:1.4}}>{p.name}</button><div style={{fontSize:11,color:"var(--p-muted)",marginTop:4}}>{p.brand||"No brand specified"}</div></div><span style={{fontSize:10,padding:"5px 8px",border:"1px solid var(--p-line)",borderRadius:6,whiteSpace:"nowrap",color:"var(--p-muted)"}}>{p.category}</span></div><div style={{display:"flex",gap:8,alignItems:"center",flexWrap:"wrap"}}>{p.variants.length>0&&<Button onClick={()=>variants(p)} style={{flex:1,padding:"9px 8px",fontSize:11,color:"var(--p-accent)"}}>View Variants</Button>}<Button onClick={()=>open("details",p)} style={{flex:1,padding:"9px 8px",fontSize:11}}>View Details</Button><Button onClick={()=>setMenu(menu===p.id?null:p.id)} style={{padding:"9px 12px",fontSize:11}} aria-label={"Actions for "+p.name}>•••</Button></div>{menu===p.id&&<div role="menu" style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:6,padding:8,border:"1px solid var(--p-line)",borderRadius:8,background:"var(--p-bg)"}}>{[["Edit Product",()=>open("edit",p)],[p.active?"Deactivate":"Activate",()=>toggle(p)],["Delete",()=>open("delete",p)]].map(([label,fn]:any)=><Button key={label} onClick={fn} style={{fontSize:11,padding:"8px 6px",borderColor:"transparent",color:label==="Delete"?"#1E293B":undefined}}>{label}</Button>)}</div>}</article>)}</div>:<div style={{overflowX:"auto"}}><table style={{width:"100%",borderCollapse:"collapse",minWidth:820}}><thead><tr style={{background:"var(--p-bg)",color:"var(--p-muted)"}}>{["Product","Category","Actions"].map(h=><th key={h} scope="col" style={{...rowStyle,fontSize:10,padding:"13px 14px",whiteSpace:"nowrap"}}>{h}</th>)}</tr></thead><tbody>{visible.map(p=><tr key={p.id}><td style={{...rowStyle,minWidth:180}}><button onClick={()=>open("details",p)} style={{font:"inherit",background:"none",border:0,padding:0,color:"var(--p-ink)",cursor:"pointer",textAlign:"left",lineHeight:1.5}}>{p.name}</button><div style={{fontSize:10,color:"var(--p-muted)",marginTop:5}}>{p.brand||"No brand specified"}</div></td><td style={rowStyle}><span style={{fontSize:10,padding:"4px 7px",border:"1px solid var(--p-line)",borderRadius:5,whiteSpace:"nowrap"}}>{p.category}</span></td><td style={{...rowStyle,minWidth:150}}><div style={{display:"flex",gap:6,alignItems:"center"}}>{p.variants.length>0&&<Button onClick={()=>variants(p)} style={{padding:"5px 8px",fontSize:10,color:"var(--p-accent)"}}>View Variants</Button>}<Button onClick={()=>setMenu(menu===p.id?null:p.id)} style={{padding:"5px 8px",fontSize:10}} aria-label={"Actions for "+p.name}>Actions</Button></div>{menu===p.id&&<div role="menu" style={{marginTop:8,padding:6,border:"1px solid var(--p-line)",borderRadius:8,background:"var(--p-surface)",display:"flex",flexDirection:"column",gap:4}}>{[["View Details",()=>open("details",p)],["Edit Product",()=>open("edit",p)],[p.active?"Deactivate":"Activate",()=>toggle(p)],["Delete",()=>open("delete",p)]].map(([label,fn]:any)=><Button key={label} onClick={fn} style={{fontSize:11,padding:"5px 8px",textAlign:"left",borderColor:"transparent",color:label==="Delete"?"#1E293B":undefined}}>{label}</Button>)}</div>}</td></tr>)}</tbody></table></div>}<footer style={{padding:narrow?"14px 16px":"16px 20px",display:"flex",justifyContent:"space-between",gap:12,alignItems:"center",flexWrap:"wrap"}}><span style={{fontSize:11,color:"var(--p-muted)"}}>{display.length?"Showing "+((currentPage-1)*pageSize+1)+"–"+Math.min(currentPage*pageSize,display.length)+" of "+display.length+" products":"0 products"}</span><div style={{display:"flex",alignItems:"center",gap:8}}><Button disabled={currentPage===1} onClick={()=>setPage(p=>p-1)}>Previous</Button><span style={{fontSize:11,color:"var(--p-muted)"}}>{currentPage} / {pageCount}</span><Button disabled={currentPage>=pageCount} onClick={()=>setPage(p=>p+1)}>Next</Button></div></footer>
 </section>
 <div style={{display:"flex",justifyContent:"space-between",gap:12,alignItems:"center",flexWrap:"wrap",color:"var(--p-muted)",fontSize:11}}><span>Prototype only · Changes reset when the page reloads.</span><label style={{display:"flex",gap:8,alignItems:"center"}}>Preview state{select(demoState,(e:any)=>setDemoState(e.target.value),["Default","Loading","Empty","No results"],"Preview table state")}</label></div>
 </>:product&&<>
 <div><Button onClick={()=>{setView("products");setDialog(null)}}>Back to Products</Button></div>
 <header style={{display:"flex",justifyContent:"space-between",gap:16,alignItems:"center",flexWrap:"wrap"}}><div><h1 style={{margin:"0 0 10px",fontSize:28,fontWeight:400}}>Product Variants</h1><p style={{margin:0,color:"var(--p-muted)",fontSize:12}}>Manage attribute combinations for this parent product.</p></div><Button primary onClick={()=>{setVariantId(null);setDialog("variant")}}>Add Variant</Button></header>
 <div style={{...panel,padding:24,display:"flex",justifyContent:"space-between",gap:16,flexWrap:"wrap"}}><div><span style={{color:"var(--p-muted)",fontSize:10}}>PARENT PRODUCT · {product.id}</span><h2 style={{fontSize:18,fontWeight:400,margin:"10px 0"}}>{product.name}</h2><p style={{fontSize:12,color:"var(--p-muted)",margin:0}}>{product.brand||"No brand"} · {product.category} · {money(product.price)}</p></div><div style={{display:"flex",alignItems:"center",gap:12}}><Badge active={product.active}/><Button onClick={()=>setDialog("details")}>Product Details</Button></div></div>
 <section style={panel}><div style={{padding:20,display:"flex",gap:10,flexWrap:"wrap"}}><input aria-label="Search variants" style={{...inputStyle,flex:"1 1 220px",width:"auto"}} placeholder="Search attribute values…" value={variantQuery} onChange={e=>setVariantQuery(e.target.value)}/>{select(variantStatus,(e:any)=>setVariantStatus(e.target.value),["All statuses","Active","Inactive"],"Variant status")}</div>
 {!listVariants.length?<Empty title={product.variants.length?"No matching variants":"No variants available"} description={product.variants.length?"Try another attribute value or status.":"Add attribute combinations to create this product’s first variant."} action={<Button primary onClick={()=>{setVariantId(null);setDialog("variant")}}>Add Variant</Button>}/>:<div style={{overflowX:"auto"}}><table style={{width:"100%",borderCollapse:"collapse",minWidth:500}}><thead><tr style={{background:"var(--p-bg)",color:"var(--p-muted)"}}>{["Variant attributes","Status","Actions"].map(h=><th key={h} style={rowStyle}>{h}</th>)}</tr></thead><tbody>{listVariants.map(v=><tr key={v.id}><td style={rowStyle}><div style={{display:"flex",gap:8,flexWrap:"wrap"}}>{Object.entries(v.values).filter(([,value])=>value).map(([k,value])=><span key={k} style={{background:"var(--p-bg)",padding:"5px 8px",borderRadius:5,fontSize:11}}><span style={{color:"var(--p-muted)"}}>{k}: </span>{value}</span>)}</div><div style={{fontSize:10,color:"var(--p-muted)",marginTop:8}}>{v.id}</div></td><td style={rowStyle}><Badge active={v.active}/></td><td style={rowStyle}><div style={{display:"flex",gap:6,flexWrap:"wrap"}}><Button onClick={()=>{setVariantId(v.id);setDialog("variantDetails")}}>View Details</Button><Button onClick={()=>{setVariantId(v.id);setDialog("variant")}}>Edit</Button><Button onClick={()=>{setProducts(ps=>ps.map(p=>p.id===product.id?{...p,variants:p.variants.map(x=>x.id===v.id?{...x,active:!x.active}:x)}:p));notify("Variant status updated.")}}>{v.active?"Deactivate":"Activate"}</Button></div></td></tr>)}</tbody></table></div>}
 <div style={{padding:20,color:"var(--p-muted)",fontSize:11}}>{listVariants.length} variants · Never listed as separate parent products</div></section>
 </>}
 </div>
 {(dialog==="add"||dialog==="edit")&&<ProductForm key={dialog+(selected||"")} product={dialog==="edit"?product:null} products={products} categories={categories} onClose={close} onSave={(f:any)=>{if(dialog==="edit"){setProducts(ps=>ps.map(p=>p.id===product.id?{...p,...f,name:f.name.trim(),price:null}:p));notify("Product updated.");setDialog(null)}else{const id="PRD-"+String(Date.now()).slice(-6);setProducts(ps=>[{id,name:f.name.trim(),category:f.category,brand:f.brand.trim(),price:null,description:f.description,qty:0,unit:({Cement:"bags",Steel:"pieces",Paint:"buckets",Hardware:"kg",Finishes:"boxes",Plumbing:"pieces",Aggregates:"m³"} as any)[f.category],active:true,variants:[]},...ps]);setSelected(id);setDemoState("Default");setDialog(null);notify("Product created.");if(f.withVariants){setView("variants");setVariantId(null);setDialog("variant")}}}}/>}
 {dialog==="details"&&product&&<Modal title="Product Details" subtitle={product.id+" · Parent product"} onClose={close} footer={<><Button onClick={()=>setDialog("edit")}>Edit Product</Button><Button primary onClick={()=>{if(product.variants.length)variants(product);else{setVariantId(null);setDialog("variant")}}}>{product.variants.length?"Manage Variants":"Add Variant"}</Button></>}>
 <div style={{display:"flex",justifyContent:"space-between",alignItems:"start",gap:12}}><h3 style={{fontSize:22,fontWeight:400,margin:0}}>{product.name}</h3><Badge active={product.active}/></div>
 <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:20}}>{[["Brand",product.brand||"Not specified"],["Category",product.category]].map(([k,value])=><div key={k}><span style={{fontSize:11,color:"var(--p-muted)",display:"block",marginBottom:8}}>{k}</span><span>{value}</span></div>)}</div>
 <div><p style={{fontSize:11,color:"var(--p-muted)",margin:"0 0 8px"}}>Description</p><p style={{margin:0,lineHeight:1.8,fontSize:13}}>{product.description||"No description added."}</p></div>
 <div style={{padding:16,borderRadius:10,background:"var(--p-bg)",fontSize:12,lineHeight:1.7}}>{product.variants.length} configured variants. Parent product information is shared across all variants.</div>
 <div style={{display:"flex",gap:10,flexWrap:"wrap"}}><Button onClick={()=>toggle(product)}>{product.active?"Deactivate Product":"Activate Product"}</Button><Button danger onClick={()=>setDialog("delete")}>Delete Product</Button></div>
 </Modal>}
 {dialog==="variant"&&product&&<VariantForm key={product.id+(variantId||"new")} product={product} variant={v} attrs={attrs[product.category]||[]} onCreateAttribute={()=>setAttributeOpen(true)} onClose={close} onSave={(data:any)=>{setProducts(ps=>ps.map(p=>p.id===product.id?{...p,variants:variantId?p.variants.map(x=>x.id===variantId?{...x,...data}:x):[...p.variants,{id:"VAR-"+String(Date.now()).slice(-6),...data}]}:p));setDialog(null);setView("variants");notify(variantId?"Variant updated.":"Variant created.")}}/>}
 {attributeOpen&&product&&<AttributeForm attrs={attrs[product.category]||[]} onClose={closeAttribute} onSave={(a:Attr)=>{setAttrs(old=>({...old,[product.category]:old[product.category]?.some(existing=>normal(existing.name)===normal(a.name))?old[product.category].map(existing=>normal(existing.name)===normal(a.name)?{...existing,values:a.values}:existing):[...(old[product.category]||[]),a]}));setAttributeOpen(false);notify("Attribute values saved. Your variant selections are preserved.")}}/>}
 {dialog==="variantDetails"&&product&&v&&<Modal title="Variant Details" subtitle={product.name+" · "+v.id} onClose={close} footer={<Button primary onClick={()=>setDialog("variant")}>Edit Variant</Button>}><Badge active={v.active}/>{Object.entries(v.values).map(([key,value])=><div key={key} style={{display:"flex",justifyContent:"space-between",padding:"10px 0",borderBottom:"1px solid var(--p-line)"}}><span style={{color:"var(--p-muted)"}}>{key}</span><span>{value}</span></div>)}</Modal>}
 {dialog==="delete"&&product&&<Modal title={product.qty>0?"Product cannot be deleted":"Delete Product?"} subtitle={product.name} onClose={close} footer={<><Button onClick={close}>Cancel</Button>{product.qty===0&&<Button danger onClick={()=>{setProducts(ps=>ps.filter(p=>p.id!==product.id));setDialog(null);setView("products");notify("Product deleted.")}}>Delete Product</Button>}</>}>
 <p style={{margin:0,lineHeight:1.8,color:"var(--p-muted)"}}>{product.qty>0?"This sample product has available stock. Deactivate it instead to preserve inventory information.":"This removes the parent product and its variants from this prototype. This action cannot be undone."}</p>
 {product.qty>0&&<Button onClick={()=>{if(product.active)toggle(product);setDialog(null)}}>Deactivate Product</Button>}
 </Modal>}
 {toast&&typeof document!=="undefined"&&createPortal(<div role="status" style={{position:"fixed",bottom:24,right:20,left:20,marginLeft:"auto",width:"fit-content",maxWidth:420,zIndex:10005,padding:"14px 18px",borderRadius:10,border:"1px solid #E2E8F0",boxShadow:"0 8px 32px rgba(24,35,56,.12)",background:"#FFFFFF",fontFamily:'"Varela Round",sans-serif',fontSize:12,color:"#2563EB",lineHeight:1.6}}>{toast}</div>,document.body)}
 </div></PreviewContext.Provider>
}

