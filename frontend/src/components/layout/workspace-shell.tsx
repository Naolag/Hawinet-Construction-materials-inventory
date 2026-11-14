"use client";
import type{ReactNode}from"react";import Sidebar from "./sidebar";import MobileNavigation from "./mobile-navigation";import WorkspaceHeader from "./workspace-header";
export default function WorkspaceShell({children}:{children:ReactNode}){return <div className="workspace-app-shell"><div className="desktop-sidebar"><Sidebar/></div><WorkspaceHeader/><MobileNavigation/><main className="workspace-main"><div className="workspace-page-container">{children}</div><footer className="workspace-footer">Hawinet · Construction Material Inventory Management</footer></main></div>}
