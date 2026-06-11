import { ReactNode } from "react";
import { Link } from "react-router-dom";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div>
      <header
        style={{
          borderBottom: "1px solid var(--border)",
          background: "var(--surface)",
        }}
      >
        <div
          className="container"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "1rem 1.25rem",
          }}
        >
          <Link to="/" style={{ textDecoration: "none", color: "var(--text)" }}>
            <span style={{ fontWeight: 700, fontSize: "1.15rem" }}>
              AISolidityAuditor
            </span>
            <span
              style={{
                marginLeft: "0.75rem",
                color: "var(--text-muted)",
                fontSize: "0.85rem",
              }}
            >
              Solidity triage · Slither + AI
            </span>
          </Link>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
